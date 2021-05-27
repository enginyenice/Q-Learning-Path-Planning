from texttable import Texttable

class FileOperation:
    fileName = ""
    f = any

    def __init__(self) -> None:
        self.fileName = "result.txt"

    def OutputFile(self, matrix,startPos,targetPos,shortedPath):
        f = open(self.fileName, "w+")
        result_text = ""
        table = Texttable()
        result_text = result_text + "BILGILENDIRME TABLOSU \n\n"
        table.add_rows([
            ["BILGI", "ICERIK" ],
            ["Duvar","[K]"],
            ["Yol","[G]"],
            ["Yukseklik",str(len(matrix))],
            ["Genislik",str(len(matrix[0]))],
            ["Baslangic(Ajan)","X:"+str(startPos[0])+" Y:"+str(startPos[1])],
            ["Hedef(Odul)","X:"+str(targetPos[0])+" Y:"+str(targetPos[1])]
        ])
                        
        result_text = result_text + table.draw() + "\n\n"
        result_text = result_text + "EN KISA YOL HAREKET TABLOSU \n\n"
        t = Texttable()
        pathTextArray = [['ADIM SAYISI', 'X','Y']]
        for location in range(len(shortedPath)):
                step = str(location+1) + ". adim"
                pathTextArray.append([step,str(shortedPath[location][0]),str(shortedPath[location][1])])
        t.add_rows(pathTextArray)
        result_text = result_text + t.draw()+ "\n\n"

        result_text = result_text + "HARITA \n\n"
        for x in range(len(matrix)):
            result_text = result_text+"[ "
            for y in range(len(matrix[x])):
                if matrix[x][y] == 0:
                    result_text = result_text + "("+str(x)+","+str(y)+",G) "
                else:
                    result_text = result_text + "("+str(x)+","+str(y)+",K) "
            result_text = result_text + "],\n"
        
        f.write(result_text)
        f.close()
