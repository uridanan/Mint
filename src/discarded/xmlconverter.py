import xml.etree.ElementTree as ET
import xml.dom.minidom as MD
import csv
import sys
from os import walk


#-----------------------------------------------------------------------------------------------------------------------
# Helper class to retrieve files in a specific folder
class folder(object):
    path = ""

    def __init__(self, p):
        self.path = p

    # Get all file names in a folder
    def getFileNames(self):
        f = []
        for (dirpath, dirnames, filenames) in walk(self.path):
            f.extend(filenames)
            break
        return f


    # Get all file names that match any the of the file extensions from a given set
    def getFilesByExtension(self, extensions):
        flist = []
        files = self.getFileNames()
        for f in files:
            for ext in extensions:
                if (f.endswith(ext)):
                    flist.append(f)
        return flist

    # Get all xml files in the folder
    def getXMLFiles(self):
        return self.getFilesByExtension(["xml"])

    # Get all xml dita in the folder
    def getDITAFiles(self):
        return self.getFilesByExtension(["dita"])
#-----------------------------------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------------------------------
# Helper class for string manipulations
class myString(object):
    s = ""

    def __init__(self, s):
        self.s = s

    def get(self):
        return self.s

    # Remove all \n characters to flatten the string
    def stripNewLine(self):
        if (self.s == None):
            return ""
        return self.s.replace("\n", "")

    # Returns true if the string is empty
    def isEmpty(self):
        if (self.s == None):
            return True
        return self.stripNewLine().strip() == ""

#-----------------------------------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------------------------------
# Helper class for xml element manipulation
class myElement(object):
    e= None

    def __init__(self,e):
        self.e = e

    def get(self):
        return self.e

    # Returns true if the element has direct inner text (not including its sub-elements)
    def hasText(self):
        if(myString(self.e.text).isEmpty()):
            return False
        return True

    # Returns all of the elements inner text
    def getInnerText(self):
        # t = ET.tostring(e, "us-ascii", "text").decode()
        return "".join(self.e.itertext())

    # Returns a flat version of the inner text (after removing \n (new line) characters)
    def getCleanText(self):
        t = ""
        if(self.hasText()):
            t = self.getInnerText()
        return myString(t).stripNewLine()

    # Format an attribute of the element as key=value
    def getKeyValuePair(self,a):
        return "=".join([a,self.e.attrib[a]])

    # Return the element attributes as a string made of key=value pairs
    def getAttributes(self):
        attributes = []
        for a in self.e.attrib:
            attributes.append(self.getKeyValuePair(a))
        return ":".join(attributes)

    # Returns the element tag, text and attributes as a comma separated string
    def getEntry(self):
        tag = myString(self.e.tag).stripNewLine()
        text = self.getCleanText()
        attrib = self.getAttributes()
        return ",".join([tag,text,attrib])


#-----------------------------------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------------------------------
# Helper class for file manipulation
# Loads xml files as input and exports to csv where each row is <tag>,<inner text>,<attributes>
class xmlFile(object):
    inputFile = ""
    output = None
    root = None


    def __init__(self, filename):
        self.inputFile = filename
        self.load()

    # Load xml file using xml element tree
    def load(self):
        self.root = self.loadXML(self.inputFile)


    @staticmethod
    def loadXML(filename):
        return ET.parse(filename).getroot()

    # Write a line to file and add carriage return
    @staticmethod
    def writeln(file, string):
        file.write(string)
        file.write('\n')

    # Write headers to the csv file to describe the structure of the rows
    @staticmethod
    def getHeaders():
        return ",".join(["TAG", "TEXT", "ATTRIBUTES"])


    # Print string to console, then to file (if available) with carriage return
    def printRow(self, row):
        print(row)
        if (self.output != None):
            self.writeln(self.output, row)


    # Go over all sub elements of a given element
    # Print elements that have inner text (directly, not in sub-elements)
    def iterateElements(self):
        for e in self.root.iter():
            me = myElement(e)
            if (me.hasText()):
                self.printRow(me.getEntry())

    # Export xml to csv file by print csv rows for each element that has inner text
    def toCSV(self):
        # Open output file
        outputFile = self.inputFile + ".csv"
        self.output = open(outputFile, 'wt')

        try:

            print("==> open " + outputFile)

            # Write headers
            self.printRow(self.getHeaders())

            # Traverse XML tree
            self.iterateElements()

            print("==> close " + outputFile)

        except Exception as err:
            print(err)
        finally:
            self.output.close()
            self.output = None

#-----------------------------------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------------------------------

#Convert all xml / dita files in a given folder
def convertFolder(path):
    #files = folder(path).getDITAFiles()
    files = folder(path).getFilesByExtension([".html"])
    print(files)
    for f in files:
        xmlFile(path + "/" + f).toCSV()


def debug1():

    #debug single file
    f = xmlFile("../inbox/bankleumi30052018.html")
    f.toCSV()

    #parse command line arguments
    if(len(sys.argv) < 2):
        convertFolder("../inbox")
    else:
        for folder in sys.argv[1:len(sys.argv)]:
            # Convert all xml / dita files in input folder
            convertFolder(folder)


def debug2():
    tree = ET.parse("../inbox/bankleumi11062018.html")
    data = tree.getElementById("ctlActivityTable")

    xfile = MD.parse("../inbox/bankleumi11062018.html")
    data = xfile.getElementById("ctlActivityTable")
    print("data parsed")

def main():
    debug2()

main()


# NEXT
# Load list of tags to parse instead of the whole document
# Get elements by tagname, use each element as root for conversion
