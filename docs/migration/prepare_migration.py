"""Prepare local JJW migration artifacts; this script makes no network writes."""

import argparse
import csv
import hashlib
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
THEME_DIRS = {"assets", "blocks", "config", "layout", "locales", "sections", "snippets", "templates"}
COLOURS = {"navy": "Blue", "mustard": "Yellow", "yellow": "Yellow", "blue": "Blue", "black": "Black",
           "white": "White", "pink": "Pink", "peach": "Peach", "sand": "Sand"}


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", required=True)
    parser.add_argument("--theme-path", type=Path, default=ROOT,
                        help="Theme directory, preferably a fresh destination CLI pull")
    parser.add_argument("--output", type=Path,
                        help="Versioned export folder within docs/migration")
    parser.add_argument("--include-media", action="store_true",
                        help="Also package all local masters and policy drafts into a store export ZIP")
    args = parser.parse_args()
    destination = args.destination
    if not destination.endswith(".myshopify.com") or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789-." for c in destination):
        raise ValueError("Destination must be a lowercase myshopify.com domain")

    snapshot = read_json(ROOT / "docs/migration/store-snapshot.json")
    catalog = read_json(ROOT / "_probe/products_payload.json")
    source_products = {p["handle"]: p for p in snapshot["products"]["items"]}
    if set(catalog) != set(source_products):
        raise ValueError("Saved catalog and snapshot handles differ")
    variant_count = sum(len(p["variants"]) for p in catalog.values())
    if (len(catalog), variant_count) != (10, 172):
        raise ValueError("Saved product or variant count changed; review before proceeding")

    # Build from current files, not the historical root ZIP. A supplied fresh
    # remote pull also preserves settings changed by the merchant in the editor.
    theme_root = args.theme_path.resolve()
    if not (theme_root / "layout/theme.liquid").is_file():
        raise ValueError(f"Not a theme directory: {theme_root}")
    theme_files = sorted(p for directory in THEME_DIRS
                         for p in (theme_root / directory).glob("*") if p.is_file()
                         and p.suffix.lower() in {".liquid", ".json", ".css", ".js", ".png", ".webp",
                                                  ".jpg", ".jpeg", ".svg", ".gif", ".woff", ".woff2",
                                                  ".ttf", ".otf", ".mp4"})
    theme_entries = {p.relative_to(theme_root).as_posix() for p in theme_files}
    output = (args.output or ROOT / "docs/migration" / f"prepared-{destination.split('.')[0]}").resolve()
    output.relative_to((ROOT / "docs/migration").resolve())
    output.mkdir(parents=True, exist_ok=True)
    theme_source = output / "JJW-theme.zip"
    with zipfile.ZipFile(theme_source, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for file in theme_files:
            archive.write(file, file.relative_to(theme_root).as_posix())
    with zipfile.ZipFile(theme_source) as archive:
        bad = archive.testzip()
        if bad or set(archive.namelist()) != theme_entries:
            raise ValueError(f"Invalid generated theme archive: {bad}")
        for file in theme_files:
            if archive.read(file.relative_to(theme_root).as_posix()) != file.read_bytes():
                raise ValueError(f"Theme archive mismatch: {file}")

    products, media, rows, skus = [], [], [], set()
    warnings = ["Saved data is a reconstruction, not a fresh export of bnwvrc-04.",
                "Prices and inventory quantities are historical; verify stock before publishing.",
                "CSV contains no image URLs. Upload local media separately and assign packshots to variants.",
                "Remote-only theme edits, orders, customers, reviews, metafields, settings and files may be absent."]
    for handle, saved in catalog.items():
        product = {"handle": handle, **saved, "status": "DRAFT"}
        for variant in product["variants"]:
            for quantity in variant.get("inventoryQuantities", []):
                quantity.pop("locationId", None)
        products.append(product)
        options = {o["name"]: {v["name"] for v in o["values"]} for o in saved["productOptions"]}
        pairs = set()
        for index, variant in enumerate(saved["variants"]):
            values = {v["optionName"]: v["name"] for v in variant["optionValues"]}
            pair = (values["Size"], values["Color"])
            if pair in pairs or values["Size"] not in options["Size"] or values["Color"] not in options["Color"]:
                raise ValueError(f"Invalid option combination on {handle}: {pair}")
            pairs.add(pair)
            sku = variant["sku"]
            if not sku or sku in skus:
                raise ValueError(f"Missing or duplicate SKU: {sku}")
            skus.add(sku)
            quantity = sum(q["quantity"] for q in variant.get("inventoryQuantities", []))
            rows.append({"Handle": handle, "Title": saved["title"] if index == 0 else "",
                         "Body (HTML)": saved["descriptionHtml"] if index == 0 else "",
                         "Vendor": saved["vendor"] if index == 0 else "",
                         "Type": saved["productType"] if index == 0 else "",
                         "Tags": ", ".join(saved["tags"]) if index == 0 else "",
                         "Published": "FALSE", "Option1 Name": "Size", "Option1 Value": values["Size"],
                         "Option2 Name": "Color", "Option2 Value": values["Color"],
                         "Variant SKU": sku, "Variant Price": variant["price"],
                         "Variant Inventory Tracker": "shopify", "Variant Inventory Qty": quantity,
                         "Variant Inventory Policy": variant["inventoryPolicy"].lower(),
                         "Variant Fulfillment Service": "manual", "Status": "draft"})
        if len(pairs) != len(options["Size"]) * len(options["Color"]):
            raise ValueError(f"Incomplete variant combinations for {handle}")

        source = source_products[handle]
        covered_colours = set()
        if source.get("hasImages"):
            folder = ROOT / source["imageFolder"]
            files = sorted(folder.glob("*/*.png"))
            if not files:
                raise ValueError(f"No local images for {handle}")
            for image_path in files:
                colour = COLOURS[image_path.parent.name]
                if colour not in options["Color"]:
                    raise ValueError(f"Unexpected photo colour on {handle}: {colour}")
                covered_colours.add(colour)
                shot = image_path.stem.split("-", 4)[4].replace("-", " ")
                media.append({"handle": handle, "colour": colour,
                              "path": image_path.relative_to(ROOT).as_posix(),
                              "alt": f"{colour} {saved['title']} {shot}",
                              "featuredForColour": "packshot" in shot,
                              "bytes": image_path.stat().st_size, "sha256": sha256(image_path)})
            for colour in covered_colours:
                if sum(m["featuredForColour"] for m in media if m["handle"] == handle and m["colour"] == colour) != 1:
                    raise ValueError(f"Expected one packshot for {handle} / {colour}")
        missing_photos = sorted(options["Color"] - covered_colours)
        if missing_photos:
            warnings.append(f"{handle}: no saved photos for {', '.join(missing_photos)}")

    collections = [{"handle": c["handle"], "title": c["title"], "rule": c["rule"]}
                   for c in snapshot["collections"]["items"] if c.get("rule")]
    menus = [{"handle": handle, "title": menu["title"],
              "items": [{k: item[k] for k in ("title", "type", "url") if k in item} for item in menu["items"]]}
             for handle, menu in snapshot["navigation"].items() if handle != "customer-account-main-menu"]
    pages = [{"handle": p["handle"], "title": p["title"], "templateSuffix": p["templateSuffix"],
              "body": "" if p["body"] == "EMPTY" else p["body"]} for p in snapshot["pages"]]

    write_json(output / "products.json", products)
    write_json(output / "media-manifest.json", media)
    write_json(output / "content.json", {"collections": collections, "menus": menus, "pages": pages})
    write_json(output / "settings-reference.json", {
        "provenance": "Historical snapshot; review against the intended destination settings before applying.",
        "currency": snapshot["shop"]["currency"],
        "customerAccounts": snapshot["shop"]["customerAccounts"],
        "discounts": [{k: discount[k] for k in ("kind", "terms")} for discount in snapshot["discounts"]],
        "shipping": snapshot["shipping"],
        "notCaptured": snapshot["_meta"]["gaps"],
        "policyDrafts": "docs/policies/ (merchant commitments require review)",
        "paymentSetup": "Configure in destination admin; account credentials do not migrate with the theme.",
    })
    with (output / "products.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    artifact_names = {"JJW-theme.zip", "products.json", "products.csv", "media-manifest.json",
                      "content.json", "settings-reference.json"}
    if (output / "README.md").is_file():
        artifact_names.add("README.md")
    manifest = {"preparedDate": "2026-10-04", "destination": destination,
                "sourceStore": "bnwvrc-04.myshopify.com", "snapshotStore": snapshot["_meta"]["store"],
                "uploaded": False, "themeFiles": len(theme_entries), "products": len(products),
                "variants": variant_count, "images": len(media), "collections": len(collections),
                "menus": len(menus), "pages": len(pages), "warnings": warnings,
                "themeSource": str(theme_root),
                "files": {name: sha256(output / name) for name in sorted(artifact_names)}}
    write_json(output / "manifest.json", manifest)
    if args.include_media:
        store_archive = output / "JJW-store-export.zip"
        # Include only explicitly scoped data. Never package _probe, browser
        # profiles, staged-upload signatures, credentials, or session archives.
        archive_sources = {name: output / name for name in artifact_names | {"manifest.json"}}
        archive_sources.update({m["path"]: ROOT / m["path"] for m in media})
        archive_sources.update({p.relative_to(ROOT).as_posix(): p
                                for p in (ROOT / "docs/policies").glob("*")
                                if p.is_file() and p.suffix in {".html", ".md"}})
        with zipfile.ZipFile(store_archive, "w", compression=zipfile.ZIP_STORED) as archive:
            for name, file in sorted(archive_sources.items()):
                archive.write(file, name)
        with zipfile.ZipFile(store_archive) as archive:
            bad = archive.testzip()
            if bad or set(archive.namelist()) != set(archive_sources):
                raise ValueError(f"Invalid store export archive: {bad}")
            for name, file in archive_sources.items():
                if hashlib.sha256(archive.read(name)).hexdigest() != sha256(file):
                    raise ValueError(f"Store archive mismatch: {name}")
        print(json.dumps({"archive": str(store_archive), "entries": len(archive_sources),
                          "bytes": store_archive.stat().st_size, "sha256": sha256(store_archive)}, indent=2))
    print(json.dumps({k: v for k, v in manifest.items() if k not in {"warnings", "files"}}, indent=2))
    print(f"Artifacts: {output}")


if __name__ == "__main__":
    main()
