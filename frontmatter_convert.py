from pathlib import Path
import re
import sys
from datetime import datetime

# ========================================
# 変換対象ファイル
# ========================================

if len(sys.argv) != 2:
    print("MarkdownファイルをこのBATファイルにドラッグ＆ドロップしてください。")
    input("Enterキーで終了します。")
    sys.exit(1)

source_path = Path(sys.argv[1])

if not source_path.exists():
    print(f"ファイルが見つかりません: {source_path}")
    input("Enterキーで終了します。")
    sys.exit(1)

if source_path.suffix.lower() != ".md":
    print("Markdownファイル（.md）を指定してください。")
    input("Enterキーで終了します。")
    sys.exit(1)


# ========================================
# ファイル読み込み
# ========================================

text = source_path.read_text(encoding="utf-8")

if not text.startswith("---"):
    print("先頭にYAMLフロントマターがありません。")
    input("Enterキーで終了します。")
    sys.exit(1)

match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n?", text, re.DOTALL)

if not match:
    print("フロントマターの終了位置を確認できません。")
    input("Enterキーで終了します。")
    sys.exit(1)

frontmatter = match.group(1)
body = text[match.end():]


# ========================================
# 変換時点の現在時刻
# ========================================

current_time = datetime.now().astimezone().strftime(
    "%Y-%m-%dT%H:%M:%S%z"
)

current_time = current_time[:-2] + ":" + current_time[-2:]


# ========================================
# フロントマターを変換
# ========================================

lines = frontmatter.splitlines()

converted = []
found = set()

for line in lines:
    key_match = re.match(
        r"^([A-Za-z_][A-Za-z0-9_-]*):(\s*)(.*)$",
        line
    )

    if key_match:
        key = key_match.group(1)
        spacing = key_match.group(2)
        value = key_match.group(3)

        # category → categories
        if key == "category":
            converted.append(f"categories:{spacing}{value}")
            found.add("categories")
            continue

        # image → images
        if key == "image":
            converted.append(f"images:{spacing}{value}")
            found.add("images")
            continue

        # その他はそのまま
        converted.append(line)
        found.add(key)

    else:
        # リスト項目などはそのまま
        converted.append(line)


# ========================================
# 不足している項目を追加
# ========================================

converted.append(f"date: {current_time}")
found.add("date")

if "tags" not in found:
    converted.append("tags:")

if "weight" not in found:
    converted.append("weight:")

if "draft" not in found:
    converted.append("draft: true")


# ========================================
# フロントマターを再構成
# ========================================

new_frontmatter = "\n".join(converted)

result = f"---\n{new_frontmatter}\n---\n{body}"


# ========================================
# 別ファイルとして保存
# ========================================

output_path = source_path.with_name(
    source_path.stem + "_converted.md"
)

output_path.write_text(result, encoding="utf-8")

print()
print("変換しました。")
print(f"元ファイル:   {source_path.name}")
print(f"変換結果:     {output_path.name}")
print(f"date:         {current_time}")
print()
print("本文部分は変更していません。")

input("Enterキーで終了します.")