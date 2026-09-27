# ========================================
# フロントマターを変換
# ========================================

lines = frontmatter.splitlines()

converted = []
found = set()
existing_slug = None
had_image = False

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

        # image → 削除して記録
        if key == "image":
            had_image = True
            continue

        # imagesが既にある場合はそのまま維持
        if key == "images":
            converted.append(line)
            found.add("images")
            continue

        # slugが既にある場合はそのまま維持
        if key == "slug":
            converted.append(line)
            found.add("slug")
            existing_slug = value.strip()
            continue

        # その他はそのまま
        converted.append(line)
        found.add(key)

    else:
        # リスト項目などはそのまま
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
    converted.append(f'  - "/images/ogp/{new_slug}.png"')


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