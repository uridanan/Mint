import pandas as pd
import io


class ExcelContent(object):
    data = None

    def __init__(self,content):
        try:
            iocontent = io.BytesIO(content)
            df = pd.read_excel(iocontent)
            self.data = df.to_dict('records')
        except Exception as e:
            #print(e)
            contentString = content.decode('utf-16')
            self.data = self.readExcel(contentString)

    def getData(self):
        return self.data

    def readExcel(self,stringContent):
        rowsIn = stringContent.split('\n')
        rowsOut = []
        for r in rowsIn:
            rowsOut.append(r.split('\t'))
        return rowsOut




