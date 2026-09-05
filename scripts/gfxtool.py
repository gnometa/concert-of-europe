#!/usr/bin/env python3
"""Graphics helper for the CoE_RoI_R Victoria 2 mod.

Finds free-to-use, Victorian-era (1820-1914) pictures on Wikimedia Commons,
converts them into the exact formats the game expects, and records the
attribution in CoE_RoI_R/gfx/CREDITS.md.

Subcommands
  missing                         list pictures referenced by events/decisions/news
                                  that exist neither in the mod nor in the game folder
  search <query> [--limit N] [--any-era]
                                  search Commons; keeps only PD/CC0/CC-BY/CC-BY-SA files
                                  dated 1820-1914 (or undated engravings/paintings that
                                  mention a year in range)
  fetch <File:Name> --kind KIND --name NAME [--no-filter] [--crop TOP|CENTER|BOTTOM]
                                  download, resize/crop, apply the Victorian filter and
                                  write gfx/pictures/<kind>/NAME.<ext>; appends credits
  convert <image> --kind KIND --name NAME [--no-filter] [--crop ...]
                                  same as fetch but from a local file (no credit entry)
  filter <in> <out>               apply only the Victorian filter (debug / preview)
  preview <game-image> <out.png>  decode a .tga/.dds from the mod for viewing

KIND sets size and format (taken from what the mod ships today):
  event     521x203  TGA 32-bit   gfx/pictures/events/
  decision   95x95   DDS uncompressed  gfx/pictures/decisions/
  news      521x203  DDS uncompressed  gfx/pictures/news/
  masthead  714x104  DDS uncompressed  gfx/pictures/news/   (newspaper titles)
  loading  1024x1024 DDS uncompressed  gfx/loadingscreens/
  tech      (same as event)  gfx/pictures/tech/

Requires Pillow (python -m pip install Pillow). Network access only for search/fetch.
"""
import io
import json
import os
import re
import sys
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOD = os.path.join(ROOT, "CoE_RoI_R")
GAME = r"D:\Steam\steamapps\common\Victoria 2"
CREDITS = os.path.join(MOD, "gfx", "CREDITS.md")
UA = "CoE-RoI-R-mod-gfxtool/1.0 (https://github.com/; genta@csrejeki.com)"
API = "https://commons.wikimedia.org/w/api.php"

ERA = (1820, 1914)
OK_LICENSES = ("public domain", "pd", "cc0", "cc by", "cc-by", "no restrictions")
BAD_LICENSES = ("nc", "nd", "fair use", "non-free")

KINDS = {
    "event":    ((521, 203), "tga", os.path.join("gfx", "pictures", "events")),
    "tech":     ((521, 203), "tga", os.path.join("gfx", "pictures", "tech")),
    "decision": ((95, 95),   "dds", os.path.join("gfx", "pictures", "decisions")),
    "news":     ((521, 203), "dds", os.path.join("gfx", "pictures", "news")),
    "masthead": ((714, 104), "dds", os.path.join("gfx", "pictures", "news")),
    "loading":  ((1024, 1024), "dds", os.path.join("gfx", "loadingscreens")),
}


# ---------------------------------------------------------------- helpers

def die(msg, code=1):
    print(msg, file=sys.stderr)
    sys.exit(code)


def pil():
    try:
        from PIL import Image, ImageEnhance, ImageOps, ImageFilter  # noqa
        return Image, ImageEnhance, ImageOps, ImageFilter
    except ImportError:
        die("Pillow is missing: python -m pip install Pillow")


def http_get(url, params=None):
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def api(params):
    params = dict(params, format="json")
    return json.loads(http_get(API, params).decode("utf-8"))


def strip_html(s):
    s = re.sub(r"<[^>]+>", "", s or "")
    s = re.sub(r"date QS:.*", "", s)                  # Wikidata date qualifiers
    s = re.sub(r"Unknown author\s*Unknown author", "Unknown author", s)
    return s.strip()


def years_in(text):
    return [int(y) for y in re.findall(r"\b(1[5-9]\d\d|20\d\d)\b", text or "")]


