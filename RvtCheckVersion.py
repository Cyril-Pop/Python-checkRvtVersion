import sys
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
import os
import os.path as op
import olefile
import re
import base64

__author__ = "Cyril POUPIN"
__copyright__ = "Cyril POUPIN (c) 2022 "
__license__ = "MIT License"
__version__ = "2.1.0"

class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()

        self.setAlignment(Qt.AlignCenter)
        self.setText('\n\n Drop Revit files Here \n\n')
        self.setFont(QFont('Arial', 10))
        self.setStyleSheet('''
            QLabel{
                border: 4px dashed #aaa
            }
        ''')

    def setPixmap(self, image):
        super().setPixmap(image)

class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(400, 600)
        self.setAcceptDrops(True)
        self.setWindowTitle("Check Revit Version")

        mainLayout = QVBoxLayout()
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)

        self.photoViewer = ImageLabel()
        mainLayout.addWidget(self.photoViewer)
        #
        self.LabelRvtVersion = QLabel(self)
        self.LabelRvtVersion.setEnabled(True)
        self.LabelRvtVersion.setText("Version")
        self.LabelRvtVersion.setAlignment(Qt.AlignCenter)
        self.LabelRvtVersion.setFont(QFont('Arial', 12, QFont.Bold))
        self.LabelRvtVersion.setMargin(5)
        mainLayout.addWidget(self.LabelRvtVersion)
        #
        self.LabelDetail = QLabel(self)
        self.LabelDetail.setEnabled(True)
        self.LabelDetail.setText("Detail")
        self.LabelDetail.setAlignment(Qt.AlignCenter)
        self.LabelDetail.setFont(QFont('Arial', 10))
        self.LabelDetail.setMargin(5)
        mainLayout.addWidget(self.LabelDetail)
        #
        self.Label_lnk = QLabel(self)
        self.Label_lnk.setEnabled(True)
        urlLink = "Version : "+ __version__ +" : <a href=\"https://voltadynabim.blogspot.com\">'voltadynabim.blogspot.com'</a>"
        self.Label_lnk.setText(urlLink)
        self.Label_lnk.setAlignment(Qt.AlignBottom)
        self.Label_lnk.setOpenExternalLinks(True)
        self.Label_lnk.setMargin(5)
        mainLayout.addWidget(self.Label_lnk)

        self.setLayout(mainLayout)

    def dragEnterEvent(self, event):
        mimeData = event.mimeData()
        mineDataTxt = mimeData.text()
        file_path = event.mimeData().urls()[0].toLocalFile()
        if file_path.endswith(('.rfa', '.rvt', '.rte')):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        mimeData = event.mimeData()
        mineDataTxt = mimeData.text()
        file_path = event.mimeData().urls()[0].toLocalFile()
        if file_path.endswith(('.rfa','.rvt', '.rte')):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        mimeData = event.mimeData()
        mineDataTxt = mimeData.text()
        if mineDataTxt.endswith(('.rfa','.rvt', '.rte')):
            event.setDropAction(Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            print(file_path)
            self.set_rvt_preview(file_path)
            self.set_rvt_file_version(file_path)
            event.accept()
        else:
            event.ignore()


    def getfileInfo(self, rvt_ole):
        rvt_version = 'Version not found'
        bfiLe = rvt_ole.openstream("BasicFileInfo")
        file_infoLe = bfiLe.read().decode("utf-16le", "ignore")
        bfiBe = rvt_ole.openstream("BasicFileInfo")
        file_infoBe = bfiBe.read().decode("utf-16be", "ignore")
        file_info = file_infoBe if "਀" in file_infoLe else file_infoLe
        print(file_info)
        if "Format" in file_info:
            rvt_file_version = re.search(r"Format.+?(\d{4})", file_info).group(1)
        else:
            rvt_file_version = re.search(r"(\d{4}).+Build", file_info).group(1)
        rvt_version = 'Revit version {}'.format(rvt_file_version)
        return rvt_version, file_info

    def set_rvt_file_version(self, rvt_file):
        rvt_version = None
        if op.exists(rvt_file):
            if olefile.isOleFile(rvt_file):
                self.LabelRvtVersion.setText("Processing...")
                rvt_ole = olefile.OleFileIO(rvt_file)
                #bfi = rvt_ole.openstream("BasicFileInfo")
                # internal function
                rvt_version, file_info = self.getfileInfo(rvt_ole)
                fileinfoReader = file_info.split("sharing:").pop()
                self.LabelRvtVersion.setText(rvt_version)
                self.LabelDetail.setText(fileinfoReader)
                rvt_ole.close()
                return rvt_version
            else:
                self.LabelRvtVersion.setText("Error OLE structure")
                return rvt_version
        else:
            self.LabelRvtVersion.setText("File not found")
            return rvt_version

    def set_rvt_preview(self, rvt_file):
        newpreview = None
        if op.exists(rvt_file):
            if olefile.isOleFile(rvt_file):
                try:
                    # Open ole file
                    rvt_ole = olefile.OleFileIO(rvt_file)
                    bfi = rvt_ole.openstream("RevitPreview4.0")
                    readed = bfi.read()
                    # Find png signature
                    readed_hex = readed.hex()
                    pos = readed_hex.find('89504e470d0a1a0a')
                    png_hex = readed_hex[pos:]
                    data = bytes.fromhex(png_hex)
                    # encode to 64 to push in PhotoImage
                    base64_encoded_data = base64.b64encode(data)
                    print(base64_encoded_data)
                    pm = QPixmap()
                    pm.loadFromData(base64.b64decode(base64_encoded_data))
                    pm = pm.scaledToWidth(180)
                    self.photoViewer.setPixmap(pm)
                    newpreview = pm
                    rvt_ole.close()
                except Exception as ex:
                    print(ex)
        return newpreview

app = QApplication(sys.argv)
demo = AppDemo()
demo.show()
sys.exit(app.exec_())