import pandas as pd
import io


class ExcelContent(object):
    data = None

    def __init__(self,content):
        df = pd.read_excel(io.BytesIO(content))
        self.data = df.to_dict('records')

    def getData(self):
        return self.data

