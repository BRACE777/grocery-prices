"""Clients for the Woolworths and Coles online price feeds.

Both are undocumented internal endpoints. They work over plain HTTP from a
residential connection but are blocked from most data centres, which is why
this runs on the user's own machine rather than in the cloud.

Neither feed exposes member pricing (Everyday Rewards / Flybuys) when not
signed in, so every price here is the standard shelf price.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
import time
import urllib.parse
from dataclasses import dataclass

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
)

# Requests go out through curl rather than Python's own HTTP client. Imperva,
# which fronts Coles, fingerprints the TLS handshake: curl is served the real
# site while urllib is served a challenge page from the same address, with
# identical headers. curl also ships with Windows, so this adds no dependency.
#
# Compression is left to curl's --compressed flag, which sets its own
# Accept-Encoding and decodes the response.
BROWSER_HEADERS = {
    "User-Agent": UA,
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "image/avif,image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "en-AU,en;q=0.9",
    "Upgrade-Insecure-Requests": "1",
    "sec-ch-ua": '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
}

POLITE_DELAY = 1.2  # seconds between requests to a single retailer
CHALLENGE_BACKOFF = 2.5  # seconds, multiplied by the attempt number
CHALLENGE_RETRIES = 4


class FetchError(RuntimeError):
    """A price could not be read. The caller renders these as a red cell.

    ``permanent`` marks a failure that retrying cannot fix, such as a 404 for a
    product that no longer exists, as opposed to a transient bot challenge.
    """

    def __init__(self, message: str, permanent: bool = False) -> None:
        super().__init__(message)
        self.permanent = permanent


@dataclass
class Offer:
    """One retailer's current offer for one product."""

    chain: str
    product_id: str
    name: str
    size: str = ""
    price: float | None = None
    was_price: float | None = None
    unit_price: float | None = None
    unit_measure: str = ""
    on_special: bool = False
    special_label: str = ""
    available: bool = True
    url: str = ""
    slug: str = ""
    error: str = ""

    @property
    def ok(self) -> bool:
        return self.error == "" and self.price is not None

    @property
    def saving(self) -> float | None:
        if self.was_price and self.price and self.was_price > self.price:
            return round(self.was_price - self.price, 2)
        return None

    @property
    def saving_percent(self) -> int | None:
        if self.was_price and self.price and self.was_price > self.price:
            return round((self.was_price - self.price) / self.was_price * 100)
        return None

    def as_dict(self) -> dict:
        d = {
            "chain": self.chain,
            "productId": self.product_id,
            "name": self.name,
            "size": self.size,
            "price": self.price,
            "wasPrice": self.was_price,
            "unitPrice": self.unit_price,
            "unitMeasure": self.unit_measure,
            "onSpecial": self.on_special,
            "specialLabel": self.special_label,
            "available": self.available,
            "url": self.url,
            "slug": self.slug,
            "error": self.error,
            "saving": self.saving,
            "savingPercent": self.saving_percent,
        }
        return d


class _Session:
    """Cookie-aware HTTP client backed by curl.

    One cookie jar per session, kept on disk for curl to read and write, so a
    challenge that hands back a cookie is presented on the retry.
    """

    def __init__(self) -> None:
        self._curl = shutil.which("curl")
        if not self._curl:
            raise FetchError(
                "curl was not found on PATH. It ships with Windows 10 and 11; "
                "if it is missing, install Git for Windows or curl itself.",
                permanent=True,
            )
        handle, self._jar = tempfile.mkstemp(prefix="pricejar-", suffix=".txt")
        os.close(handle)
        self._last_request = 0.0

    def __del__(self) -> None:
        try:
            os.unlink(self._jar)
        except OSError:
            pass

    def get(
        self,
        url: str,
        headers: dict | None = None,
        timeout: int = 30,
        retries: int = 0,
        data: str | None = None,
    ) -> bytes:
        """Fetch a URL, retrying transient bot challenges.

        A challenge is worth retrying because it hands back cookies that the
        next attempt presents, which is usually enough to be let through. A 404
        is not, so it fails immediately.
        """
        last: FetchError | None = None
        for attempt in range(retries + 1):
            if attempt:
                time.sleep(CHALLENGE_BACKOFF * attempt)
            try:
                return self._get_once(url, headers, timeout, data)
            except FetchError as exc:
                if exc.permanent:
                    raise
                last = exc
        raise last if last else FetchError("request failed")

    def _get_once(
        self, url: str, headers: dict | None, timeout: int, data: str | None = None
    ) -> bytes:
        wait = POLITE_DELAY - (time.monotonic() - self._last_request)
        if wait > 0:
            time.sleep(wait)

        body_handle, body_path = tempfile.mkstemp(prefix="pricebody-")
        os.close(body_handle)
        command = [
            self._curl,
            "--silent",
            "--show-error",
            "--compressed",
            "--location",
            "--cookie", self._jar,
            "--cookie-jar", self._jar,
            "--max-time", str(timeout),
            "--output", body_path,
            "--write-out", "%{http_code}",
        ]
        for name, value in {**BROWSER_HEADERS, **(headers or {})}.items():
            command += ["--header", f"{name}: {value}"]
        if data is not None:
            command += ["--data-binary", data]
        command.append(url)

        try:
            result = subprocess.run(
                command, capture_output=True, timeout=timeout + 15, check=False
            )
            status = (result.stdout or b"").decode("ascii", "ignore").strip()[-3:]
            if not status.isdigit():
                detail = (result.stderr or b"").decode("utf-8", "replace").strip()
                raise FetchError(f"curl failed: {detail or 'no response'}")
            code = int(status)
            with open(body_path, "rb") as handle:
                payload = handle.read()
            if code != 200:
                raise FetchError(f"HTTP {code}", permanent=code == 404)
            return payload
        except subprocess.TimeoutExpired as exc:
            raise FetchError("request timed out") from exc
        finally:
            self._last_request = time.monotonic()
            try:
                os.unlink(body_path)
            except OSError:
                pass

    def post_json(
        self, url: str, body: str, headers: dict | None = None, retries: int = 0
    ) -> dict:
        """POST a JSON body. Used only by the Woolworths search endpoint."""
        raw = self.get(
            url,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                **(headers or {}),
            },
            retries=retries,
            data=body,
        )
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            raise FetchError("search response was not JSON") from exc

    def get_json(self, url: str, headers: dict | None = None, retries: int = 0) -> dict:
        raw = self.get(
            url, headers={"Accept": "application/json", **(headers or {})}, retries=retries
        )
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            raise FetchError("response was not JSON (likely a bot challenge)") from exc


