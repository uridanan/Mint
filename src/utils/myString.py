
#-----------------------------------------------------------------------------------------------------------------------
# Helper class for string manipulations
class myString:

    # Remove all \n characters to flatten the string
    @staticmethod
    def stripNewLine(s):
        if not isinstance(s, str):
            return ""
        if (s == None):
            return ""
        return s.replace("\n", "")

    # Returns true if the string is empty
    @staticmethod
    def isEmpty(s):
        if (s == None):
            return True
        return myString.stripNewLine(s).strip() == ""

    @staticmethod
    def strip(s):
        if (s == None):
            return ""
        t = s.text.strip()
        return t

    @staticmethod
    def singleQuote(s):
        if (s == None):
            return "''"
        t = "'" + s + "'"
        return t

#-----------------------------------------------------------------------------------------------------------------------
