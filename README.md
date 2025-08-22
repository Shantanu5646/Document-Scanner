*** This repository contains two versions of a Document Scanner Project:
1. Original Project (basic scanner) – Available in the main branch.
2. Improved Project (enhanced scanner with OCR & PDF export) – Available in the improvements branch (default).

*** Original Project (main branch):-
1. Image scanning using perspective transform.
2. Basic thresholding for scanned effect.
3. Output as scanned images.

*** Improved Project (improvements branch):-
1. Brightness & Contrast correction.
2. Multiple thresholding methods (binary, adaptive, Otsu, etc.).
3. Batch processing of multiple images.
4. OCR integration using Tesseract.
5. Export as .txt or searchable PDF.
6. Cleaner, modular code with separate utility files:-
  1. enhancements.py → Image preprocessing.
  2. ocr_utils.py → OCR & PDF export.
  3. scanner.py → Document scanning (perspective transform).
  4. main.py → Entry point for CLI usage.

*** Run the Project:-

python main.py -i path/to/image.jpg --ocr --pdf

*** Outputs:-
1. Scanned Image (cleaned up)
2. Extracted Text file (.txt)
3. Searchable PDF (.pdf)

*** Branches:-
1. main:- Original basic project.
2. Improvements:- Enhanced scanner (default branch).

*** Why This Project?:-
1. Practical use of OpenCV for image preprocessing.
2. Applying OCR (pytesseract) for text extraction.
3. Handling real-world scanning challenges like skew correction & noise.
4. Code improvements: modular design, scalability, and CLI options.