class Woolworths:
    """Reads the Woolworths product detail API.

    Requires an Akamai cookie, which is issued by a plain request to the
    homepage. No JavaScript execution or sign-in is involved.
    """

    chain = "woolworths"
    label = "Woolworths"
    BASE = "https://www.woolworths.com.au"

    def __init__(self) -> None:
        self.session = _Session()
        self._primed = False

    def _prime(self) -> None:
        if self._primed:
            return
        self.session.get(self.BASE + "/", retries=CHALLENGE_RETRIES)
        self._primed = True

    def fetch(self, product_id: str) -> Offer:
        offer = Offer(chain=self.chain, product_id=str(product_id), name="")
        try:
            self._prime()
            data = self.session.get_json(
                f"{self.BASE}/apis/ui/product/detail/{product_id}"
            )
        except FetchError as exc:
            offer.error = str(exc)
            return offer

        p = data.get("Product") or {}
        if not p or p.get("Stockcode") in (None, 0):
            offer.error = "product not found"
            return offer

        offer.name = (p.get("Name") or "").strip()
        offer.size = (p.get("PackageSize") or "").strip()
        offer.price = _as_float(p.get("Price"))
        was = _as_float(p.get("WasPrice"))
        offer.was_price = was if was and offer.price and was > offer.price else None
        offer.unit_price = _as_float(p.get("CupPrice"))
        offer.unit_measure = (p.get("CupMeasure") or "").strip()
        offer.available = bool(p.get("IsAvailable"))
        offer.on_special = bool(p.get("IsOnSpecial")) or offer.was_price is not None
        if p.get("IsHalfPrice"):
            offer.special_label = "Half price"
        elif offer.on_special:
            offer.special_label = "Special"
        slug = p.get("UrlFriendlyName") or ""
        offer.url = f"{self.BASE}/shop/productdetails/{product_id}/{slug}".rstrip("/")
        if offer.price is None:
            offer.error = "no price in response"
        return offer

    def search(self, term: str, limit: int = 8) -> list[dict]:
        self._prime()
        body = json.dumps(
            {
                "SearchTerm": term,
                "PageSize": limit,
                "PageNumber": 1,
                "SortType": "TraderRelevance",
                "Location": f"/shop/search/products?searchTerm={urllib.parse.quote(term)}",
                "Filters": [],
                "IsSpecial": False,
                "GpBoost": 0,
            }
        )
        data = self.session.post_json(
            f"{self.BASE}/apis/ui/Search/products", body, retries=CHALLENGE_RETRIES
        )

        out: list[dict] = []
        for group in data.get("Products") or []:
            for p in group.get("Products") or []:
                out.append(
                    {
                        "id": str(p.get("Stockcode")),
                        "name": p.get("Name"),
                        "size": p.get("PackageSize"),
                        "price": _as_float(p.get("Price")),
                    }
                )
        return out[:limit]


