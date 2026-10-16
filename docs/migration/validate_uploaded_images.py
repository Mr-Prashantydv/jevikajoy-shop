"""Check original CDN PNG URLs against master dimensions before a catalog import."""

import concurrent.futures
import json
import struct
import urllib.request
from pathlib import Path


def png_size(header):
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("Not a PNG")
    return struct.unpack(">II", header[16:24])


def main():
    root = Path(__file__).resolve().parents[2]
    export = root / "docs/migration/export-1uz1hi-01-20261004"
    media = json.loads((export / "media-manifest.json").read_text(encoding="utf-8"))
    urls = json.loads((export / "uploaded-image-urls.json").read_text(encoding="utf-8"))
    local = {Path(m["path"]).name: m for m in media}

    def check(item):
        name, url = item
        with (root / local[name]["path"]).open("rb") as stream:
            expected = png_size(stream.read(24))
        request = urllib.request.Request(url, headers={"Range": "bytes=0-23"})
        with urllib.request.urlopen(request, timeout=25) as response:
            size = png_size(response.read(24))
            if response.status not in (200, 206) or size != expected:
                raise ValueError(f"Original PNG mismatch: {name}: {size} vs {expected}")
        return name, {"url": url, "dimensions": list(size), "checked": True}

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        checks = dict(pool.map(check, urls.items()))
    (export / "uploaded-images-verified.json").write_text(json.dumps(checks, indent=2), encoding="utf-8")
    print(json.dumps({"verified": len(checks), "expected": len(media)}))


if __name__ == "__main__":
    main()
