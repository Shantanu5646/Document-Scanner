"""import cv2
import numpy as np
from skimage.filters import threshold_local

def adjust_contrast_brightness(image, clip_limit=2.0, tile_grid_size=(8,8), upscale=False):
    # Grayscale
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    # Mild denoising
    gray = cv2.fastNlMeansDenoising(gray, h=5)

    # Optional mild sharpening
    kernel = np.array([[0,-0.25,0],
                       [-0.25,2,-0.25],
                       [0,-0.25,0]])
    gray = cv2.filter2D(gray, -1, kernel)

    # CLAHE (milder)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    gray = clahe.apply(gray)

    # Optional upscale
    if upscale and gray.shape[1] < 800:
        gray = cv2.resize(gray, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)

    return gray

def apply_threshold(image, method="adaptive"):
    if method == "adaptive":
        T = threshold_local(image, 11, offset=10, method="gaussian")
        return (image > T).astype("uint8") * 255
    elif method == "otsu":
        _, th = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return th
    elif method == "simple":
        _, th = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
        return th
    else:
        return image
    



#scanner.py
import cv2
import imutils
from image_search.transform import four_point_transform
from enhancements import adjust_contrast_brightness, apply_threshold
from ocr_utils import extract_text

def scan_document(image_path, thresh_method="adaptive"):
    # load the image
    orig = cv2.imread(image_path)
    ratio = orig.shape[0] / 500.0
    image = imutils.resize(orig, height=500)

    # convert to gray, blur, and edge detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)

    # find contours
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
        raise ValueError(f"[ERROR] Could not detect document boundary in {image_path}")

    # perspective transform
    warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)

    # enhance + threshold
    warped = adjust_contrast_brightness(warped)
    warped = apply_threshold(warped, method=thresh_method)

    # OCR text
    text = extract_text(warped)

    return warped, text"""