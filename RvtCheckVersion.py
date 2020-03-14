# coding : utf-8
#CopyRight(c) 2019- POUPIN.C
#v1.3
import tkinter 
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
import os
import os.path as op
import olefile
import re
import base64
import webbrowser
import encodings


class Interface(Frame):
  def __init__(self, fenetre):
    ##The Base64 icon version as a string
    icon = "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"
    img = tkinter.PhotoImage(data=icon)
    Frame.__init__(self, fenetre, width=280, height=110)
    fenetre.minsize(width=280, height=110)
    fenetre.title("Check Rvt version")
    fenetre.wm_iconphoto(True, img)
    self.pack(fill=BOTH)
    self.filename = None
    self.message = Label(self, text="Verification de la version d'un fichier Revit", bd=10)
    self.message.pack()
    self.info = Label(self, text="_", bd=3)
    self.info.pack()
    self.bouton_quitter = Button(self, text="Quitter", command=self.quit, bd=2)
    self.bouton_quitter.pack(side="left", padx=10,pady=10)
    self.bouton_cliquer = Button(self, text="Choisir le fichier", fg="red", command=self.cliquer, bd=2)
    self.bouton_cliquer.pack(side="right", padx=10,pady=10)
    self.lbl = Label(fenetre, text=r"https://voltadynabim.blogspot.com/", fg="blue", cursor="hand2")
    self.lbl.pack()
    self.lbl.bind("<Button-1>", self.callback)
 

  def callback(self, event):
    webbrowser.open_new(event.widget.cget("text"))
  def cliquer(self):
    def getfileInfo(bfi):
      msgbox = 'Version non trouvée'
      file_info_read = bfi.read() 
      for codec , regex in [['utf_16_le', r"(\d{4})..Build"], ['utf_16_be', r"Format.+?(\d{4})"]]:
        file_info = file_info_read.decode(codec, "ignore")
        print(file_info)
        if re.search(regex, file_info) is not None:
          rvt_file_version = re.search(regex, file_info).group(1)
          msgbox = 'Fichier Revit version {}'.format(rvt_file_version)
          break
      return msgbox, file_info         

    def get_rvt_file_version(rvt_file):
      if op.exists(rvt_file):
        if olefile.isOleFile(rvt_file):
          rvt_ole = olefile.OleFileIO(rvt_file)
          bfi = rvt_ole.openstream("BasicFileInfo")
          #internal function
          msgbox, file_info = getfileInfo(bfi)
          fileinfoReader = file_info.split("Username:").pop()
          self.info["text"] = "\nINFORMATIONS FICHIER\n\nAuteur:" + fileinfoReader
          return msgbox
        else:
          msgbox = "le fichier n'a pas de structure OLE"
          return msgbox
      else:
        msgbox = "Fichier non trouvé"
        return msgbox
        
    filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Revit Files","*.rfa;*.rvt;*.rte"),("all files","*.*")))
    verionRvt = get_rvt_file_version(filename)
    self.message["text"] = verionRvt
    self.message["bg"] = "red"

fenetre = Tk()
interface = Interface(fenetre)

interface.mainloop()
try:
  interface.destroy()
except: pass