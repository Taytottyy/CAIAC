# CAIAC

**What's New in AI Safety**: a one-page feed of recent posts from five AI safety newsletters, grouped by month.

Open `index.html` in a browser, or serve the repo with GitHub Pages.

## Sources

- [AI Safety Newsletter](https://newsletter.safe.ai/) (Center for AI Safety). Its issues are marked ★ Notable.
- [Don't Worry About the Vase](https://thezvi.substack.com/) (Zvi Mowshowitz)
- [The Power Law](https://blog.peterwildeford.com/) (Peter Wildeford)
- [AI Safety Papers](https://onexerxes.substack.com/)
- [Hyperdimensional](https://www.hyperdimensional.co/) (Dean W. Ball)

## Refresh the feed

```bash
python3 build.py
```

This fetches each Substack's RSS feed, saves the result to `posts.json`, and rebuilds `index.html` from `template.html`. To rebuild without fetching, run `python3 build.py --no-fetch`.

A GitHub Action (`.github/workflows/refresh.yml`) does this every day at 13:00 UTC and commits the result. You can also run it by hand from the Actions tab.
