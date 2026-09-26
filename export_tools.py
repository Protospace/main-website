#!/usr/bin/env python3
"""Export the Protospace Wiki tool catalog and its thumbnails.

Usage:
    python3 export_tools.py

The wiki uses a small JavaScript challenge.  The equivalent cookie is sent on
both the page request and each thumbnail request.
"""
from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

WIKI_URL = "https://wiki.protospace.ca/Tools_we_have"
WIKI_ROOT = "https://wiki.protospace.ca"
COOKIE = "human_check=verified"
ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "tools.json"
IMAGE_DIR = ROOT / "assets" / "tools"


class ToolsParser(HTMLParser):
    """Extract ordered category/gallery data from the MediaWiki HTML."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.category: str | None = None
        self.in_h2 = False
        self.h2_text: list[str] = []
        self.item: dict | None = None
        self.item_depth = 0
        self.anchor: dict | None = None
        self.items: list[dict] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        if tag == "h2":
            self.in_h2 = True
            self.h2_text = []
        elif tag == "li" and "gallerybox" in (attrs_dict.get("class") or "").split():
            self.item = {"category": self.category, "anchors": [], "src": None}
            self.item_depth = 1
        elif self.item is not None and tag == "li":
            self.item_depth += 1
        elif self.item is not None and tag == "a":
            self.anchor = {"href": attrs_dict.get("href"), "text": []}
        elif self.item is not None and tag == "img" and self.item["src"] is None:
            self.item["src"] = attrs_dict.get("src")

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        if tag == "h2" and self.in_h2:
            category = " ".join("".join(self.h2_text).split())
            if category and category.lower() != "contents":
                self.category = category
            self.in_h2 = False
        elif tag == "a" and self.anchor is not None:
            self.anchor["text"] = " ".join("".join(self.anchor["text"]).split())
            if self.item is not None:
                self.item["anchors"].append(self.anchor)
            self.anchor = None
        elif tag == "li" and self.item is not None:
            self.item_depth -= 1
            if self.item_depth == 0:
                if self.item["category"] and self.item["category"].lower() != "removed equipment":
                    self.items.append(self.item)
                self.item = None

    def handle_data(self, data: str) -> None:
        if self.in_h2:
            self.h2_text.append(data)
        if self.anchor is not None:
            self.anchor["text"].append(data)


def fetch(url: str) -> tuple[bytes, str]:
    request = Request(url, headers={"Cookie": COOKIE, "User-Agent": "Protospace tools exporter/1.0"})
    with urlopen(request, timeout=30) as response:
        content_type = response.headers.get_content_type()
        return response.read(), content_type


def image_filename(src: str) -> str:
    parts = [part for part in urlparse(src).path.split("/") if part]
    # MediaWiki thumbnails end with e.g. 120px-182.jpg; the preceding part is
    # the original filename and is stable even when thumbnail dimensions change.
    if len(parts) >= 2:
        return parts[-2]
    return Path(parts[-1]).name


def main() -> int:
    try:
        page_bytes, content_type = fetch(WIKI_URL)
    except Exception as exc:
        print(f"Could not fetch {WIKI_URL}: {exc}", file=sys.stderr)
        return 1
    if content_type != "text/html" or b"Verifying you are human" in page_bytes:
        print("The wiki returned the human-verification page; check the cookie.", file=sys.stderr)
        return 1

    parser = ToolsParser()
    parser.feed(page_bytes.decode("utf-8", errors="replace"))
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    exported: list[dict[str, str]] = []
    skipped = 0

    for raw in parser.items:
        anchors = raw["anchors"]
        name_anchor = next((a for a in anchors if "_ID:" in (a["href"] or "") or " ID:" in a["text"]), None)
        name = name_anchor["text"] if name_anchor else ""
        id_match = re.search(r"\bID:(\d+)\s*$", name)
        photo_src = raw["src"]
        if not name or not id_match or not photo_src:
            skipped += 1
            continue
        photo_url = urljoin(WIKI_ROOT, photo_src)
        source_filename = image_filename(photo_url)
        filename = f"{id_match.group(1)}{Path(source_filename).suffix.lower()}"
        destination = IMAGE_DIR / filename
        try:
            image_bytes, image_type = fetch(photo_url)
            if not image_type.startswith("image/") or not image_bytes:
                raise ValueError(f"response was {image_type}, not an image")
            destination.write_bytes(image_bytes)
        except Exception as exc:
            print(f"Skipping {name}: broken photo ({exc})", file=sys.stderr)
            skipped += 1
            continue

        link = urljoin(WIKI_ROOT, name_anchor["href"])
        exported.append(
            {
                "ID": id_match.group(1),
                "name": re.sub(r"\s*ID:\d+\s*$", "", name).strip(),
                "photo file": f"/assets/tools/{filename}",
                "link": link,
                "category": raw["category"],
            }
        )

    OUTPUT.write_text(json.dumps(exported, ensure_ascii=False, indent=2) + "\n")
    print(f"Exported {len(exported)} tools to {OUTPUT}")
    print(f"Skipped {skipped} tools without valid metadata or photos")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
