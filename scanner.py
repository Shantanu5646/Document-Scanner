import cv2
from image_search.transform import four_point_transform
from enhancements import adjust_contrast_brightness, apply_threshold, recommend_thresh_method
import imutils

def scan_document(image_path, thresh_method=None, upscale=True, sharpen=True, do_ocr=False):
    """
    Scans a single document image.
    Returns:
        - scanned image (warped + enhanced)
        - extracted text (OCR) if needed
    """
    # Load image
    image = cv2.imread(image_path)
    ratio = image.shape[0] / 500.0
    orig = image.copy()
    image_resized = imutils.resize(image, height=500)

    # Convert to grayscale and detect edges
    gray = cv2.cvtColor(image_resized, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)

    # Find contours
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

    screenCnt = None
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            screenCnt = approx
            break

    if screenCnt is None:
        raise Exception("Could not find document edges.")

    # Perspective transform
    warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)

    # Enhance contrast, optional sharpen & upscale
    warped = adjust_contrast_brightness(warped, upscale=upscale, sharpen=sharpen)

    # Automatic threshold if not provided
    if thresh_method is None:
        thresh_method = recommend_thresh_method(warped)

    # Apply threshold
    scanned = apply_threshold(warped, method=thresh_method)
    text = None
    if do_ocr:
        import pytesseract
        text = pytesseract.image_to_string(scanned, lang="eng")

    return scanned, text