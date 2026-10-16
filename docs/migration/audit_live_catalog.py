"""Compare the anonymous storefront catalog with the reviewed recovery CSV."""
import csv
import json
from collections import defaultdict
from decimal import Decimal
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).parent / 'export-1uz1hi-01-20261004'

def main():
    with (ROOT / 'products-with-images.csv').open(encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    expected = defaultdict(list)
    for row in rows:
        expected[row['Handle']].append(row)
    with urlopen('https://jevikajoy.shop/products.json?limit=250', timeout=30) as f:
        live = json.load(f)['products']
    errors = []
    if set(expected) != {p['handle'] for p in live}:
        errors.append('Product handles differ')
    checks = []
    for product in live:
        source = expected.get(product['handle'])
        if not source:
            continue
        first = source[0]
        for field, csv_field in [('title', 'Title'), ('body_html', 'Body (HTML)'),
                                 ('vendor', 'Vendor'), ('product_type', 'Type')]:
            if product[field] != first[csv_field]:
                errors.append(f"{product['handle']}: {field} differs")
        tags = product['tags']
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(',')]
        if set(tags) != {t.strip() for t in first['Tags'].split(',')}:
            errors.append(f"{product['handle']}: tags differ")
        variants = {v['sku']: v for v in product['variants']}
        if set(variants) != {r['Variant SKU'] for r in source}:
            errors.append(f"{product['handle']}: SKUs differ")
        with urlopen(f"https://jevikajoy.shop/products/{product['handle']}.js", timeout=30) as f:
            ajax = json.load(f)
        photos = {i['alt']: i for i in ajax.get('media', []) if i['media_type'] == 'image'}
        expected_alts = {r['Image Alt Text'] for r in source if r['Image Src']}
        if set(photos) != expected_alts or len(photos) != len(product['images']):
            errors.append(f"{product['handle']}: photos/alt labels differ")
        for i in (1, 2):
            values = list(dict.fromkeys(r[f'Option{i} Value'] for r in source))
            option = product['options'][i-1]
            if option['name'] != first[f'Option{i} Name'] or option['values'] != values:
                errors.append(f"{product['handle']}: option {i} order differs")
        for row in source:
            v = variants.get(row['Variant SKU'])
            if not v:
                continue
            if Decimal(v['price']) != Decimal(row['Variant Price']):
                errors.append(f"{v['sku']}: price differs")
            if [v['option1'], v['option2']] != [row['Option1 Value'], row['Option2 Value']]:
                errors.append(f"{v['sku']}: options differ")
            featured = v.get('featured_image')
            if row['Variant Image']:
                alt = next(r['Image Alt Text'] for r in source
                           if r['Image Src'] == row['Variant Image'])
                if not featured or featured['src'] != photos.get(alt, {}).get('src'):
                    errors.append(f"{v['sku']}: featured packshot differs")
        if ajax.get('media') and ajax['media'][0]['alt'] != first['Image Alt Text']:
            errors.append(f"{product['handle']}: primary card packshot differs")
        checks.append({'handle': product['handle'], 'variants': len(product['variants']),
                       'images': len(product['images']), 'published': bool(product['published_at'])})
    report = {'url': 'https://jevikajoy.shop', 'products': checks,
              'product_count': len(live), 'variant_count': sum(len(p['variants']) for p in live),
              'image_count': sum(len(p['images']) for p in live), 'errors': errors,
              'limitations': ['Physical inventory not verified', 'Payments and checkout not verified']}
    (ROOT / 'live-catalog-audit.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))
    raise SystemExit(bool(errors))

if __name__ == '__main__':
    main()