def license_ok(short, usage_terms):
    s = (short or "").lower() + " " + (usage_terms or "").lower()
    if any(b in s for b in BAD_LICENSES):
        return False
    return any(g in s for g in OK_LICENSES)


def era_ok(meta):
    """True when the picture itself is from 1820-1914."""
    for key in ("DateTimeOriginal", "DateTime"):
        ys = years_in(strip_html(meta.get(key, {}).get("value")))
        if ys:
            return any(ERA[0] <= y <= ERA[1] for y in ys)
    # undated: accept if the description names a year in range
    ys = years_in(strip_html(meta.get("ImageDescription", {}).get("value")))
    return any(ERA[0] <= y <= ERA[1] for y in ys)


def imageinfo(titles):
    out = {}
    for i in range(0, len(titles), 20):
        chunk = titles[i:i + 20]
        data = api({
            "action": "query", "titles": "|".join(chunk), "prop": "imageinfo",
            "iiprop": "url|size|extmetadata|mime",
            "iiextmetadatafilter": "LicenseShortName|UsageTerms|Artist|Credit|"
                                   "DateTimeOriginal|DateTime|ImageDescription|Attribution|LicenseUrl",
        })
        for page in data.get("query", {}).get("pages", {}).values():
            ii = page.get("imageinfo")
            if ii:
                out[page["title"]] = ii[0]
    return out


def describe(title, ii):
    m = ii.get("extmetadata", {})
    g = lambda k: strip_html(m.get(k, {}).get("value"))
    return {
        "title": title,
        "url": ii.get("url"),
        "page": "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_")),
        "size": "%sx%s" % (ii.get("width"), ii.get("height")),
        "license": g("LicenseShortName") or g("UsageTerms"),
        "license_url": g("LicenseUrl"),
        "artist": g("Artist"),
        "date": g("DateTimeOriginal") or g("DateTime"),
        "desc": g("ImageDescription")[:160],
        "license_ok": license_ok(g("LicenseShortName"), g("UsageTerms")),
        "era_ok": era_ok(m),
    }


# ---------------------------------------------------------------- image work