class Coles:
    """Reads the Coles Next.js data routes.

    Two wrinkles. The build id changes on every deployment and must be read
    from a page first. And products are addressed by slug, not id, so an id is
    resolved to its canonical slug via the redirect the site itself returns.
    Both are cached for the life of the run and re-resolved when stale.
    """

    chain = "coles"
    label = "Coles"
    BASE = "https://www.coles.com.au"

    # Any product works for checking whether a cached build id still resolves.
    PROBE_ID = "2993706"

    def __init__(self, build_id_hint: str = "") -> None:
        self.session = _Session()
        self._build_id: str | None = None
        self._hint = build_id_hint

    @property
    def build_id(self) -> str:
        if self._build_id is None:
            self._build_id = self._hint if self._hint_works() else self._read_build_id()
        return self._build_id

    def _hint_works(self) -> bool:
        """Does last run's build id still resolve? Saves hitting the homepage.

        The homepage is an HTML path and is challenged far more often than the
        JSON data routes, so it is worth avoiding when we already have an id.

        Only a 404 proves the cached id is stale. Any other failure says
        nothing about it, so the id is kept rather than thrown away in favour
        of a homepage read that is even more likely to be blocked.
        """
        if not self._hint:
            return False
        url = (
            f"{self.BASE}/_next/data/{self._hint}/en/product/"
            f"x-{self.PROBE_ID}.json"
        )
        try:
            data = self.session.get_json(url, retries=CHALLENGE_RETRIES)
        except FetchError as exc:
            return not exc.permanent
        return bool((data.get("pageProps") or {}).get("__N_REDIRECT"))

    def _read_build_id(self) -> str:
        """Read a fresh build id from the homepage, retrying challenges."""
        html = self.session.get(
            self.BASE + "/", retries=CHALLENGE_RETRIES
        ).decode("utf-8", "replace")
        match = re.search(r'"buildId":"([^"]+)"', html)
        if not match:
            raise FetchError(
                "Coles served a bot challenge instead of the homepage; "
                "could not read its build id"
            )
        return match.group(1)

    def _data_url(self, path: str) -> str:
        return f"{self.BASE}/_next/data/{self.build_id}/en/{path}"

    def resolve_slug(self, product_id: str) -> str:
        """Ask Coles for the canonical slug of a product id."""
        data = self.session.get_json(
            self._data_url(f"product/x-{product_id}.json"), retries=CHALLENGE_RETRIES
        )
        target = (data.get("pageProps") or {}).get("__N_REDIRECT")
        if not target:
            raise FetchError("no canonical slug returned")
        return target.rsplit("/", 1)[-1]

    def fetch(self, product_id: str, slug: str = "") -> Offer:
        offer = Offer(chain=self.chain, product_id=str(product_id), name="")
        try:
            if not slug:
                slug = self.resolve_slug(product_id)
            data = self._fetch_product(slug)
            if data is None:
                # A stale slug or a rotated build id both land here. Re-resolve
                # once from the id, which is the stable handle.
                self._build_id = None
                slug = self.resolve_slug(product_id)
                data = self._fetch_product(slug)
            if data is None:
                offer.error = "product not found"
                return offer
        except FetchError as exc:
            offer.error = str(exc)
            return offer

        offer.slug = slug
        brand = (data.get("brand") or "").strip()
        name = (data.get("name") or "").strip()
        offer.name = f"{brand} {name}".strip()
        offer.size = (data.get("size") or "").strip()
        offer.available = bool(data.get("availability", True))

        pricing = data.get("pricing") or {}
        offer.price = _as_float(pricing.get("now"))
        was = _as_float(pricing.get("was"))
        offer.was_price = was if was and offer.price and was > offer.price else None
        unit = pricing.get("unit") or {}
        offer.unit_price = _as_float(unit.get("price"))
        measure_qty = unit.get("ofMeasureQuantity")
        measure_units = unit.get("ofMeasureUnits") or ""
        if measure_units:
            offer.unit_measure = f"{measure_qty or ''}{measure_units}".strip()
        offer.on_special = (
            pricing.get("promotionType") == "SPECIAL" or offer.was_price is not None
        )
        offer.special_label = (
            pricing.get("priceDescription") or pricing.get("saveStatement") or ""
        ).strip()
        if offer.on_special and not offer.special_label:
            offer.special_label = "Special"
        offer.url = f"{self.BASE}/product/{slug}"
        if offer.price is None:
            offer.error = "no price in response"
        return offer

    def _fetch_product(self, slug: str) -> dict | None:
        try:
            data = self.session.get_json(
                self._data_url(f"product/{slug}.json"), retries=CHALLENGE_RETRIES
            )
        except FetchError:
            return None
        product = (data.get("pageProps") or {}).get("product")
        return product or None

    def search(self, term: str, limit: int = 8) -> list[dict]:
        url = self._data_url("search/products.json") + "?" + urllib.parse.urlencode(
            {"q": term}
        )
        data = self.session.get_json(url, retries=CHALLENGE_RETRIES)
        results = (
            ((data.get("pageProps") or {}).get("searchResults") or {}).get("results")
            or []
        )
        out: list[dict] = []
        for r in results:
            if not r.get("id"):
                continue
            out.append(
                {
                    "id": str(r["id"]),
                    "name": f"{r.get('brand','')} {r.get('name','')}".strip(),
                    "size": r.get("size"),
                    "price": _as_float((r.get("pricing") or {}).get("now")),
                }
            )
        return out[:limit]


def _as_float(value) -> float | None:
    try:
        if value is None or value == "":
            return None
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if number > 0 else None
