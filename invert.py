# pip install pdf2img
# pip install img2pdf
from pdf2image import convert_from_path
from PIL import ImageOps
import os, img2pdf

def InvertPdfColor(filepath):

    if os.path.exists("output/") == False:
        os.mkdir("output/")

    file_basename = os.path.basename(filepath)
    file_name = os.path.splitext(file_basename)[0]

    images = convert_from_path(filepath)

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
    print("Invert PDF Color 1.0")
    print("Welcome\n")
    path = str(input("File path: "))
    try:
        InvertPdfColor(path)
        print("Finished.")
    except:
        print("Error occured while trying to invert pdf color.")
    exit(0)