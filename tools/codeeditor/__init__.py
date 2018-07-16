import sys
import os
from PyQt5 import *

class CodeEditor(QtWidgets.QDialog):
    def __init__(self, main, current_file):
        super(CodeEditor, self).__init__(main)
        self.main = main
        self.webkit = QtWebKit.QWebView()
        self.realpath = os.path.dirname(os.path.realpath(__file__))

        self.current_file = current_file

        #Reading the target file
        if "objects" in self.current_file:
            extension = ".object.json"
            self.syntax_mode = "markdown"
        elif "scripts" in self.current_file:
            extension = ".py"
            self.syntax_mode = "python"
        else:
            print "Error over 9000"

        #Reading the template
        with open(os.path.join(self.realpath,'html','template.html')) as f:
            template = f.read()
            template = template.replace("MODE", self.syntax_mode)

        if self.current_file!="":
            try:
                with open(os.path.join(self.main.app_path, self.current_file + extension), 'r') as f:
                    target = f.read()
                    
            except:
                target = ""
        else:
            target = "ERROR OPENING THE FILE"
        
        new_file = template.replace("TEXTPLACEHOLDER", target)

        with open(os.path.join(self.realpath,'currentfile.html'),'w') as f:
            f.write(new_file)

        url = "file:///" + os.path.join(self.realpath,'currentfile.html')
        url = url.replace("\\", "/")
        self.webkit.load(QtCore.QUrl(url))

        self.ContainerGrid = QtWidgets.QGridLayout(self)
        self.ContainerGrid.setMargin (0)
        self.ContainerGrid.setSpacing(0)
        self.ContainerGrid.addWidget(self.webkit)
        self.setLayout(self.ContainerGrid)

        #saveAction = QtWidgets.QAction(QtGui.QIcon(), '&Save', self)        
        #saveAction.setShortcut('Ctrl+S')
        #saveAction.triggered.connect(self.save)
        QtWidgets.QShortcut(QtWidgets.QKeySequence("Ctrl+S"), self, self.save)

    def save(self):
        jscript = "editor.getValue();"     
        current_text = self.webkit.page().mainFrame().evaluateJavaScript(jscript)  
        current_text = current_text.toPyObject()

        self.main.statusBar().showMessage(self.current_file + ' Saved', 2000)
        with open(self.current_file,'w') as f:
            try:
                f.write(current_text)
            except Exception, e:
                print e

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = CodeEditor("C:\\Users\\Loremi\\Documents\\GitHub\\Astral\\Astral.py")
    mainWin.show()
    mainWin.raise_() #Making the window get focused on OSX
    sys.exit(app.exec_())
