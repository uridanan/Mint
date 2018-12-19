import lxml
from lxml.html.clean import Cleaner

class HTMLFile(object):
    data = None

    def __init__(self,htmlFile):
        self.data = self.cleanInputFile(htmlFile)

    def cleanInputFile(self, htmlFile):
        cleaner = Cleaner()
        cleaner.javascript = True  # This is True because we want to activate the javascript filter
        cleaner.style = True  # This is True because we want to activate the styles & stylesheet filter
        # "WITH JAVASCRIPT & STYLES"
        htmlString = lxml.html.tostring(lxml.html.parse(htmlFile))
        # "WITHOUT JAVASCRIPT & STYLES"
        htmlClean = lxml.html.tostring(cleaner.clean_html(lxml.html.parse(htmlFile)))
        return htmlClean

    def getData(self):
        return self.data
