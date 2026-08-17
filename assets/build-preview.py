import re

ROOT = r"D:\projects\shopify"
DEFAULTS = {
    "eyebrow": "ORIGINAL 3D HERO MERCH AGES 4-9", "heading_prefix": "Stories they love,",
    "heading_cursive": "Heroes", "heading_suffix": "they can hold.",
    "subheading": "Replace screen-time with handcrafted plushies, organic story apparel, and hardbound bedtime adventures built with world-class craft.",
    "primary_cta_text": "Shop the Squad", "secondary_cta_text": "Explore Storybooks",
    "description": "Tactile craft, premium organic fabrics, and screen-free physical storytelling.",
    "accessible_label": "Store highlights", "padding_top": 36, "padding_bottom": 48,
}

def section_html(fpath, section_id, extra=None):
    src = open(f"{ROOT}\\sections\\{fpath}", encoding="utf-8").read()
    style = re.search(r"\{%-?\s*style\s*-?%\}(.*?)\{%-?\s*endstyle\s*-?%\}", src, re.S).group(1)
    rest = src.split("{%- endstyle -%}", 1)[1]
    body = rest.split("<script>")[0]
    m = re.search(r"<script>(.*?)</script>", rest, re.S)
    script = "<script>" + m.group(1) + "</script>" if m else ""
    def rs(s):
        defaults = dict(DEFAULTS)
        if extra:
            defaults.update(extra)
        s = re.sub(r"\{\{\s*'[^']+'\s*\|\s*asset_url\s*\|\s*stylesheet_tag\s*\}\}", "", s)
        s = re.sub(r"\{\{\s*'([^']+)'\s*\|\s*asset_url\s*\}\}", r"\1", s)
        s = s.replace("{{ routes.collections_url }}", "#")
        s = s.replace("{{ section.id }}", section_id)
        s = s.replace("{{ reveal }}", "")
        s = re.sub(r'\{\{\s*section\.settings\.[a-z_]+\s*\|\s*default:\s*"([^"]*)"\s*\}\}', r"\1", s)
        s = re.sub(r"\{\{\s*section\.settings\.[a-z_]+\s*\|\s*default:\s*'([^']*)'\s*\}\}", r"\1", s)
        s = re.sub(r"\{\{\s*section\.settings\.(padding_top|padding_bottom)\s*\|\s*times[^}]*\}\}",
                   lambda mm: str(int(float(defaults.get(mm.group(1), 36)) * 0.75)), s)
        s = re.sub(r"\{\{\s*section\.settings\.[a-z_]+\s*\}\}",
                   lambda mm: str(defaults.get(re.search(r"settings\.([a-z_]+)", mm.group(0)).group(1), "")), s)
        s = re.sub(r"\{%-?\s*if [^%]*?-%\}", "", s)
        s = re.sub(r"\{%-?\s*endif\s*-?%\}", "", s)
        s = re.sub(r"\{%-?\s*liquid.*?-?%\}", "", s, flags=re.S)
        return s
    return "<style>" + rs(style) + "</style>\n" + rs(body) + "\n" + rs(script)

items = "SCREEN-FREE PLAY | 100% ORGANIC COTTON | BIS & EN71 CERTIFIED | 30-DAY HAPPINESS PROMISE | FREE SHIPPING OVER 999 | BEDTIME STORIES THAT BUILD CHARACTER".split("|")
star = '<svg class="jjw-marquee__star" viewBox="0 0 24 24" fill="#FFD93D" aria-hidden="true" focusable="false"><path d="M12 2l2.4 6.2 6.6.4-5.1 4.2 1.7 6.4L12 15.9 6.4 19.2l1.7-6.4L3 8.6l6.6-.4L12 2z"/></svg>'
track_items = "".join('<span class="jjw-marquee__item">' + it.strip() + " " + star + "</span>" for it in items for _ in range(2))
marquee = ('<style>#JJWMarquee-prev { padding: 20px 0; isolation: isolate; overflow: hidden; }</style>\n'
           '<section id="JJWMarquee-prev"><div class="jjw-marquee" role="marquee" aria-label="Store highlights">'
           '<div class="jjw-marquee__track" data-jjw-marquee-track>' + track_items + '</div></div></section>\n'
           '<script>(function() { var track = document.querySelector("#JJWMarquee-prev [data-jjw-marquee-track]"); if (!track) return; '
           'var guard = 0; while (track.scrollWidth < window.innerWidth * 2.4 && guard < 4) { track.innerHTML += track.innerHTML; guard++; } })();</script>')

BLOB = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>'
        '<clipPath id="jjw-blob" clipPathUnits="objectBoundingBox"><path d="M276.099 61.423L10.521 64.37C4.734 64.434 0 60.582 0 55.807V8.56508C0 3.78408 4.74299 -0.0710076 10.537 0.000992371L276.115 3.27602C281.787 3.34602 286.341 7.15898 286.341 11.84V52.859C286.341 57.544 281.778 61.359 276.099 61.423Z" transform="scale(0.0034843206,0.015384615)" /></clipPath></defs></svg>')

parts = [
    section_html("jjw-hero-squad.liquid", "hero"),
    marquee,
    section_html("jjw-featured-categories.liquid", "cats", {"eyebrow": "THE JJW SHOP", "heading_prefix": "All the", "heading_cursive": "Cuddles", "heading_suffix": "None of the Screen-Time."}),
    section_html("jjw-meet-heroes.liquid", "heroes", {"eyebrow": "THE JJW UNIVERSE", "heading_prefix": "Meet the Five", "heading_cursive": "Heroes", "heading_suffix": "of JJW", "padding_top": 48, "padding_bottom": 48}),
    section_html("jjw-parent-trust.liquid", "trust", {"eyebrow": "PARENTOLOGY BY JJW", "heading_prefix": "Made for Play.", "heading_cursive": "Trusted", "heading_suffix": "by Parents.", "padding_top": 48, "padding_bottom": 48}),
]

html = ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
        '<title>JJW Store Preview</title><link rel="stylesheet" href="base.css"><link rel="stylesheet" href="jevikajoy-theme.css"></head>'
        '<body style="margin:0;">' + BLOB + "".join(parts) + '</body></html>')

open(f"{ROOT}\\assets\\_preview.html", "w", encoding="utf-8").write(html)
print("preview written:", len(html))
