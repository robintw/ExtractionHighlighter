from .support.char_array import  CharIndex
from .support.line import  Line
from .support.color_picker import  hexColorFor, meanColorFor, colorFor

class HighlightedFile():
    """
    class that can load/tokenize a datafile, record changes to the file,
    then export a highlighted version of the file that indicates extraction
    """

    def __init__(self, filename: str,numberOfLines=None):
        """
        Constructor for this object
        Args:
            filename (str): The name of the file to be parsed/reported upon
        """
        self.filename = filename
        self.dictColor={}
        self.numberOfLines=numberOfLines
    #
    def charsDebug(self):
        """
        Debug method, to check contents of chars
        """
        return self.chars
    def lines(self):
        """
        slice the file into single lines
        """
        if self.numberOfLines == None:
            return self.notLimitedLines()
        elif self.numberOfLines <= 0 :
            print("Negative number of lines. Please provide positive number")
            exit(1)
        else:
            return self.limitedLines()



    def export(self, filename: str):
        """
        Provide highlighter summary for this file
        Args:
            filename (str): The name of the destination for the HTML output
        """
        fOut = open(filename, "w")

        lastHash = ""

        for charIndex in self.chars:
            letter = charIndex.letter
            thisHash = ""
            thisMessage = ""
            colors = []
            for usage in charIndex.usages:
                thisHash += usage.toolField
                needsNewLine = thisMessage != ""
                colors.append(colorFor(usage.toolField,self.dictColor))
                if needsNewLine:
                    thisMessage += " // "
                thisMessage += usage.toolField + ", " + usage.message

            # do we have anything to shade?
            if thisHash != "":
                # generate/retrieve a color for this hash
                newColor = meanColorFor(colors)
                hexColor = hexColorFor(newColor)

                # are we already in hash?
                if lastHash != "":
                    # is it the different to this one?
                    if (lastHash != thisHash):
                        # ok, close the span
                        fOut.write("</span>")

                        # start a new span
                        fOut.write("<span title='" + thisMessage + "' style=\"background-color:" + hexColor + "\"a>")
                else:
                    fOut.write("<span title='" + thisMessage + "' style=\"background-color:" + hexColor + "\">")
            elif lastHash != "":
                fOut.write("</span>")

            # just check if it's newline
            if (letter == "\n"):
                fOut.write("</br>")
            else:
                fOut.write(letter)

            lastHash = thisHash

        if (lastHash != ""):
            fOut.write("</span>")

        fOut.close()

    def limitedLines(self):
        """
            If  numberOfLines were limited
        :return:
        """

        with open(self.filename, 'r') as file:
            sampleLines = file.read()

        lineCtr = 0
        lines = []
        strLines = sampleLines.splitlines()
        strLines= strLines[0:self.numberOfLines]
        stringToChar = '\n'.join(str(e) for e in strLines)
        self.chars = [None] * len(stringToChar)
        # initialise the char index
        charCtr = 0
        for char in stringToChar:
            # put letter into a struct
            charInd = CharIndex(char)
            self.chars[charCtr] = charInd
            charCtr += 1
        counter=0


        for thisLine in strLines:
            thisLen = len(thisLine)
            newL = Line(str(lineCtr), str(lineCtr + thisLen), thisLine, self.chars)
            lines.append(newL)
            lineCtr += thisLen + 1


        return lines

    def notLimitedLines(self):
        with open(self.filename, 'r') as file:
            sampleLines = file.read()


            # make the char index the correct length
        self.chars = [None] * len(sampleLines)

        # initialise the char index
        charCtr = 0
        for char in sampleLines:
            # put letter into a struct
            charInd = CharIndex(char)
            self.chars[charCtr] = charInd
            charCtr += 1

            # ok, break the file into self-aware lines
        lineCtr = 0
        lines = []
        strLines = sampleLines.splitlines()

        stringToChar = ''.join(str(e) for e in strLines)
        for thisLine in strLines:
            thisLen = len(thisLine)
            newL = Line(str(lineCtr), str(lineCtr + thisLen), thisLine, self.chars)
            lines.append(newL)
            lineCtr += thisLen + 1

        return lines