"""Fetch the five Substack RSS feeds and rebuild index.html.

Usage: python3 build.py            (fetch + build)
       python3 build.py --no-fetch (rebuild from posts.json)
"""
import datetime, email.utils, html, json, pathlib, re, sys, urllib.request
import xml.etree.ElementTree as ET

HERE = pathlib.Path(__file__).parent
FEEDS = {
    "newsletter.safe.ai": "AI Safety Newsletter",
    "thezvi.substack.com": "Don't Worry About the Vase",
    "blog.peterwildeford.com": "The Power Law",
    "onexerxes.substack.com": "AI Safety Papers",
    "www.hyperdimensional.co": "Hyperdimensional",
}
NO_SUMMARY = {"Don't Worry About the Vase", "Hyperdimensional"}  # their feed descriptions are fragments


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36",
    "Accept": "application/rss+xml, application/xml;q=0.9, */*;q=0.8",
}


def fetch():
    old = json.loads((HERE / "posts.json").read_text()) if (HERE / "posts.json").exists() else []
    posts, failed = [], []
    for host, name in FEEDS.items():
        try:
            req = urllib.request.Request(f"https://{host}/feed", headers=HEADERS)
            root = ET.fromstring(urllib.request.urlopen(req, timeout=30).read())
        except Exception as e:  # keep the last good posts for a feed that fails
            print(f"{name}: {e}; keeping previous posts")
            failed.append(name)
            posts += [p for p in old if p["source"] == name]
            continue
        for it in root.iter("item"):
            desc = re.sub("<[^>]+>", "", html.unescape(it.findtext("description") or "")).strip()
            if name in NO_SUMMARY or desc.startswith("Welcome to") or len(desc) < 15:
                desc = ""
            elif len(desc) > 170:
                desc = desc[:170].rsplit(" ", 1)[0] + "…"
            posts.append({
                "source": name,
                "title": (it.findtext("title") or "").strip(),
                "url": it.findtext("link"),
                "date": email.utils.parsedate_to_datetime(it.findtext("pubDate")).strftime("%Y-%m-%d"),
                "summary": desc,
            })
    posts.sort(key=lambda p: p["date"], reverse=True)
    (HERE / "posts.json").write_text(json.dumps(posts, indent=1, ensure_ascii=False))
    if len(failed) == len(FEEDS):
        sys.exit("every feed failed; posts.json left unchanged")


def build():
    posts = json.loads((HERE / "posts.json").read_text())
    data = json.dumps(posts, ensure_ascii=False).replace("</", "<\\/")
    out = (HERE / "template.html").read_text()
    out = out.replace("/*__POSTS__*/[]", data).replace("/*__UPDATED__*/", datetime.date.today().isoformat())
    page = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
            '<style>body{margin:0}[hidden]{display:none!important}</style>\n</head>\n<body>\n' + out + '\n</body>\n</html>\n')
    (HERE / "index.html").write_text(page)
    print(f"built index.html with {len(posts)} posts")


if __name__ == "__main__":
    if "--no-fetch" not in sys.argv:
        fetch()
    build()
