"""Read-only checks for the recovered catalog and its image mapping."""

import copy
import csv
import json
import unittest
from pathlib import Path

from attach_image_urls import attach


class CatalogImageMappingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        export = Path(__file__).parent / "export-1uz1hi-01-20261004"
        with (export / "products.csv").open(encoding="utf-8-sig", newline="") as stream:
            cls.rows = list(csv.DictReader(stream))
        cls.media = json.loads((export / "media-manifest.json").read_text(encoding="utf-8"))
        cls.urls = {Path(item["path"]).name:
                    "https://cdn.shopify.com/fixture/" + Path(item["path"]).name
                    for item in cls.media}

    def test_preserves_catalog_and_all_photos(self):
        result = attach(self.rows, self.media, self.urls)
        self.assertEqual(len(result), 172)
        self.assertEqual(len({row["Handle"] for row in result}), 10)
        self.assertEqual(len({row["Variant SKU"] for row in result}), 172)
        self.assertEqual(sum(bool(row["Image Src"]) for row in result), 80)
        self.assertEqual(sum(bool(row["Variant Image"]) for row in result), 88)
        self.assertEqual(len({row["Variant Image"] for row in result
                              if row["Variant Image"]}), 20)
        for source, row in zip(self.rows, result):
            for key, value in source.items():
                self.assertEqual(row[key], value)

    def test_first_image_is_default_colour_packshot(self):
        result = attach(self.rows, self.media, self.urls)
        first = {}
        for row in result:
            first.setdefault(row["Handle"], row)
        for row in first.values():
            if row["Image Src"]:
                self.assertEqual(row["Image Position"], "1")
                self.assertEqual(row["Image Src"], row["Variant Image"])
                self.assertIn("packshot", row["Image Alt Text"].lower())

    def test_missing_url_fails(self):
        urls = dict(self.urls)
        urls.pop(next(iter(urls)))
        with self.assertRaisesRegex(ValueError, "Missing or invalid"):
            attach(self.rows, self.media, urls)

    def test_duplicate_media_fails(self):
        with self.assertRaisesRegex(ValueError, "Duplicate source filename"):
            attach(self.rows, self.media + self.media[:1], self.urls)

    def test_wrong_colour_alt_fails(self):
        media = copy.deepcopy(self.media)
        media[0]["alt"] = "Unknown colour"
        with self.assertRaisesRegex(ValueError, "Colour-first alt mismatch"):
            attach(self.rows, media, self.urls)

    def test_active_import_fails(self):
        rows = copy.deepcopy(self.rows)
        rows[0]["Status"] = "active"
        with self.assertRaisesRegex(ValueError, "draft and unpublished"):
            attach(rows, self.media, self.urls)


if __name__ == "__main__":
    unittest.main()
