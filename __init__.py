from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QLineEdit, QFileDialog, QGroupBox, QPushButton, QCheckBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize
from enumerate_pdf import EnumeratePDF
import os
import sys

class EnumerateUI(QMainWindow):
    def __init__(self, *argv):
        super().__init__(*argv)
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("EnumeratePDF")
        self.setMinimumSize(QSize(600, 200))
        self.setMaximumSize(QSize(600, 200))
        self.setWindowIcon(QIcon("numeracion.png"))
        group = QGroupBox(self)
        group.setTitle("Seleccione el archivo")
        self.setCentralWidget(group)
        self.filePath = QLineEdit(self)
        self.check = QCheckBox("Numero en letras", self)
        
        grid1 = QVBoxLayout()
        grid0 = QHBoxLayout()
        grid2 = QHBoxLayout()
        group.setLayout(grid1)
        grid0.addWidget(self.filePath)
        
        button0 = QPushButton("Buscar", self)
        button0.clicked.connect(self.openFile)
        grid0.addWidget(button0)
        button1 = QPushButton("Enumerar", self)
        button1.clicked.connect(self.enumerar)
        button2 = QPushButton("Salir", self)
        grid2.addWidget(button1)
        grid2.addWidget(button2)
        grid1.addLayout(grid0)
        grid1.addWidget(self.check)
        grid1.addLayout(grid2) 

    def openFile(self):
        file, cond = QFileDialog.getOpenFileName(self, "Abrir", "", "PDF (*.pdf)")
        if cond:
            self.filePath.setText(file)
        
    def enumerar(self):
        print(self.filePath.text())
        path,file = os.path.split(self.filePath.text())
        
        namefile, ext= tuple(file.split("."))
        gen = EnumeratePDF(os.path.join(path,file)) 

        gen.generate(os.path.join(path, namefile+"fo."+ext), self.check.isChecked)
        

def main():
    app = QApplication(sys.argv)
    win = EnumerateUI()
    win.show()
    app.exec()

if __name__ == '__main__':
    main()
