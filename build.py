#!/usr/bin/env python3
"""Generates the static pages. Edit CONFIG, then run: python3 build.py"""
import json, pathlib

CONFIG = {
    "site_name": "SnapKB",
    # Change to the live address once hosted, e.g. https://USERNAME.github.io/snapkb
    "site_url": "https://johncamil168-sys.github.io/snapkb",
    # Paste the Gumroad/Payhip product link here once the product is listed.
    "shop_url": "",
    "shop_text": "Printable Monthly Budget Planner (PDF) — plan every dollar in 10 minutes a month.",
    # Paste your AdSense client id (ca-pub-...) once approved. Empty = no ads.
    "adsense_client": "",
}

SIZES = {
    10: "very small upload limits, like some exam and job portals that cap signatures at 10 KB",
    20: "signature and thumb-impression uploads on government and exam forms",
    30: "signature uploads and small profile pictures",
    50: "passport-style photos on online application forms and visa portals",
    100: "photo uploads on job sites, school admissions and ID applications",
    150: "document scans and profile photos where 100 KB is too blurry",
    200: "scanned certificates and ID cards on application forms",
    500: "email attachments and website images that still need to look sharp",
    1024: "1 MB limits on chat apps, forums and online forms",
}

def kb_label(k): return "1 MB" if k == 1024 else f"{k} KB"
def slug(k): return "compress-image-to-1mb" if k == 1024 else f"compress-image-to-{k}kb"

def page(path, title, desc, h1, sub, default_kb, body_html, tool=True):
    c = CONFIG
    url = c["site_url"].rstrip("/") + ("/" if path == "index.html" else "/" + path)
    ads = (f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={c["adsense_client"]}" crossorigin="anonymous"></script>'
           if c["adsense_client"] else "")
    promo = (f'<div class="card promo"><strong>Free tool, paid by readers like you.</strong> '
             f'{c["shop_text"]} <a href="{c["shop_url"]}" rel="noopener">Get it here</a>.</div>'
             if c["shop_url"] else "")
    chips = "".join(f'<a href="{slug(k)}.html">{kb_label(k)}</a>' for k in SIZES)
    faq = [
        ("Are my photos uploaded anywhere?", "No. The compression runs inside your browser, so your image never leaves your device."),
        ("Why does my photo look smaller?", "If quality alone cannot reach the target size, the tool also shrinks the width and height a little. Pick a larger KB value for a sharper result."),
        ("Which formats work?", "You can open JPG, PNG, WEBP and most other image types. The result is saved as JPG (best for forms) or WEBP."),
    ]
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
    tool_html = f'''
<div class="card">
  <div class="drop" id="drop"><input type="file" id="file" accept="image/*">
    <strong>Click or drop a photo here</strong><br><span class="sub" id="picked">JPG, PNG or WEBP · stays on your device</span></div>
  <div class="row">
    <label>Target size (KB)<input type="number" id="kb" min="1" value="{default_kb}"></label>
    <label>Max width (px, optional)<input type="number" id="maxw" min="0" placeholder="any"></label>
    <label>Format<select id="fmt"><option value="image/jpeg">JPG</option><option value="image/webp">WEBP</option></select></label>
    <button id="go" disabled>Compress</button>
  </div>
  <div class="chips">{chips}</div>
</div>
<div class="card" id="result"><div class="stats" id="stats"></div><img id="out" alt="Compressed result"><a class="btn" id="dl">Download</a></div>
''' if tool else ""
    faq_html = "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in faq) if tool else ""
    html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{url}">
<link rel="stylesheet" href="style.css">{ads}
{'<script type="application/ld+json">'+json.dumps(ld)+'</script>' if tool else ''}
</head><body>
<header><a class="logo" href="index.html">{c["site_name"]}</a><nav><a href="index.html">Compress</a><a href="about.html">About</a></nav></header>
<main>
<h1>{h1}</h1><p class="sub">{sub}</p>
{tool_html}
{promo}
{body_html}
{('<h2>Questions</h2>' + faq_html) if tool else ''}
</main>
<footer><a href="about.html">About</a><a href="privacy.html">Privacy</a><span>© {c["site_name"]}</span></footer>
{'<script src="app.js"></script>' if tool else ''}
</body></html>'''
    pathlib.Path(path).write_text(html)
    return url

urls = []
urls.append(page("index.html",
    "Compress Image to Exact KB Online — Free, No Upload | SnapKB",
    "Shrink any photo to an exact size like 20 KB, 50 KB or 100 KB for online forms. Free, fast and private: your image never leaves your device.",
    "Compress a photo to an exact size in KB",
    "Pick a target size, drop your photo, download. Free, and your image never leaves your device.",
    100,
    "<h2>How it works</h2><p>Online forms often reject photos that are too big. SnapKB lowers the JPG quality step by step until your photo fits the size you choose, and only shrinks the dimensions if it has to. Everything runs in your browser, so it works even on slow connections once the page has loaded.</p>"
    "<h2>Popular sizes</h2><ul>" + "".join(f'<li><a href="{slug(k)}.html">Compress image to {kb_label(k)}</a> for {u}.</li>' for k, u in SIZES.items()) + "</ul>"))

for k, use in SIZES.items():
    lab = kb_label(k)
    urls.append(page(f"{slug(k)}.html",
        f"Compress Image to {lab} Online — Free & Private | SnapKB",
        f"Reduce a photo to {lab} or less in seconds. Ideal for {use}. Free, no sign-up, nothing is uploaded.",
        f"Compress image to {lab}",
        f"Get your photo under {lab} for {use}. Free, and nothing is uploaded.",
        k,
        f"<h2>Tips for a sharp {lab} photo</h2><ul>"
        f"<li>Crop away empty background first so more of the {lab} goes to your face or document.</li>"
        f"<li>If the form also asks for a size in pixels, enter that width in <em>Max width</em>.</li>"
        f"<li>JPG is accepted almost everywhere. Only pick WEBP if the site says it accepts it.</li></ul>"))

page("about.html", "About SnapKB", "What SnapKB is and who runs it.", "About SnapKB",
     "A small, free tool for people stuck on photo size limits.", 0,
     "<p>SnapKB was built to solve one annoying problem: online forms rejecting photos because they are too big. "
     "It compresses images to an exact size in KB, right in your browser, without uploading anything.</p>"
     "<p>The site is kept free by small ads and by optional printable products. Questions or ideas? Contact the owner through the shop page.</p>", tool=False)
page("privacy.html", "Privacy Policy — SnapKB", "SnapKB privacy policy.", "Privacy policy", "Short version: your images never leave your device.", 0,
     "<p>Images you open in SnapKB are processed entirely inside your web browser. They are never uploaded to any server.</p>"
     "<p>This site may show ads from Google AdSense. Google and its partners may use cookies to show ads based on your visits to this and other sites. "
     "You can opt out of personalised advertising at <a href=\"https://www.google.com/settings/ads\">Google Ads Settings</a>.</p>"
     "<p>The site host may keep standard server logs (such as IP address and pages visited) for security.</p>", tool=False)

base = CONFIG["site_url"].rstrip("/")
pathlib.Path("sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n")
pathlib.Path("robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n")
print(f"Built {len(urls)} tool pages + about + privacy")
