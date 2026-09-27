from pathlib import Path
import re
import sys
import secrets
import string
from datetime import datetime


# ========================================
# 変換対象ファイル
# ========================================

if len(sys.argv) != 2:
    print("Markdownファイルをこのスクリプトにドラッグ＆ドロップしてください。")
    input("Enterキーで終了します...")
    sys.exit(1)

source_path = Path(sys.argv[1])

if not source_path.exists():
    print("ファイルが見つかりません。")
    input("Enterキーで終了します...")
    sys.exit(1)


# ========================================
# 出力先
# ========================================

output_dir = Path(
    r"C:\Users\white\Documents\PaperMod\content\posts"
)

output_dir.mkdir(parents=True, exist_ok=True)


# ========================================
# Markdown読み込み
# ========================================

text = source_path.read_text(encoding="utf-8")

if not text.startswith("---"):
    print("フロントマターが見つかりません。")
    input("Enterキーで終了します...")
    sys.exit(1)

parts = text.split("---", 2)

if len(parts) < 3:
    print("フロントマターの形式が正しくありません。")
    input("Enterキーで終了します...")
    sys.exit(1)

frontmatter = parts[1].strip()
body = parts[2].lstrip("\r\n")


# ========================================
# 日時
# ========================================

current_time = datetime.now().astimezone().isoformat(timespec="seconds")


# ========================================
# slug生成
# ========================================

def generate_slug():
    chars = string.ascii_lowercase + string.digits

    while True:
        slug = "".join(secrets.choice(chars) for _ in range(8))

        # 既存の投稿と重複しないか確認
        if not any(
            path.stem.endswith(slug)
            for path in output_dir.glob("*.md")
        ):
            return slug


# ========================================
# フロントマターを変換
# ========================================

lines = frontmatter.splitlines()

converted = []
found = set()
existing_slug = None

for line in lines:

    key_match = re.match(
        r"^([A-Za-z_][A-Za-z0-9_-]*):(\s*)(.*)$",
        line
    )

    if key_match:
        key = key_match.group(1)
        spacing = key_match.group(2)
        value = key_match.group(3)

        # ----------------------------------------
        # category → categories
        # ----------------------------------------

        if key == "category":
            converted.append(
                f"categories:{spacing}{value}"
            )
            found.add("categories")
            continue

        # ----------------------------------------
        # image → 削除
        # ----------------------------------------
        # 元のimageの値は使わず、
        # 後でslugを使ってimagesを生成する

        if key == "image":
            continue

        # ----------------------------------------
        # images
        # ----------------------------------------

        if key == "images":
            converted.append(line)
            found.add("images")
            continue

        # ----------------------------------------
        # slug
        # ----------------------------------------

        if key == "slug":
            converted.append(line)
            found.add("slug")
            existing_slug = value.strip()
            continue

        # ----------------------------------------
        # その他
        # ----------------------------------------

        converted.append(line)
        found.add(key)

    else:
        # リスト項目など
        converted.append(line)


# ========================================
# slugを確定
# ========================================

if "slug" not in found:
    new_slug = generate_slug()
    converted.append(f"slug: {new_slug}")
else:
    new_slug = existing_slug


# ========================================
# OGP画像設定
# ========================================

if "images" not in found:
    converted.append("images:")
    converted.append(
        f'  - "/images/ogp/{new_slug}.png"'
    )


# ========================================
# 不足している項目を追加
# ========================================

if "date" not in found:
    converted.append(f"date: {current_time}")

if "tags" not in found:
    converted.append("tags:")

if "weight" not in found:
    converted.append("weight:")

if "draft" not in found:
    converted.append("draft: true")


# ========================================
# 出力
# ========================================

new_frontmatter = "\n".join(converted)

output_text = (
    "---\n"
    + new_frontmatter
    + "\n---\n\n"
    + body
)

output_path = output_dir / f"{source_path.stem}_converted.md"

output_path.write_text(
    output_text,
    encoding="utf-8"
)


# ========================================
# 完了
# ========================================

print("変換完了")
print()
print(f"入力:  {source_path}")
print(f"出力:  {output_path}")
print(f"slug:  {new_slug}")
print(f"OGP:   /images/ogp/{new_slug}.png")
print()

input("Enterキーで終了します...")