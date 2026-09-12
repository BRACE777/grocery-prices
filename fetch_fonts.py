"""Download the page's typefaces so it does not depend on a third party.

The page's display voice is Barlow Condensed. Loading it from a font CDN means
a blocked or slow request ships the page in the platform's own sans instead,
which is a different design. These are fetched once, subset to latin, and
served from docs/ alongside the page.

    python fetch_fonts.py

Barlow and Barlow Condensed are licensed under the SIL Open Font License,
which allows redistribution; the licence is saved next to the files.
"""

from __future__ import annotations

import pathlib
import re
import shutil
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent
FONTS = ROOT / "docs" / "fonts"

# Only the weights the page actually sets.
WANTED = {
    "Barlow": [400, 600, 700],
    "Barlow+Condensed": [500, 600, 700, 800],
}

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
)
LICENCE = "https://raw.githubusercontent.com/jpt/barlow/master/OFL.txt"


def curl(url: str, out: pathlib.Path | None = None) -> bytes:
    binary = shutil.which("curl")
    command = [
        binary, "--silent", "--show-error", "--location", "--fail",
        "--max-time", "60", "--user-agent", UA,
    ]
    if out:
        command += ["--output", str(out)]
    command.append(url)
    result = subprocess.run(command, capture_output=True, check=False)
    if result.returncode != 0:
        detail = (result.stderr or b"").decode("utf-8", "replace").strip()
        raise SystemExit(f"could not fetch {url}\n  {detail}")
    return result.stdout


def main() -> int:
    FONTS.mkdir(parents=True, exist_ok=True)
    faces: list[tuple[str, int, str]] = []

    for family, weights in WANTED.items():
        spec = ";".join(f"0,{w}" for w in weights)
        css = curl(
            f"https://fonts.googleapis.com/css2?family={family}:ital,wght@{spec}"
            "&display=swap"
        ).decode("utf-8", "replace")

        # Keep only the latin block; the page has no other script in it.
        blocks = re.findall(r"/\*\s*([\w\-\[\]]+)\s*\*/\s*(@font-face\s*\{[^}]*\})", css)
        for subset, block in blocks:
            if subset != "latin":
                continue
            weight = re.search(r"font-weight:\s*(\d+)", block)
            url = re.search(r"url\((https://[^)]+\.woff2)\)", block)
            if not (weight and url):
                continue
            name = family.replace("+", "")
            filename = f"{name}-{weight.group(1)}.woff2"
            curl(url.group(1), FONTS / filename)
            size = (FONTS / filename).stat().st_size
            faces.append((family.replace("+", " "), int(weight.group(1)), filename))
            print(f"  {filename:<28} {size // 1024}KB")

    curl(LICENCE, FONTS / "OFL.txt")
    print(f"  {'OFL.txt':<28} {(FONTS / 'OFL.txt').stat().st_size // 1024}KB")

    declarations = "\n".join(
        "@font-face{"
        f'font-family:"{family}";font-style:normal;font-weight:{weight};'
        f"font-display:swap;src:url(fonts/{filename}) format('woff2')"
        "}"
        for family, weight, filename in sorted(faces, key=lambda f: (f[0], f[1]))
    )
    (FONTS / "faces.css").write_text(declarations + "\n", encoding="utf-8",
                                     newline="\n")
    print(f"\n{len(faces)} faces written. Declarations in {FONTS / 'faces.css'}")
    print("render.py embeds these inline; rerun fetch_prices.py --render.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
