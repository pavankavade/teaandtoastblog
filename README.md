# 🍞🍵 Tea & Toast (@teaandtoastblog)

> Elevating morning slices and afternoon teatime rituals with artisanal sourdough, whipped spreads, comforting bakes, and mindful tea pairings.

Official web home for the [@teaandtoastblog](https://www.instagram.com/teaandtoastblog/) community. Built with **Astro 5**, **Tailwind CSS**, and **Recipe Schema (JSON-LD)** for maximum SEO, instant page loads (100 Core Web Vitals), and turnkey Google AdSense monetization.

---

## ⚡ Key Features

- **Blazing Fast Static Performance**: Zero client-side JavaScript overhead by default; instant page transitions.
- **Google Recipe Rich Snippets**: Automatic `Schema.org/Recipe` JSON-LD generation with cooking times, prep times, calories, servings, ingredients, and step-by-step instructions for Google Search rich cards.
- **Interactive Kitchen Features**:
  - **Dynamic Serving Scaler**: Recalculates ingredient quantities on the fly (1x, 2x, 3x).
  - **Interactive Prep Checklist**: Check off ingredients as you prepare them.
  - **Print & Cook Mode**: Clean, ad-free, high-contrast printable recipe card sheets (`window.print()` friendly).
  - **Tea & Toast Pairing Assistant**: Interactive sommelier widget matching breads and toppings to their ideal loose-leaf or herbal brew.
- **Social Media & Video Flywheel**:
  - **Native Video / Reel Embeds**: Supports Instagram Reels, YouTube Shorts, and MP4 videos directly in recipe headers.
  - **Monetized Link-in-Bio Hub (`/links`)**: Directs Instagram/TikTok traffic to your own ad-monetized website rather than third-party Linktree.
- **Google AdSense Ready**:
  - Pre-configured responsive ad slots (Leaderboard, In-Article, Sidebar).
  - Complete legal & trust compliance pages (`/about`, `/contact`, `/privacy-policy`, `/terms`, `/disclaimer`).
- **Automated AI Recipe Pipeline**:
  - Built-in Python CLI generator (`scripts/generate_recipe.py`) to turn Instagram captions or prompts into schema-compliant MDX posts.

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
npm install
```

### 2. Run Local Development Server
```bash
npm run dev
```
Visit `http://localhost:4321` in your browser.

### 3. Build for Production
```bash
npm run build
```
Static production files are generated into the `dist/` directory.

---

## ☁️ Deploying to Cloudflare Pages

1. Push your repository to GitHub: `https://github.com/pavankavade/teaandtoastblog`
2. Log in to the [Cloudflare Dashboard](https://dash.cloudflare.com/) and navigate to **Workers & Pages** → **Create application** → **Pages** → **Connect to Git**.
3. Select your `teaandtoastblog` repository.
4. Configure the build settings:
   - **Framework preset**: `Astro`
   - **Build command**: `npm run build`
   - **Build output directory**: `dist`
   - **Node.js Version** (under Environment variables): `NODE_VERSION` = `20` (or `22`)
5. Click **Save and Deploy**. Cloudflare will build and deploy your site globally on their edge network in under 60 seconds!
6. (Optional) In Cloudflare Pages, add your custom domain (e.g., `teaandtoast.online` or `teaandtoastblog.com`) under **Custom domains**.

---

## 💰 Enabling Google AdSense

Once your domain is registered and ready for AdSense:
1. In `src/layouts/BaseLayout.astro`, pass your AdSense Publisher ID to `adSenseClientId` (e.g. `ca-pub-XXXXXXXXXXXXXXXX`).
2. In `src/components/AdSlot.astro`, set your default `adClientId` and slot IDs.
3. Submit your domain in the Google AdSense dashboard under **Sites** → **Add Site**.

---

## 🤖 Generating New Recipes with AI

Run the CLI script to draft new recipes:
```bash
python scripts/generate_recipe.py --title "Whipped Ricotta and Hot Honey Toast" --category "Toasts & Spreads"
```
New recipes are saved directly into `src/content/recipes/`.
