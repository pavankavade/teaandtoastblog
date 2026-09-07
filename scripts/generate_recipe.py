#!/usr/bin/env python3
"""
Tea & Toast AI Recipe Generator Pipeline
-----------------------------------------
Automates the creation of high-ranking, SEO-optimized, schema-compliant
recipe MDX files for the Tea & Toast food blog.

Usage:
  python scripts/generate_recipe.py --title "Whipped Ricotta and Roasted Fig Toast" --category "Toasts & Spreads"
"""

import os
import sys
import json
import re
import argparse
from datetime import datetime

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    return re.sub(r'[\s-]+', '-', text).strip('-')

RECIPE_TEMPLATES = {
    "whipped-ricotta-and-hot-honey-toast": {
        "title": "Whipped Ricotta & Hot Honey Fig Toast",
        "description": "Ultra-creamy whole-milk ricotta whipped with citrus zest and sea salt, slathered over blistered sourdough and finished with warm spiced honey.",
        "category": "Toasts & Spreads",
        "difficulty": "Easy",
        "prepTime": "10 mins",
        "cookTime": "5 mins",
        "totalTime": "15 mins",
        "yield": "2 servings",
        "servingsCount": 2,
        "calories": 340,
        "heroImage": "https://images.unsplash.com/photo-1525351484163-7529414344d8?q=80&w=1200&auto=format&fit=crop",
        "tags": ["Ricotta", "Sourdough", "Hot Honey", "Figs", "Sweet & Savory", "Brunch"],
        "featured": True,
        "teaPairing": {
            "teaName": "Jasmine Pearl Green Tea",
            "description": "The delicate, intoxicating floral perfume of jasmine pearls cuts through the rich dairy fats of whole-milk ricotta while accentuating the amber honey sweetness.",
            "brewingNotes": "Steep 2g pearls in 75°C (167°F) water for 2.5 minutes."
        },
        "ingredients": [
            {"amount": "2", "unit": "thick slices", "name": "Rustic Country Sourdough"},
            {"amount": "1", "unit": "cup", "name": "Whole Milk Ricotta Cheese", "notes": "drained of excess whey"},
            {"amount": "1", "unit": "tbsp", "name": "Extra Virgin Olive Oil"},
            {"amount": "1", "unit": "tsp", "name": "Fresh Lemon Zest"},
            {"amount": "2", "unit": "tbsp", "name": "Hot Honey", "notes": "or clover honey with chili flakes"},
            {"amount": "4", "unit": "fresh", "name": "Ripe Figs", "notes": "quartered (or sliced stone fruit)"},
            {"amount": "1", "unit": "pinch", "name": "Flaky Maldon Sea Salt"},
            {"amount": "1", "unit": "sprig", "name": "Fresh Thyme Leaves"}
        ],
        "instructions": [
            {"step": 1, "title": "Whip the Ricotta", "instruction": "Add the ricotta, extra virgin olive oil, lemon zest, and a pinch of salt to a small food processor. Whip on high for 60 to 90 seconds until silky smooth, glossy, and cloud-like."},
            {"step": 2, "title": "Toast the Sourdough", "instruction": "Brush sourdough slices with olive oil and toast in a hot cast-iron skillet over medium-high heat until deeply golden and blistered, about 2-3 minutes per side."},
            {"step": 3, "title": "Assemble", "instruction": "Generously swirl the whipped ricotta across the warm toast. Arrange the fresh fig slices over the cheese."},
            {"step": 4, "title": "Finish & Drizzle", "instruction": "Warm the hot honey slightly in a small saucepan, drizzle generously over the figs and ricotta, and scatter fresh thyme leaves with a crunch of flaky sea salt."}
        ],
        "tips": [
            "Use whole milk ricotta; part-skim ricotta contains too much water and will separate rather than become velvety.",
            "Pan-toasting in olive oil gives a much crunchier, shatteringly crisp exterior compared to a slot toaster.",
            "If fresh figs are out of season, swap with caramelized pear slices, fresh berries, or roasted grapes."
        ],
        "nutrition": {
            "calories": "340",
            "protein": "14g",
            "fat": "16g",
            "carbs": "36g"
        },
        "story": """
There is toast, and then there is the sensory awakening of whipped ricotta on warm, charred sourdough. 

Standard grocery store ricotta straight from the tub often gets a bad reputation for being grainy and wet. But the secret that Italian trattorias have known for decades is that a ninety-second spin in a food processor transforms ordinary ricotta into a velvety spread rivaling imported mascarpone.

Paired with the deep, floral warmth of clover honey infused with chili heat, and the gentle sweetness of fresh summer figs, this recipe is proof that breakfast can feel like a boutique hotel indulgence in under fifteen minutes.

### The Secret to Shatteringly Crisp Toast
When you are topping bread with a luxurious spread like whipped ricotta, flimsy sandwich bread simply will not hold. You need a bread with structural integrity—an open-crumb sourdough with a chewy interior and thick crust. We prefer searing the bread in a cast-iron skillet with a gentle sheen of fruity olive oil, giving you deep golden Maillard browning and irresistible crunch.
"""
    }
}

