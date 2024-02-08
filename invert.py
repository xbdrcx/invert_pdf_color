# - pip install pdf2img
# - pip install img2pdf
import os, sys, img2pdf, threading
import tkinter as tk
from tkinter import ttk, messagebox, StringVar
from tkinter.filedialog import askopenfilename
from PIL import ImageOps
from pdf2image import convert_from_path
from pdf2image.exceptions import (
        PDFInfoNotInstalledError,
        PDFPageCountError,
        PDFSyntaxError
)

# Versions
print("Developed Under:")
print("python v.3.10.8")
print("poppler v.23.07.0")
print("Currently Using:")
print("python v." + sys.version)
print("poppler v.23.07.0")

# This version uses Poppler V23.07.0 (https://github.com/oschwartz10612/poppler-windows/releases/)
# When it executes for the first time it creates a VARIABLE PATH on the computer pointing to the existing Poppler folder in the project directory
POPPLER_PATH = os.path.dirname(os.path.abspath(__file__)) + r"\poppler-23.07.0\library\bin"
sys.path.append(POPPLER_PATH)

app_title = "PDF Color Inverter"

default_output_path = "output/"

if os.path.exists(default_output_path) == False:
    os.mkdir(default_output_path)

selected_file = ""
output_path = default_output_path

class GUI():
    def __init__(self):
        # MAIN CONFIG
        self.root = tk.Tk()
        self.root.title(app_title)
        self.root.geometry("400x250")
        self.root.resizable(0,0)
        # FRAMES
        self.top_frame = tk.Frame(self.root)
        self.bottom_frame = tk.Frame(self.root)
        self.progress_frame = tk.Frame(self.root)
        self.top_frame.rowconfigure(0, weight=4)
        self.bottom_frame.rowconfigure(0, weight=4)
        self.progress_frame.rowconfigure(0, weight=4)
        self.top_frame.grid(row=0, column=0, sticky="W")
        self.bottom_frame.grid(row=1, column=0, sticky="W")
        self.progress_frame.grid(row=2, column=0, sticky="W")
        # TOP ELEMENTS
        tk.Label(self.top_frame, text="Select PDF:").grid(row=0, column=0, padx=10, pady=10)
        self.import_btn = tk.Button(self.top_frame, text="Choose", command=lambda:ChooseFile(self))
        self.import_btn.grid(row=0, column=1, padx=10, pady=10)
        self.file_lbl = tk.Label(self.top_frame, text="None")
        self.file_lbl.grid(row=0, column=2, padx=10, pady=10, columnspan=1, sticky="W")
        # BOTTOM ELEMENTS
        var = StringVar()
        self.invert_btn = tk.Button(self.bottom_frame, text="Invert Colors", command=lambda:threading.Thread(target=InvertPdfColor, args=(self, )).start(), state="disabled")
        self.invert_btn.grid(row=0, column=0, padx=10, pady=10)
        self.output_folder_btn = tk.Button(self.bottom_frame, text="Open Folder", command=lambda:os.startfile(os.path.abspath("./" + output_path)))
        self.output_folder_btn.grid(row=0, column=1)
        self.output_area = tk.Text(self.bottom_frame, height=6, width=45)
        self.output_area.bindtags((str(), str(self.root), "all"))
        self.output_area.grid(row=1, column=0, columnspan=4, padx=10, pady=10)
        # PROGRESS BAR
        self.progress_bar = ttk.Progressbar(self.progress_frame, orient=tk.HORIZONTAL, mode="indeterminate", length=380)
        self.progress_bar.grid(row=0, column=0, padx=8, pady=8)
        # MENU BAR
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Change Output Directory", command=lambda:ChangeOutputDir(self))
        filemenu.add_command(label="Exit", command=lambda:self.root.destroy())
        menubar.add_cascade(label="File", menu=filemenu)
        self.root.config(menu=menubar)
        # INIT
        self.output(app_title + "\n")
        self.root.mainloop()

    def output(self, message):
        print(message)
        self.output_area.config(state=tk.NORMAL)
        self.output_area.insert(tk.INSERT, message+"\n")
        self.output_area.see(tk.END)
        self.output_area.config(state=tk.DISABLED)

def ChangeOutputDir(gui):
    return

def ChooseFile(gui):
    global selected_file
    selected_file = askopenfilename(filetypes=[("PDF", ".pdf")])
    gui.file_lbl.config(text=selected_file)
    gui.invert_btn.config(state="normal")

def InvertPdfColor(gui):
    file_name = os.path.splitext(os.path.basename(selected_file))[0]
    gui.root.update()
    try:
        gui.progress_bar.start()
        gui.output("Inverting...")
        images = convert_from_path(selected_file, poppler_path=POPPLER_PATH)
    except (PDFInfoNotInstalledError, PDFPageCountError, PDFSyntaxError) as err:
        gui.output(err)
    gui.progress_bar.stop()
    try:
        gui.progress_bar.config(mode="determinate")
        idx_counter = []
        for idx, i in enumerate(images):
            image_name = "output" + str(idx) + ".jpeg"
            idx_counter.append(image_name)
            i = ImageOps.invert(i)
            i.save(image_name)
            gui.progress_bar['value'] = (idx / len(images) + 1) * 100
        with open(output_path + file_name + "_inverted.pdf", "wb") as f:
            f.write(img2pdf.convert(idx_counter))
        for i in idx_counter:
            os.remove(i)
        gui.output("PDF colors inverted.")
        gui.file_lbl.config(text="None")
        gui.invert_btn.config(state="disabled")
        messagebox.showinfo(app_title, "PDF colors inverted.")
    except:
        gui.output("Error inverting PDF colors.")
        messagebox.showerror(app_title, "Error inverting PDF colors.")
    gui.progress_bar['value'] = 0

if __name__ == "__main__":
    gui = GUI()
    