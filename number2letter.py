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
                
                for i,j in enumerate(b):
                    ret += self.toLetter(j, i==(len(b)-1)) + " "
                    if int(j) == 1:
                        ret += self.llones[:len(b)][::-1][i] 
                    else:
                        ret += self.llones[:len(b)][::-1][i].replace("ón", "ones")
                    ret += " "
                    
                    
                return ret
                    
