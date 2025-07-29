import re
import os
import json
import asyncio
from collections import defaultdict
from pypdf import PdfReader, PdfWriter

BULLET_REGEX = re.compile(r"^(\d+(?:\.\d+)*)(?:[.)]?)\s+(.+)")
TOC_LINE_REGEX = re.compile(r"^(.*?)[\s\.\-]{2,}(\d+)$")


def extract_toc_from_text(text):
    toc_entries = []
    for line in text.split("\n"):
        match = TOC_LINE_REGEX.match(line.strip())
        if match:
            title = match.group(1).strip()
            page_number = int(match.group(2).strip())
            toc_entries.append((title, page_number))
    return toc_entries


def extract_bullets_from_doc(reader):
    bookmarks = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if not text:
            continue
        for line in text.split("\n"):
            match = BULLET_REGEX.match(line.strip())
            if match:
                bullet = match.group(1)
                title = match.group(2)
                level = bullet.count(".")
                parent_key = ".".join(bullet.split(".")[:-1]) if level > 0 else None
                bookmarks.append(
                    {
                        "key": bullet,
                        "title": title.strip(),
                        "page": i,
                        "level": level,
                        "parent_key": parent_key,
                    }
                )
    return bookmarks


def extract_headers_by_font(reader):
    font_sizes = defaultdict(list)
    for i, page in enumerate(reader.pages):
        if not page:
            continue
        try:
            blocks = page.get_text("dict")["blocks"]
        except Exception:
            continue
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span.get("text", "").strip()
                    if len(text) > 3 and not text.islower():
                        font_sizes[round(span["size"], 1)].append((i, text))
    if not font_sizes:
        return []
    top_fonts = sorted(font_sizes.keys(), reverse=True)[:3]
    bookmarks = []
    for level, size in enumerate(top_fonts, 1):
        for page, title in font_sizes[size]:
            bookmarks.append([level, title.strip(), page])
    return bookmarks


def normalize_bookmarks(bookmarks):
    if not bookmarks:
        return bookmarks
    for b in bookmarks:
        b[0] = int(b[0])
    min_level = min(b[0] for b in bookmarks)
    for b in bookmarks:
        b[0] = b[0] - min_level + 1
    return bookmarks


async def add_bookmarks_to_pdf_file(input_pdf_path):
    log = []

    if not os.path.isfile(input_pdf_path):
        return {"status": "error", "message": "Invalid file path", "log": log}

    folder = os.path.dirname(input_pdf_path)
    filename = os.path.basename(input_pdf_path)
    base, ext = os.path.splitext(filename)
    output_pdf_path = os.path.join(folder, f"{base}_bookmarked{ext}")

    reader = await asyncio.to_thread(PdfReader, input_pdf_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    # Extract TOC from first few pages
    toc_text = ""
    for page in reader.pages[:5]:
        toc_text += page.extract_text() or ""

    toc_entries = extract_toc_from_text(toc_text)
    bookmarks = []

    if toc_entries:
        log.append("✅ TOC found.")
        for title, page in toc_entries:
            level = title.count(".") + 1 if re.match(r"^\d+(\.\d+)*", title) else 1
            title_clean = re.sub(r"[\s\.\-]{2,}\d+$", "", title).strip()
            bookmarks.append([level, title_clean, page - 1])
    else:
        log.append("ℹ️ No TOC found. Trying bullet pattern...")
        bullets = extract_bullets_from_doc(reader)
        if bullets:
            log.append("✅ Bullet pattern found.")
            bookmarks_map = {}
            for b in bullets:
                node = writer.add_outline_item(b["title"], b["page"])
                bookmarks_map[b["key"]] = node
            for b in bullets:
                if b["parent_key"] in bookmarks_map:
                    child = writer.add_outline_item(
                        b["title"], b["page"], parent=bookmarks_map[b["parent_key"]]
                    )
                    bookmarks_map[b["key"]] = child
        else:
            log.append("⚠️ No bullets found. Trying font size headers...")
            bookmarks = extract_headers_by_font(reader)
            if bookmarks:
                log.append("✅ Font size-based headers found.")
                bookmarks = normalize_bookmarks(bookmarks)
                for level, title, page in bookmarks:
                    writer.add_outline_item(title, page)
            else:
                log.append("❌ No suitable headers found from font sizes.")

    if bookmarks:
        log.append("✅ Bookmarks added to writer.")
        bookmarks = normalize_bookmarks(bookmarks)
        parents = {0: None}
        for level, title, page in bookmarks:
            parent = parents.get(level - 1)
            bookmark = writer.add_outline_item(title, page, parent=parent)
            parents[level] = bookmark
    else:
        log.append("⚠️ No hierarchical bookmarks constructed.")

    await asyncio.to_thread(writer.write, output_pdf_path)

    log.append(f"📄 Bookmarked PDF saved to {output_pdf_path}")

    return {
        "status": "Bookmarks created successfully",
        "bookmarked_file": output_pdf_path,
        "bookmarks": bookmarks,
        "log": log,
    }
