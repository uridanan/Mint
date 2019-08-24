import lxml
from lxml.html.clean import Cleaner

class HTMLFile(object):
    data = None

    def __init__(self,htmlFile):
        self.data = self.cleanInputFile(htmlFile)

    def loadInputFile(self, htmlFile):
        # "WITH JAVASCRIPT & STYLES"
        htmlString = lxml.html.parse(htmlFile)
        return htmlString

    def cleanInputString(self, htmlString):
        # "WITH JAVASCRIPT & STYLES"
        cleaner = Cleaner()
        cleaner.javascript = True  # This is True because we want to activate the javascript filter
        cleaner.style = True  # This is True because we want to activate the styles & stylesheet filter
        # "WITHOUT JAVASCRIPT & STYLES"
        htmlClean = lxml.html.tostring(cleaner.clean_html(htmlString))
        return htmlClean

    def cleanInputFile(self, htmlFile):
        return self.cleanInputString(self.loadInputFile(htmlFile))

    def getData(self):
        return self.data
