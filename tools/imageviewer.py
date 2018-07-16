#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets, QtGui
import os, sys

if sys.version_info.major == 2:
    str = unicode    

class ImageEditor(QtWidgets.QDialog):
    def __init__(self, main, name, filename):
        super(ImageEditor, self).__init__(main)
        self.main = main
        self.filename = filename
        self.name = name

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        if os.path.exists(os.path.join('..','images')):
        	img_path=os.path.join('..','images')
        else:
        	img_path=os.path.join('images')

        self.fitToWindowAct = QtWidgets.QAction("&Fit to Window", self,
                enabled=False, checkable=True, shortcut="Ctrl+F",
                triggered=self.fitToWindow)
        self.zoomInAct = QtWidgets.QAction("Zoom &In (25%)", self,
                shortcut="Ctrl++", enabled=True, triggered=self.zoomIn)

        self.zoomOutAct = QtWidgets.QAction("Zoom &Out (25%)", self,
                shortcut="Ctrl+-", enabled=True, triggered=self.zoomOut)

        self.normalSizeAct = QtWidgets.QAction("&Normal Size", self,
                shortcut="Ctrl+S", enabled=True, triggered=self.normalSize)

        saveAction = QtWidgets.QAction(QtGui.QIcon(os.path.join(img_path, 'save.png')), 'Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.triggered.connect(self.save_file)
        self.toolbar = QtWidgets.QToolBar('Image Toolbar')
        self.toolbar.setIconSize(QtCore.QSize(16, 16))
        self.toolbar.addAction(self.zoomInAct)
        self.toolbar.addAction(self.zoomOutAct)
        self.toolbar.addAction(self.normalSizeAct)

        self.ContainerGrid = QtWidgets.QGridLayout(self)
        self.ContainerGrid.setContentsMargins (0, 0, 0, 0)
        self.ContainerGrid.setSpacing(0)

        self.imageLabel = QtWidgets.QLabel()
        self.imageLabel.setBackgroundRole(QtGui.QPalette.Base)
        self.imageLabel.setStyleSheet('background-image: url(../images/transparent.png);')
        self.imageLabel.setSizePolicy(QtWidgets.QSizePolicy.Ignored,
                QtWidgets.QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)
        self.open_image(filename)

        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)

        self.widgetloco = QtWidgets.QWidget()
        self.nameEdit = QtWidgets.QLineEdit()
        spacer = QtWidgets.QWidget() 
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding) 

        self.LeftColGrid = QtWidgets.QGridLayout()
        self.LeftColGrid.addWidget(QtWidgets.QLabel('Name: '), 0,0)
        self.LeftColGrid.addWidget(self.nameEdit,0,1)
        self.LeftColGrid.addWidget(spacer)
        self.widgetloco.setLayout(self.LeftColGrid)
        self.widgetloco.setStyleSheet("max-width:150px;")

        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.splitter.addWidget(self.widgetloco)
        self.splitter.addWidget(self.scrollArea)

        self.ContainerGrid.addWidget(self.toolbar)
        self.ContainerGrid.addWidget(self.splitter)

        self.setLayout(self.ContainerGrid)


    def open_image(self, filename):
        fileName = filename
        if fileName:
            image = QtGui.QImage(fileName)
            if image.isNull():
                QtWidgets.QMessageBox.information(self, "Image Viewer",
                        "Cannot load %s." % fileName)
                return

            self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(image))
            self.scaleFactor = 1.0

            if not self.fitToWindowAct.isChecked():
                self.imageLabel.adjustSize()

    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.normalSize()

        self.updateActions()

    def zoomIn(self):
        self.scaleImage(1.25)

    def zoomOut(self):
        self.scaleImage(0.8)

    def normalSize(self):
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

        #self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        #self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        self.zoomInAct.setEnabled(self.scaleFactor < 10.0)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.1)

    def save_file(self):
        with open(self.filename, 'w') as f:
            f.write(self.textedit.toPlainText())
        self.main.statusBar().showMessage(os.path.basename(str(self.filename))+' saved!', 2000)

    def closeEvent(self, event):
            del self.main.window_index[self.name]

class Editor(QtWidgets.QMainWindow):
    def __init__(self):
        super(Editor, self).__init__()
        target="none"
        pathtofile="Astral.png"

        self.ShowFrame = QtWidgets.QFrame()
        self.showlayout = QtWidgets.QGridLayout()
        self.showlayout.setMargin(0)

        self.textedit = ImageEditor(self, target, pathtofile)

        self.showlayout.addWidget(self.textedit)
        self.ShowFrame.setLayout(self.showlayout)

        self.setCentralWidget(self.ShowFrame)
        self.setWindowTitle("Astral - ImageEditor")
        self.resize(640, 480)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = Editor()
    mainWin.show()
    mainWin.raise_() #Making the window get focused on OSX
    sys.exit(app.exec_())
