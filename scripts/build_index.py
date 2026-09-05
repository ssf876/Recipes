from pathlib import Path
from collections import defaultdict
import yaml

RECIPES_DIR = Path("recipes")
INDEX_FILE = Path("INDEX.md")

by_category = defaultdict(list)
by_country = defaultdict(list)
by_macro = defaultdict(list)

for recipe_file in RECIPES_DIR.rglob("*.md"):
    text = recipe_file.read_text()

    if not text.startswith("---"):
        continue

    _, frontmatter, _ = text.split("---", 2)
    metadata = yaml.safe_load(frontmatter)

    title = metadata["title"]
    relative_path = recipe_file.as_posix()

    entry = f"[{title}]({relative_path})"

    for category in metadata.get("categories", []):
        by_category[category].append(entry)

    country = metadata.get("country")
    if country:
        by_country[country].append(entry)

    macros = metadata.get("macros", {})

    if macros.get("protein") == "high":
        by_macro["High Protein"].append(entry)

    if macros.get("carbs") == "high":
        by_macro["High Carb"].append(entry)

    if macros.get("fat") == "high":
        by_macro["High Fat"].append(entry)


def section(title, groups):
    output = [f"## {title}", ""]

    for group in sorted(groups):
        output.append(f"### {group}")
        output.append("")

        for recipe in sorted(groups[group]):
            output.append(f"- {recipe}")

        output.append("")

    return output


lines = [
    "# Recipe Index",
    "",
    "_This file is generated automatically from recipe metadata._",
    "",
]

lines += section("By Category", by_category)
lines += section("By Cuisine", by_country)
lines += section("By Macro Profile", by_macro)

INDEX_FILE.write_text("\n".join(lines))

print(f"Generated {INDEX_FILE}")
