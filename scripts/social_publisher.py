#!/usr/bin/env python3
"""
Tea & Toast Social Media Automation Engine
------------------------------------------
Generates, formats, and publishes content across:
- X (Twitter): @teaandtoastblog (https://x.com/teaandtoastblog)
- Facebook: Tea and Toast Page (https://www.facebook.com/profile.php?id=100063631472993)
- Instagram: @teaandtoastblog (https://www.instagram.com/teaandtoastblog/)

Usage:
  python scripts/social_publisher.py --list
  python scripts/social_publisher.py --recipe sourdough-avocado-chili-crunch-toast
  python scripts/social_publisher.py --all --export social_calendar.json
  python scripts/social_publisher.py --recipe sourdough-avocado-chili-crunch-toast --post-x
  python scripts/social_publisher.py --recipe sourdough-avocado-chili-crunch-toast --post-fb
"""

import os
import sys
import json
import glob
import re
import argparse
import urllib.request
import urllib.parse

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RECIPES_DIR = os.path.join(BASE_DIR, "src", "content", "recipes")
SITE_URL = "https://teaandtoastblog.pages.dev"

def parse_frontmatter(file_path):
    """Extract YAML frontmatter and markdown body from recipe file."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not match:
        return {}, content

    yaml_text = match.group(1)
    body = match.group(2)

    data = {}
    current_key = None

    for raw_line in yaml_text.splitlines():
        if not raw_line or raw_line.strip().startswith("#"):
            continue

        # Only process top-level keys (no leading spaces)
        if not raw_line.startswith(" ") and not raw_line.startswith("\t") and ":" in raw_line:
            key, val = raw_line.split(":", 1)
            key = key.strip()
            val = val.strip()
            val = re.sub(r'^["\']|["\']$', '', val)

            if val.startswith("[") or val.startswith("{"):
                try:
                    val = json.loads(val)
                except Exception:
                    pass
            elif val.lower() == "true":
                val = True
            elif val.lower() == "false":
                val = False

            data[key] = val

    slug = os.path.splitext(os.path.basename(file_path))[0]
    data["slug"] = slug
    return data, body

def get_all_recipes():
    recipes = []
    files = glob.glob(os.path.join(RECIPES_DIR, "*.md"))
    for f in sorted(files):
        data, _ = parse_frontmatter(f)
        if data.get("title"):
            recipes.append(data)
    return recipes

def format_social_package(recipe):
    title = recipe.get("title", "Artisanal Recipe")
    desc = recipe.get("description", "")
    time = recipe.get("totalTime", "15 mins")
    slug = recipe.get("slug", "")
    url = f"{SITE_URL}/recipes/{slug}"
    image = recipe.get("heroImage", "")
    tea = recipe.get("teaPairing", {}).get("teaName", "Earl Grey Tea") if isinstance(recipe.get("teaPairing"), dict) else "Earl Grey Tea"

    # 1. X (Twitter) - Punchy, high-engagement hook (Twitter counts any URL as 23 chars)
    x_post = (
        f"🍞 {title}\n\n"
        f"{desc[:90]}...\n\n"
        f"⏱️ {time} • 🍵 {tea}\n"
        f"👉 Recipe: {url}\n\n"
        f"#teaandtoast #recipes"
    )

    # 2. Facebook Post - Engaging, community question hook
    fb_post = (
        f"Weekend breakfast inspiration! 🍞✨\n\n"
        f"{title}\n\n"
        f"{desc}\n\n"
        f"What makes this recipe special:\n"
        f"• Ready in just {time}\n"
        f"• Best paired with a freshly steeped cup of {tea}\n"
        f"• Perfect balance of crispy crust and velvety richness\n\n"
        f"Get the complete printable recipe card with exact measurements & tips below:\n"
        f"{url}\n\n"
        f"Let us know in the comments: What is your all-time favorite toast topping? 👇"
    )

    # 3. Instagram / Reel Caption
    ig_caption = (
        f"Elevate your morning slice. 🍞✨\n\n"
        f"{title.upper()}\n\n"
        f"{desc}\n\n"
        f"▫️ Prep & cook: {time}\n"
        f"▫️ Ideal sip: {tea}\n"
        f"▫️ Sourdough crunch level: 10/10\n\n"
        f"Save this post for your weekend brunch! 📌\n"
        f"Full measurements, printable recipe card & pairing guide at the link in our bio 👉 @teaandtoastblog\n"
        f".\n.\n.\n"
        f"#teaandtoast #toastrecipes #sourdoughlove #breakfastideas #brunchgoals #toasttuesday #foodreels #morningritual #cozyvibes #teatime"
    )

    return {
        "slug": slug,
        "title": title,
        "url": url,
        "image": image,
        "x_post": x_post,
        "x_char_count": len(x_post),
        "facebook_post": fb_post,
        "instagram_caption": ig_caption,
    }

def post_to_x(text):
    """Post to X (Twitter API v2) if credentials are provided."""
    bearer_token = os.environ.get("X_BEARER_TOKEN")
    if not bearer_token:
        print("⚠️ X_BEARER_TOKEN environment variable not set.")
        print("   Direct web link to post manually:")
        print(f"   https://twitter.com/intent/tweet?text={urllib.parse.quote(text)}")
        return False

    url = "https://api.twitter.com/2/tweets"
    payload = json.dumps({"text": text}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            res_data = json.loads(resp.read().decode("utf-8"))
            print(f"✅ Successfully posted to X! ID: {res_data.get('data', {}).get('id')}")
            return True
    except Exception as e:
        print(f"❌ Error posting to X: {e}")
        return False

def post_to_facebook(text, link):
    """Post to Facebook Page feed if Page Access Token is provided."""
    page_id = os.environ.get("FB_PAGE_ID", "100063631472993")
    token = os.environ.get("FB_PAGE_ACCESS_TOKEN")
    if not token:
        print("⚠️ FB_PAGE_ACCESS_TOKEN environment variable not set.")
        print("   Direct web link to share on Facebook:")
        print(f"   https://www.facebook.com/sharer/sharer.php?u={urllib.parse.quote(link)}")
        return False

    url = f"https://graph.facebook.com/v19.0/{page_id}/feed"
    params = urllib.parse.urlencode({"message": text, "link": link, "access_token": token}).encode("utf-8")
    req = urllib.request.Request(url, data=params, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            res_data = json.loads(resp.read().decode("utf-8"))
            print(f"✅ Successfully posted to Facebook! ID: {res_data.get('id')}")
            return True
    except Exception as e:
        print(f"❌ Error posting to Facebook: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Tea & Toast Social Media Automation Engine")
    parser.add_argument("--list", action="store_true", help="List all available recipes")
    parser.add_argument("--recipe", type=str, help="Recipe slug (e.g. sourdough-avocado-chili-crunch-toast)")
    parser.add_argument("--all", action="store_true", help="Process all recipes")
    parser.add_argument("--export", type=str, help="Export all formatted posts to a JSON file")
    parser.add_argument("--post-x", action="store_true", help="Publish directly to X (Twitter)")
    parser.add_argument("--post-fb", action="store_true", help="Publish directly to Facebook Page")

    args = parser.parse_args()
    recipes = get_all_recipes()

    if args.list:
        print(f"\n🍞 Found {len(recipes)} recipes in vault:")
        for r in recipes:
            print(f"  • {r.get('slug'):<50} | {r.get('title')}")
        print("\nUse --recipe <slug> to format social posts.")
        return

    if args.all or args.export:
        packages = [format_social_package(r) for r in recipes]
        if args.export:
            with open(args.export, "w", encoding="utf-8") as f:
                json.dump(packages, f, indent=2)
            print(f"✅ Exported {len(packages)} social post packages to: {args.export}")
        else:
            print(f"Formatted {len(packages)} recipe social packages.")
        return

    # Single recipe processing
    target_slug = args.recipe or (recipes[0].get("slug") if recipes else None)
    if not target_slug:
        print("❌ No recipes found.")
        return

    matched = [r for r in recipes if r.get("slug") == target_slug]
    if not matched:
        print(f"❌ Recipe slug '{target_slug}' not found. Run with --list to view options.")
        return

    pkg = format_social_package(matched[0])

    print("\n" + "=" * 60)
    print(f"  🍞 SOCIAL MEDIA DISTRIBUTION PACKAGE: {pkg['title']}")
    print("=" * 60)

    print("\n--- 1. X (TWITTER) POST (Chars: " + str(pkg["x_char_count"]) + "/280) ---")
    print(pkg["x_post"])

    print("\n--- 2. FACEBOOK PAGE POST ---")
    print(pkg["facebook_post"])

    print("\n--- 3. INSTAGRAM REEL / POST CAPTION ---")
    print(pkg["instagram_caption"])

    print("\n" + "-" * 60)
    print("⚡ Instant Web Share Links:")
    print("  X Tweet:    https://twitter.com/intent/tweet?text=" + urllib.parse.quote(pkg["x_post"]))
    print("  Facebook:   https://www.facebook.com/sharer/sharer.php?u=" + urllib.parse.quote(pkg["url"]))
    print("  Instagram:  https://www.instagram.com/teaandtoastblog/")
    print("=" * 60 + "\n")

    if args.post_x:
        post_to_x(pkg["x_post"])

    if args.post_fb:
        post_to_facebook(pkg["facebook_post"], pkg["url"])

if __name__ == "__main__":
    main()
