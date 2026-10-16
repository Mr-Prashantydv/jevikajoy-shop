"""Build a draft Shopify import from verified Content Files URLs, never guessed URLs."""

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlsplit


def attach(rows, media, urls):
    by_handle = defaultdict(list)
    featured = {}
    seen = set()
    for item in media:
        name = Path(item["path"]).name
        url = urls.get(name)
        parts = urlsplit(url or "")
        if parts.scheme != "https" or parts.hostname != "cdn.shopify.com":
            raise ValueError(f"Missing or invalid observed Shopify URL: {name}")
        if name in seen:
            raise ValueError(f"Duplicate source filename: {name}")
        seen.add(name)
        if item["alt"].split()[0] != item["colour"]:
            raise ValueError(f"Colour-first alt mismatch: {name}")
        by_handle[item["handle"]].append((url, item["alt"]))
        if item["featuredForColour"]:
            key = (item["handle"], item["colour"])
            if key in featured:
                raise ValueError(f"Duplicate featured colour: {key}")
            featured[key] = url

    result = []
    indices = defaultdict(int)
    handles = {row["Handle"] for row in rows}
    if set(by_handle) - handles:
        raise ValueError("Media references a product missing from the catalog")
    # Shopify uses the first product image on collection cards. Put the first
    # variant colour's packshot first, not the alphabetically first back view.
    default_colours = {}
    for row in rows:
        colour = next((row[f"Option{n} Value"] for n in (1, 2)
                       if row[f"Option{n} Name"] in ("Color", "Colour")), None)
        if colour is None:
            raise ValueError(f"Missing colour option: {row['Handle']}")
        default_colours.setdefault(row["Handle"], colour)
    for handle, photos in by_handle.items():
        first = featured.get((handle, default_colours[handle]))
        if first:
            photos.sort(key=lambda photo: photo[0] != first)
    for source in rows:
        row = dict(source)
        if row["Status"].lower() != "draft" or row["Published"].upper() != "FALSE":
            raise ValueError("Import must stay draft and unpublished until reviewed")
        handle = row["Handle"]
        index = indices[handle]
        photos = by_handle[handle]
        row.update({"Image Src": "", "Image Position": "", "Image Alt Text": ""})
        if index < len(photos):
            row["Image Src"], row["Image Alt Text"] = photos[index]
            row["Image Position"] = str(index + 1)
        option = next((row[f"Option{n} Value"] for n in (1, 2)
                       if row[f"Option{n} Name"] in ("Color", "Colour")), None)
        if option is None:
            raise ValueError(f"Missing colour option: {handle}")
        row["Variant Image"] = featured.get((handle, option), "")
        indices[handle] += 1
        result.append(row)
    for handle, photos in by_handle.items():
        if len(photos) > indices[handle]:
            raise ValueError(f"Too few catalog rows for photos: {handle}")
    if len({r["Variant SKU"] for r in result}) != len(result):
        raise ValueError("Duplicate SKU")
    assert sum(bool(r["Image Src"]) for r in result) == len(media)
    assert {r["Variant Image"] for r in result if r["Variant Image"]} == set(featured.values())
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--export", type=Path, required=True)
    parser.add_argument("--urls", type=Path, required=True)
    args = parser.parse_args()
    with (args.export / "products.csv").open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        fields = reader.fieldnames
        rows = list(reader)
    media = json.loads((args.export / "media-manifest.json").read_text(encoding="utf-8"))
    urls = json.loads(args.urls.read_text(encoding="utf-8"))
    result = attach(rows, media, urls)
    target = args.export / "products-with-images.csv"
    fields = fields + ["Image Src", "Image Position", "Image Alt Text", "Variant Image"]

    def write_csv(path, batch):
        with path.open("w", encoding="utf-8-sig", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            writer.writerows(batch)

    write_csv(target, result)
    first_handle = result[0]["Handle"]
    write_csv(args.export / "products-canary.csv",
              [row for row in result if row["Handle"] == first_handle])
    write_csv(args.export / "products-remaining.csv",
              [row for row in result if row["Handle"] != first_handle])
    print(json.dumps({"path": str(target), "products": len({r["Handle"] for r in result}),
                      "variants": len(result), "images": len(media),
                      "featured_images": len({r["Variant Image"] for r in result if r["Variant Image"]}),
                      "variant_image_bindings": sum(bool(r["Variant Image"]) for r in result)}))


if __name__ == "__main__":
    main()
