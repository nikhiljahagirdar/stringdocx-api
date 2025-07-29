import os
import pymupdf  # PyMuPDF
from PyPDF2 import PdfReader
import os
import asyncio


async def analyze_pdf_quality(file_path: str) -> dict:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    reader = PdfReader(file_path)

    is_encrypted = reader.is_encrypted
    result = {
        "is_security": False,
        "is_encrypted": is_encrypted,
        "has_bookmarks": False,
        "has_tags": False,
        "has_media": False,
        "has_images": False,
        "has_fonts": False,
        "has_non_standard_fonts": False,
        "has_tables": False,
        "has_links": False,
        "has_annotations": False,
        "has_form_fields": False,
    }

    if is_encrypted:
        # PDF is password protected, stop further analysis
        result["is_security"] = True
        return result
    else:
        result["is_security"] = reader.metadata is not None and reader.metadata != {}
        result["has_bookmarks"] = bool(reader.outline) if hasattr(reader, "outline") else False
        result["has_tags"] = "/MarkInfo" in reader.pages[0].keys() if reader.pages else False
        result["has_form_fields"] = any(
            page.get("/Annots") for page in reader.pages if page.get("/Annots")
        )

        standard_fonts = [
            "Courier",
            "Courier-Bold",
            "Courier-Oblique",
            "Courier-BoldOblique",
            "Helvetica",
            "Helvetica-Bold",
            "Helvetica-Oblique",
            "Helvetica-BoldOblique",
            "Times-Roman",
            "Times-Bold",
            "Times-Italic",
            "Times-BoldItalic",
            "Symbol",
            "ZapfDingbats",
        ]

        try:
            doc = pymupdf.open(file_path)
            text = ""
            all_fonts = set()
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text += page.get_text()
                if not result["has_images"] and page.get_images(full=True):
                    result["has_images"] = True
                if not result["has_links"] and page.get_links():
                    result["has_links"] = True
                if not result["has_annotations"] and page.annots():
                    result["has_annotations"] = True
                fonts = page.get_fonts(full=True)
                if fonts:
                    result["has_fonts"] = True
                    for font in fonts:
                        font_name = doc.xref_object(font[0])[7].decode('utf-8') if isinstance(doc.xref_object(font[0])[7], bytes) else doc.xref_object(font[0])[7]
                        all_fonts.add(font_name.split('+')[-1]) # Extract base font name

            doc.close()
            result["has_tables"] = "table" in text.lower()
            result["has_non_standard_fonts"] = any(font not in standard_fonts for font in all_fonts)
            # Media detection requires deeper XObject stream parsing, skipping for now
            # result["has_media"] = ...

        except Exception as e:
            print(f"Error processing file with PyMuPDF: {e}")
            # Continue with other information if available

    return result