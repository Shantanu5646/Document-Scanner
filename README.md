# Document-Scanner
The Document Scanner is a Python-based project that allows you to scan documents from images using OpenCV. It detects document edges, applies perspective transformation, and enhances the scanned output for a clean, sharp look.
Features:-
Edge Detection & Perspective Transform – Automatically detects the document and straightens it.
Image Enhancement – Brightness & contrast correction.
Tech Stack:-
1. Python 3
2. OpenCV (for image processing)
3. NumPy (for numerical operations)
4. Pytesseract (for text extraction / OCR)
How It Works:-
1. Upload an image of a document.
   Use the cmp command in your IDE. python main.py --image [file name (ex:- doc.jpg)]
   Press Enter two times. At first Enter you get outline of the piece of paper
   At second enter you get scanned image.
3. The scanner detects edges and applies a 4-point perspective transform.
4. The processed image is enhanced for readability.
