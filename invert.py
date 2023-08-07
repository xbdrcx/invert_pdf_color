# This version uses Poppler V23.07.0 (https://github.com/oschwartz10612/poppler-windows/releases/)
# When it executes for the first time it creates a VARIABLE PATH on the computer pointing to the existing Poppler folder in the project directory
# - pip install pdf2img
# - pip install img2pdf
from tkinter.filedialog import askopenfilename
from pdf2image import convert_from_path
from pdf2image.exceptions import (
        PDFInfoNotInstalledError,
        PDFPageCountError,
        PDFSyntaxError
)
from PIL import ImageOps
import os, sys, img2pdf

POPPLER_PATH = os.path.dirname(os.path.abspath(__file__)) + r"\poppler-23.07.0\library\bin"

sys.path.append(POPPLER_PATH)

def InvertPdfColor(filepath):

    if os.path.exists("output/") == False:
        os.mkdir("output/")

    file_name = os.path.splitext(os.path.basename(filepath))[0]
    
    try:
        images = convert_from_path(filepath, poppler_path=POPPLER_PATH)
    except (PDFInfoNotInstalledError, PDFPageCountError, PDFSyntaxError) as err:
        print(err)

    idx_counter = []
    for idx, i in enumerate(images):
        idx_counter.append('output'+str(idx)+".jpeg")
        i = ImageOps.invert(i)
        i.save('output'+ str(idx) +'.jpeg')

    with open("output/" + file_name + "_inverted.pdf", "wb") as f:
        f.write(img2pdf.convert(idx_counter))
        
    for i in idx_counter:
        os.remove(i)

if __name__ == "__main__":
    print("Invert PDF Color")
    print("Welcome\n")
    print("Opening file dialog...")
    path = askopenfilename(title="Choose PDF to Invert Colors", initialdir=POPPLER_PATH, filetypes=[("PDF", "*.pdf")])
    print("Choosen PDF: ", path)
    try:
        print("Inverting PDF colors...")
        InvertPdfColor(path)
        print("Finished.")
    except:
        print("Error occured while trying to invert PDF colors.")
    exit(0)
    