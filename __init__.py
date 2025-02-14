import io
import os
import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QLineEdit, QFileDialog, QGroupBox, QPushButton, QCheckBox, QProgressBar, QLabel
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize
from PyPDF2 import PdfWriter, PdfReader, Transformation
 
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont("Corrido", "Autography.ttf"))
pdfmetrics.registerFont(TTFont("Hello", "Hello.ttf"))

class NumberToLetter:
    def __init__(self):
        self.numeros = {"0": "cero", "1":"uno", "2":"dos", "3":"tres", "4":"cuatro", "5":"cinco", "6":"seis", "7":"siete", "8":"ocho", "9":"nueve", "10":"diez", "11":"once", "12":"doce", "13":"trece", "14":"catorce", "15":"quince", "16":"dieciseis", "17":"diecisiete", "18":"dieciocho", "19":"diecinuene", "20":"veinte", "21":"veintiuno", "22":"veintidos", "23":"veintitres", "24":"veinticuatro", "25":"veinticinco", "26":"veintiseis", "27":"veintisiete", "28":"veintiocho", "29":"veintinueve"}
        self.decenas = ["","diez","veinte","Treinta", "cuarenta", "cincuenta", "sesenta", "setenta", "ochenta", "noventa"]
        self.centenas = ["","cien","doscientos","trescientos", "cuatrocientos", "quinientos", "seiscientos", "setecientos", "ochocientos", "novecientos"]
        self.llones = ["", "millón", "billón", "trillón", "cuatrillón"]
    def toLetter(self, a, sigue = False):
        
        if int(a)<30:
            if int(a) == 1:
                if sigue:
                    return "un"
                else:
                    return "uno"
            else:
                return self.numeros[str(int(a))]
        else:
            
            if len(a)<3:
                return self.decenas[int(a[0])] + " y " + self.numeros[a[1]] if a[1] != "0" else self.decenas[int(a[0])]
            elif len(a)<4:
                ret = ""
                if int(a[0]) == 1 and int(a[1:]) != 0:
                    ret += "ciento"
                else:
                    ret += self.centenas[int(a[0])]
                if int(a[1:]) == 0:
                    return ret
                else:
                    return ret + " "  + self.toLetter(a[1:])
            elif len(a)<7:
                ret = ""
                if int(a[:-3][-1]) == 1:
                    ret += self.toLetter(a[:-3])[:-1]
                else:
                    ret += self.toLetter(a[:-3])
                ret += " mil " + self.toLetter(a[-3:])
                return ret
            else:
                b = list(map(lambda x: x[::-1], [a[::-1][i*6:(i+1)*6] for i in range(int(len(a)//6)+1)][::-1]))
                for i,j in enumerate(b):
                    if j:
                        continue
                    else:
                        del(b[i])
                ret = ""
                
                print(self.llones[:len(b)-1][::-1])
                for i,j in enumerate(b):
                    ret += self.toLetter(j, i==(len(b)-1)) + " "
                    if int(j) == 1:
                        ret += self.llones[:len(b)][::-1][i] 
                    else:
                        ret += self.llones[:len(b)][::-1][i].replace("ón", "ones")
                    ret += " "
                    
                    
                return ret
                    
class EnumeratePDF:
    def __init__(self, path):
        self._pdf = PdfReader(open(path, "rb"))
        self.pages = self._pdf.pages
        self.packet = io.BytesIO()
        self.nump = len(self._pdf.pages)
        self.output = PdfWriter()
    
    def addNumber(self, c:Canvas, i:str, p:tuple)->None:
        c.setFont("Corrido", 22)
        c.setStrokeColorRGB(1, 1, 1)
        c.setFillColorRGB(1, 1, 1)
        c.roundRect(int(p[0]-10), int(p[1]-10), 25, 25, 8, 1, 1)
        c.setFillColorRGB(0, 0, 1)
        c.drawString(int(p[0]-5), int(p[1]-5), i)

    def addNumberletter(self, c:Canvas, i:str, p:tuple)->None:
        size = 18
        c.setFont("Hello", size)
        c.setStrokeColorRGB(1, 1, 1)
        c.setFillColorRGB(1, 1, 1)
        c.roundRect(int(p[0]-10)-int(len(i)*5), int(p[1]-10)-23,int(len(i)*8), 25, 8, 1, 1)
        c.setFillColorRGB(0, 0, 1)
        c.drawString(int(p[0]-5)-int(len(i)*5), int(p[1]-5)-22, i)
    
    def generate(self, path_o, letter=False, progress:QProgressBar=None, label:QLabel=None)->None:
        label.setText("Abriendo archivo")
        output = open(path_o, "wb")
        ntl = NumberToLetter()
        if progress:
            progress.setMaximum(self.nump)
        for i in range(self.nump):
            if progress:
                progress.setValue(i+1)
            page = self._pdf.pages[i]
            
            esquina_s = page.mediabox.upper_right
            esquina_i = page.mediabox.lower_left
        
            canvas = Canvas(self.packet, pagesize=(page.mediabox.width, page.mediabox.height))
            if float(esquina_s[0])-float(esquina_i[0])<float(esquina_s[1])-float(esquina_i[1]):
                
                self.addNumber(canvas, "%.2d"%(self.nump-i), (int(esquina_s[0]-35), int(esquina_s[1])-35))
                if letter:
                    self.addNumberletter(canvas, ntl.toLetter(str(self.nump-i)).capitalize(), (int(esquina_s[0]-35), int(esquina_s[1])-35))
            else:
                canvas.rotate(-90)
                self.addNumber(canvas, "%.2d"%(self.nump-i), (-35, int(esquina_s[0]-35)))
                if letter:
                    self.addNumberletter(canvas, ntl.toLetter(str(self.nump-i)).capitalize(), (-35, int(esquina_s[0])-35))
            
            canvas.save()
            
            self.packet.seek(0)
            
            res_pdf = PdfReader(self.packet)
            
            res_page = res_pdf.pages[0]
            op = Transformation().rotate(0).translate(tx=0, ty=0)
            res_page.add_transformation(op)
            page.merge_page(res_page)
            self.output.add_page(page)
        label.setText("Escribiendo archivo")
        self.output.write(output)
        output.close()
        label.setText("Archivo creado exitosamente!")



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
        grid3 = QHBoxLayout()
        group.setLayout(grid1)
        grid0.addWidget(self.filePath)
        
        button0 = QPushButton("Buscar", self)
        button0.clicked.connect(self.openFile)
        grid0.addWidget(button0)
        button1 = QPushButton("Enumerar", self)
        button1.clicked.connect(self.enumerar)
        button2 = QPushButton("Salir", self)
        button2.clicked.connect(self.close)

        self.label = QLabel(self)
        self.label.setText("A la espera...!")
        self.progressBar = QProgressBar(self)
        grid3.addWidget(self.label)
        grid3.addWidget(self.progressBar)
        grid2.addWidget(button1)
        grid2.addWidget(button2)
        grid1.addLayout(grid0)
        grid1.addWidget(self.check)
        grid1.addLayout(grid2)
        grid1.addLayout(grid3) 

    def openFile(self):
        file, cond = QFileDialog.getOpenFileName(self, "Abrir", "", "PDF (*.pdf)")
        if cond:
            self.filePath.setText(file)
            self.progressBar.setValue(0)
        
    def enumerar(self):
        print(self.filePath.text())
        path,file = os.path.split(self.filePath.text())
        
        namefile, ext= tuple(file.split("."))
        gen = EnumeratePDF(os.path.join(path,file)) 

        gen.generate(os.path.join(path, namefile+"fo."+ext), self.check.isChecked(), self.progressBar, self.label)
        

def main():
    app = QApplication(sys.argv)
    win = EnumerateUI()
    win.show()
    app.exec()

if __name__ == '__main__':
    main()
