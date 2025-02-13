from PyPDF2 import PdfWriter, PdfReader, Transformation
import io
import os 
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from number2letter import NumberToLetter as n2l
pdfmetrics.registerFont(TTFont("Corrido", "Autography.ttf"))
pdfmetrics.registerFont(TTFont("Hello", "Hello.ttf"))

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
    
    def generate(self, path_o, letter=False)->None:
        output = open(path_o, "wb")
        ntl = n2l()
        for i in range(self.nump):
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
        self.output.write(output)
        output.close()


def main():
    path,file = os.path.split(input("Ingrese ubicacion del archivo: "))
    letras = input("Quiere con letras? (Y/N): ").lower()
    namefile, ext= tuple(file.split("."))
    gen = EnumeratePDF(os.path.join(path,file)) 

    gen.generate(os.path.join(path, namefile+"fo."+ext), letras == "y")

if __name__ == '__main__':
    main()
