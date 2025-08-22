import cv2
import numpy as np
from skimage.filters import threshold_local

def adjust_contrast_brightness(image, clip_limit=2.0, tile_grid_size=(8,8),
                               upscale=False, sharpen=True):
    """
    Enhances image clarity for readable scans and OCR:
    - Grayscale conversion
    - Mild sharpening (optional)
    - CLAHE contrast enhancement
    - Optional upscaling for small images
    """
    # Convert to grayscale
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    # Optional mild sharpening
    if sharpen:
        kernel = np.array([[0, -0.15, 0],
                           [-0.15, 1.6, -0.15],
                           [0, -0.15, 0]])
        gray = cv2.filter2D(gray, -1, kernel)

    # CLAHE for contrast
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    gray = clahe.apply(gray)

    # Optional upscale for small images
    if upscale and gray.shape[1] < 800:
        gray = cv2.resize(gray, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)

    return gray


def apply_threshold(image, method="adaptive"):
    """
    Applies thresholding to produce clean, high-contrast scanned image.
    method options: "adaptive", "otsu", "simple"
    """
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
        # fallback: return original image
        return image


def recommend_thresh_method(image):
    """
    Automatically select threshold method based on image analysis.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    std_dev = np.std(gray)
    mean_val = np.mean(gray)

    # Low variation, uniform image → Otsu
    if std_dev < 40:
        return "otsu"
    # Moderate variation → adaptive
    elif std_dev >= 40 and 60 < mean_val < 190:
        return "adaptive"
    # Extreme dark or bright images → simple
    else:
        return "simple"
