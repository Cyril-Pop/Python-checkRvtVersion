# coding : utf-8
import tkinter 
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
import os.path as op
import olefile
import re

def get_rvt_file_version(rvt_file):
  if op.exists(rvt_file):
    if olefile.isOleFile(rvt_file):
      rvt_ole = olefile.OleFileIO(rvt_file)
      bfi = rvt_ole.openstream("BasicFileInfo")
      file_info = bfi.read().decode("utf-16le", "ignore")
      rvt_file_version = re.search(r"(\d{4})", file_info).group(1)
      return rvt_file_version
    else:
      msgbox = "le fichier n'est pas de structure OLE: {}".format(rvt_file)
      messagebox.showinfo(msgbox)
  else:
    msgbox = "Fichier non trouvé: {}".format(rvt_file)
    messagebox.showinfo(msgbox)


root = Tk()
root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Revit Files","*.rfa;*.rvt"),("all files","*.*")))
verionRvt = get_rvt_file_version(root.filename)
info = messagebox.showinfo('Information Fichier', 'Fichier Revit version {}'.format(verionRvt))
#root.mainloop()