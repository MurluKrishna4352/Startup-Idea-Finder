import os
import markdown
import pdfkit
import shutil

def get_wkhtmltopdf_path():
    """Find wkhtmltopdf binary automatically"""
    if shutil.which("wkhtmltopdf"):
        return shutil.which("wkhtmltopdf")

    default_windows_path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    if os.path.exists(default_windows_path):
        return default_windows_path

    raise FileNotFoundError("wkhtmltopdf not found. Please install it and add to PATH.")

def save_to_markdown(text, filename="solutions.md"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)

def markdown_to_pdf(md_file="solutions.md", pdf_file="solutions.pdf"):
    with open(md_file, "r", encoding="utf-8") as f:
        html = markdown.markdown(f.read())

    config = pdfkit.configuration(wkhtmltopdf=get_wkhtmltopdf_path())
    pdfkit.from_string(html, pdf_file, configuration=config)
