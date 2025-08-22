import argparse
import os
import glob
import cv2
from scanner import scan_document
from ocr_utils import save_as_pdf

def process_files(files, output_dir, thresh_method, do_ocr, do_pdf):
    os.makedirs(output_dir, exist_ok=True)

    for idx, f in enumerate(files):
        print(f"[INFO] Processing {f}")
        scanned, text = scan_document(f, thresh_method=thresh_method, do_ocr=args["ocr"])

        out_img = os.path.join(output_dir, f"scanned_{idx}.png")
        cv2.imwrite(out_img, scanned)

        if do_ocr:
            out_txt = os.path.join(output_dir, f"scanned_{idx}.txt")
            with open(out_txt, "w", encoding="utf-8") as txt_file:
                txt_file.write(text)

        if do_pdf:
            out_pdf = os.path.join(output_dir, f"scanned_{idx}.pdf")
            save_as_pdf(scanned, out_pdf)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, help="Path to image or folder")
    ap.add_argument("-o", "--output", default="output", help="Output folder")
    ap.add_argument("--thresh", default="adaptive", choices=["adaptive","otsu","simple"],
                    help="Threshold method")
    ap.add_argument("--ocr", action="store_true", help="Extract text and save to .txt")
    ap.add_argument("--pdf", action="store_true", help="Save as searchable PDF")
    args = vars(ap.parse_args())

    if os.path.isfile(args["input"]):
        files = [args["input"]]
    else:
        files = glob.glob(os.path.join(args["input"], "*.*"))

    process_files(files, args["output"], args["thresh"], args["ocr"], args["pdf"])