def victorian(img):
    """Sepia tone, softened contrast, slight vignette, faint grain: makes photos,
    paintings and engravings from different sources sit together in the event window."""
    Image, ImageEnhance, ImageOps, ImageFilter = pil()
    img = img.convert("RGB")
    grey = ImageOps.grayscale(img)
    grey = ImageOps.autocontrast(grey, cutoff=1)
    sepia = ImageOps.colorize(grey, black=(28, 18, 10), mid=(142, 110, 72), white=(240, 226, 196))
    # keep a little of the original colour so paintings do not go fully monochrome
    out = Image.blend(sepia, img, 0.22)
    out = ImageEnhance.Contrast(out).enhance(1.08)
    out = ImageEnhance.Sharpness(out).enhance(0.9)
    # vignette
    w, h = out.size
    mask = Image.radial_gradient("L").resize((w, h))
    mask = ImageOps.invert(mask).point(lambda v: 255 - int((255 - v) * 0.45))
    dark = Image.new("RGB", (w, h), (20, 12, 6))
    out = Image.composite(out, dark, mask)
    # grain
    import random
    rnd = random.Random(1837)
    noise = Image.effect_noise((w, h), 14).convert("L")
    noise = noise.point(lambda v: 128 + (v - 128) // 3)
    out = Image.merge("RGB", [
        Image.eval(Image.blend(c, noise, 0.10), lambda v: min(255, max(0, v)))
        for c in out.split()
    ])
    return out


def fit(img, size, crop="CENTER"):
    Image, ImageEnhance, ImageOps, ImageFilter = pil()
    pos = {"TOP": (0.5, 0.0), "CENTER": (0.5, 0.5), "BOTTOM": (0.5, 1.0)}[crop.upper()]
    return ImageOps.fit(img.convert("RGB"), size, method=Image.LANCZOS, centering=pos)


def save_game(img, path, ext):
    Image, ImageEnhance, ImageOps, ImageFilter = pil()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if ext == "tga":
        img.convert("RGBA").save(path, "TGA")            # uncompressed 32-bit, like the mod's events
    elif ext == "dds":
        img.convert("RGBA").save(path, "DDS")            # uncompressed RGBA, like vanilla decisions/news
    else:
        die("unknown ext " + ext)


def load_any(path_or_bytes):
    Image, ImageEnhance, ImageOps, ImageFilter = pil()
    if isinstance(path_or_bytes, bytes):
        return Image.open(io.BytesIO(path_or_bytes))
    return Image.open(path_or_bytes)


def make(img, kind, name, use_filter=True, crop="CENTER"):
    size, ext, sub = KINDS[kind]
    out = fit(img, size, crop)
    if use_filter:
        out = victorian(out)
    dest = os.path.join(MOD, sub, "%s.%s" % (name, ext))
    save_game(out, dest, ext)
    return dest


def add_credit(dest, info):
    header = "# Picture credits\n\nImages fetched with `scripts/gfxtool.py fetch` from Wikimedia Commons. All are public domain or CC-licensed; keep this file when redistributing the mod.\n\n| File | Source | Author | Date | Licence |\n|---|---|---|---|---|\n"
    line = "| `%s` | [%s](%s) | %s | %s | %s |\n" % (
        os.path.relpath(dest, MOD).replace("\\", "/"), info["title"], info["page"],
        info["artist"] or "unknown", info["date"] or "undated", info["license"] or "?")
    if os.path.exists(CREDITS):
        with open(CREDITS, "r", encoding="utf-8") as f:
            body = f.read()
    else:
        body = header
    if line not in body:
        body = body.rstrip("\n") + "\n" + line
    with open(CREDITS, "w", encoding="utf-8", newline="\n") as f:
        f.write(body)


# ---------------------------------------------------------------- commands

def cmd_missing():
    pic = re.compile(r'picture\s*=\s*"?([A-Za-z0-9_./\\-]+)')
    refs = {"event": set(), "decision": set(), "news": set()}
    for folder, kind in (("events", "event"), ("decisions", "decision"), ("news", "news")):
        d = os.path.join(MOD, folder)
        for fn in os.listdir(d):
            if not fn.lower().endswith(".txt"):
                continue
            text = open(os.path.join(d, fn), "r", encoding="cp1252", errors="replace").read()
            for line in text.splitlines():
                line = line.split("#", 1)[0]
                for m in pic.finditer(line):
                    k = kind
                    if kind == "decision" and re.search(r"\b(country|province)_event\b", text):
                        k = "event" if "SetupGVG" in fn else kind
                    refs[k].add((m.group(1), fn))
    problems = 0
    def exists(rel):
        return os.path.exists(os.path.join(MOD, rel)) or os.path.exists(os.path.join(GAME, rel))
    for name, fn in sorted(refs["event"]):
        if not exists(os.path.join("gfx", "pictures", "events", name + ".tga")) and \
           not exists(os.path.join("gfx", "pictures", "events", name + ".dds")):
            print("missing event picture  gfx/pictures/events/%s.tga  (events/%s)" % (name, fn)); problems += 1
    for name, fn in sorted(refs["decision"]):
        if not exists(os.path.join("gfx", "pictures", "decisions", name + ".dds")) and \
           not exists(os.path.join("gfx", "pictures", "decisions", name + ".tga")):
            print("missing decision picture  gfx/pictures/decisions/%s.dds  (decisions/%s)" % (name, fn)); problems += 1
    for name, fn in sorted(refs["news"]):
        if name.endswith("/"):
            continue
        if not exists(os.path.join("gfx", "pictures", name)):
            print("missing news picture  gfx/pictures/%s  (news/%s)" % (name, fn)); problems += 1
    return 1 if problems else 0


def cmd_search(query, limit=10, any_era=False):
    data = api({"action": "query", "list": "search", "srnamespace": 6, "srlimit": min(limit * 4, 50),
                "srsearch": query + " filetype:bitmap"})
    titles = [r["title"] for r in data.get("query", {}).get("search", [])]
    if not titles:
        print("no results"); return 1
    infos = imageinfo(titles)
    shown = 0
    for t in titles:
        if t not in infos:
            continue
        d = describe(t, infos[t])
        if not d["license_ok"]:
            continue
        if not any_era and not d["era_ok"]:
            continue
        shown += 1
        print("%s\n    %s | %s | %s | %s\n    %s\n    %s" % (
            d["title"], d["size"], d["license"], d["date"] or "undated", d["artist"] or "unknown artist",
            d["desc"], d["page"]))
        if shown >= limit:
            break
    if not shown:
        print("no results passed the licence/era filter (try --any-era or another query)")
        return 1
    return 0


def cmd_fetch(title, kind, name, use_filter=True, crop="CENTER", force=False):
    if kind not in KINDS:
        die("kind must be one of " + ", ".join(KINDS))
    if not title.startswith("File:"):
        title = "File:" + title
    infos = imageinfo([title])
    if title not in infos:
        die("not found on Commons: " + title)
    d = describe(title, infos[title])
    if not d["license_ok"] and not force:
        die("licence not in the allowed set (%s); use --force only if you have checked it yourself" % d["license"])
    if not d["era_ok"] and not force:
        die("not dated 1820-1914 (%s); use --force to accept it anyway" % (d["date"] or "undated"))
    size, ext, sub = KINDS[kind]
    w = max(size[0] * 2, 1200)
    thumb = api({"action": "query", "titles": title, "prop": "imageinfo", "iiprop": "url", "iiurlwidth": w})
    page = next(iter(thumb["query"]["pages"].values()))
    url = page["imageinfo"][0].get("thumburl") or d["url"]
    img = load_any(http_get(url))
    dest = make(img, kind, name, use_filter, crop)
    add_credit(dest, d)
    print("wrote %s  (%s, %s, %s)" % (os.path.relpath(dest, ROOT), d["license"], d["date"] or "undated", d["artist"] or "unknown"))
    return 0


def cmd_convert(src, kind, name, use_filter=True, crop="CENTER"):
    if kind not in KINDS:
        die("kind must be one of " + ", ".join(KINDS))
    dest = make(load_any(src), kind, name, use_filter, crop)
    print("wrote " + os.path.relpath(dest, ROOT))
    return 0


def cmd_filter(src, dst):
    victorian(load_any(src)).save(dst)
    print("wrote " + dst)
    return 0


def cmd_preview(src, dst):
    load_any(src).convert("RGB").save(dst)
    print("wrote " + dst)
    return 0


def main(argv):
    try:
        sys.stdout.reconfigure(errors="replace")
    except Exception:
        pass
    if not argv:
        print(__doc__.strip()); return 0
    cmd, args = argv[0], argv[1:]
    opts = {a.split("=", 1)[0]: (a.split("=", 1)[1] if "=" in a else True) for a in args if a.startswith("--")}
    pos = [a for a in args if not a.startswith("--")]
    # allow "--kind event" as well as "--kind=event"
    i = 0
    while i < len(args):
        if args[i].startswith("--") and "=" not in args[i] and i + 1 < len(args) and not args[i + 1].startswith("--") \
           and args[i] in ("--kind", "--name", "--crop", "--limit"):
            opts[args[i]] = args[i + 1]
            pos.remove(args[i + 1])
            i += 1
        i += 1
    if cmd == "missing":
        return cmd_missing()
    if cmd == "search":
        return cmd_search(" ".join(pos), int(opts.get("--limit", 10)), "--any-era" in opts)
    if cmd == "fetch":
        return cmd_fetch(pos[0], opts.get("--kind"), opts.get("--name"), "--no-filter" not in opts,
                         opts.get("--crop", "CENTER"), "--force" in opts)
    if cmd == "convert":
        return cmd_convert(pos[0], opts.get("--kind"), opts.get("--name"), "--no-filter" not in opts,
                           opts.get("--crop", "CENTER"))
    if cmd == "filter":
        return cmd_filter(pos[0], pos[1])
    if cmd == "preview":
        return cmd_preview(pos[0], pos[1])
    die("unknown subcommand " + cmd)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