def generate_recipe_md(data):
    frontmatter = {
        "title": data["title"],
        "description": data["description"],
        "pubDate": datetime.now().strftime("%Y-%m-%d"),
        "heroImage": data["heroImage"],
        "prepTime": data["prepTime"],
        "cookTime": data["cookTime"],
        "totalTime": data["totalTime"],
        "yield": data["yield"],
        "servingsCount": data["servingsCount"],
        "calories": data.get("calories", 350),
        "difficulty": data.get("difficulty", "Easy"),
        "category": data["category"],
        "tags": data["tags"],
        "featured": data.get("featured", False),
        "author": "Tea & Toast Team",
        "teaPairing": data.get("teaPairing"),
        "ingredients": data["ingredients"],
        "instructions": data["instructions"],
        "tips": data.get("tips", []),
        "nutrition": data.get("nutrition", {})
    }

    yaml_lines = ["---"]
    for k, v in frontmatter.items():
        if isinstance(v, (dict, list)):
            yaml_lines.append(f"{k}: {json.dumps(v, ensure_ascii=False)}")
        elif isinstance(v, bool):
            yaml_lines.append(f"{k}: {str(v).lower()}")
        elif isinstance(v, int):
            yaml_lines.append(f"{k}: {v}")
        else:
            clean_str = str(v).replace('"', '\\"')
            yaml_lines.append(f'{k}: "{clean_str}"')
    yaml_lines.append("---")
    yaml_lines.append("")
    yaml_lines.append(data.get("story", "").strip())
    yaml_lines.append("")

    return "\n".join(yaml_lines)

def main():
    parser = argparse.ArgumentParser(description="Generate rich recipe MDX for Tea & Toast")
    parser.add_argument("--title", type=str, help="Recipe Title")
    parser.add_argument("--category", type=str, default="Toasts & Spreads", help="Recipe Category")
    args = parser.parse_args()

    slug = slugify(args.title) if args.title else "whipped-ricotta-and-hot-honey-toast"
    recipe_data = RECIPE_TEMPLATES.get(slug)

    if not recipe_data:
        # Default generator
        recipe_data = {
            "title": args.title or "Artisanal Sourdough Toast",
            "description": f"A perfected breakfast recipe for {args.title or 'Artisanal Toast'} paired with artisanal tea.",
            "category": args.category,
            "difficulty": "Easy",
            "prepTime": "10 mins",
            "cookTime": "5 mins",
            "totalTime": "15 mins",
            "yield": "2 servings",
            "servingsCount": 2,
            "calories": 320,
            "heroImage": "https://images.unsplash.com/photo-1525351484163-7529414344d8?q=80&w=1200&auto=format&fit=crop",
            "tags": ["Toast", "Artisanal", "Breakfast", "Cozy"],
            "featured": False,
            "teaPairing": {
                "teaName": "English Breakfast Tea",
                "description": "Full-bodied malty black tea that balances savory and buttery tones.",
                "brewingNotes": "Steep 3g in 98°C water for 4 minutes."
            },
            "ingredients": [
                {"amount": "2", "unit": "slices", "name": "Artisan Sourdough Bread"},
                {"amount": "2", "unit": "tbsp", "name": "Cultured Butter"}
            ],
            "instructions": [
                {"step": 1, "title": "Toast Bread", "instruction": "Toast bread slices in a pan with melted butter until crisp and golden brown on both sides."},
                {"step": 2, "title": "Serve", "instruction": "Serve immediately alongside a steaming cup of freshly steeped tea."}
            ],
            "tips": ["Always preheat your skillet for uniform crust development."],
            "nutrition": {"calories": "320", "protein": "8g", "fat": "14g", "carbs": "38g"},
            "story": f"### The Philosophy of {args.title or 'Toast'}\n\nNothing beats a warm slice prepared with care and quality ingredients."
        }

    md_content = generate_recipe_md(recipe_data)
    out_dir = os.path.join(os.path.dirname(__file__), "..", "src", "content", "recipes")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{slug}.md")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"✅ Generated recipe at: {out_path}")

if __name__ == "__main__":
    main()
