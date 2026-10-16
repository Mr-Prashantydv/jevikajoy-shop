"""Run inside browser-use on Shopify Content Files; capture visible, observed URLs."""

import json
import re
from pathlib import Path

export = Path("D:/projects/JEVIKAJOY.SHOP/docs/migration/export-1uz1hi-01-20261004")
expected = {Path(m["path"]).stem: Path(m["path"]).name
            for m in json.loads((export / "media-manifest.json").read_text(encoding="utf-8"))}
observed = js('''Array.from(document.querySelectorAll('[role=row]'))
 .filter(e=>e.querySelector('s-thumbnail[src]') && e.querySelector('a[data-primary-link]'))
 .map(e=>({name:e.querySelector('a[data-primary-link]').textContent,
           thumbnail:e.querySelector('s-thumbnail[src]').getAttribute('src'),
           admin:e.querySelector('a[data-primary-link]').href}))''')
target = export / "uploaded-files-observed.json"
records = json.loads(target.read_text(encoding="utf-8")) if target.exists() else {}
urls_target = export / "uploaded-image-urls.json"
urls = json.loads(urls_target.read_text(encoding="utf-8")) if urls_target.exists() else {}
for item in observed:
    name = expected.get(item["name"])
    if name is None:
        continue
    thumb = item["thumbnail"]
    if not thumb.startswith("https://cdn.shopify.com/") or "_800x800.png" not in thumb:
        raise ValueError(f"Unexpected thumbnail format: {name}")
    # Shopify's observed legacy image-size suffix is removed; validate original URLs
    # separately against the PNG masters before importing. Never construct the store ID.
    original = re.sub(r"_800x800(?=\.png(?:\?|$))", "", thumb)
    if original.split("?")[0].rsplit("/", 1)[-1] != name:
        raise ValueError(f"Filename changed or duplicate renamed: {name}")
    records[name] = item
    urls[name] = original
target.write_text(json.dumps(records, indent=2), encoding="utf-8")
urls_target.write_text(json.dumps(urls, indent=2), encoding="utf-8")
print(json.dumps({"observed_this_page": len(observed), "captured": len(urls),
                  "expected": len(expected)}))
