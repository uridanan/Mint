class TimeSeriesData:
    data = dict()
    dates = []
    start = None
    end = None

    def __init__(self,dataFrame):
        self.data = self.groupByDate(dataFrame)

    def groupByDate(self,dataFrame):
        data = dict()
        start = None
        end = None
        for row in dataFrame.values:
            date = row[0]
            key = row[1]
            value = row[2]
            self.addDate(date)
            if date in data:
                entry = data[date]
            else:
                entry = dict()
            entry[key] = value
            data[date] = entry
        return data

    def addDate(self,date):
        if date in self.dates:
            return
        self.dates.append(date)
        if self.start == None:
            start = date
        self.end = date

    def getSeriesByName(self,name):
        values = []
        for k in self.data.keys():
            v = 0
            if name in self.data[k].keys() and self.data[k][name] != None:
                v = self.data[k][name]
            values.append(v)
        return values

    def getDates(self):
        return self.dates

    def getRange(self):
        return [self.start,self.end]