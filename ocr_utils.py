import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"D:\Python requirements\Tesseract\tesseract.exe"
def extract_text(image):
    text = pytesseract.image_to_string(image, lang="eng")
    return text

def save_as_pdf(image, output_path):
    pdf_bytes = pytesseract.image_to_pdf_or_hocr(image, extension='pdf')
    with open(output_path, 'wb') as f:
        f.write(pdf_bytes)