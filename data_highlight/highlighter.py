from .support.char_array import CharIndex
from .support.line import Line
from .highlighter_functionality.export import export as export_from_functionality
from .support.token import SmallToken


class HighlightedFile:
    """
    class that can load/tokenize a datafile, record changes to the file,
    then export a highlighted version of the file that indicates extraction
    """

    def __init__(self, filename: str, number_of_lines=None):
        """
        Constructor for this object
        Args:
            filename (str): The name of the file to be parsed/reported upon
            number_of_lines(int) Number of lines that should be showed
                   to the output, or all line if omitted
        """
        self.chars = []
        self.filename = filename
        self.dict_color = {}
        self.number_of_lines = number_of_lines

    #

    def chars_debug(self):
        """
        Debug method, to check contents of chars
        """
        return self.chars

    def lines(self):
        """
        slice the file into single lines
        """
        if self.number_of_lines is None:
            return self.not_limited_lines()
        elif self.number_of_lines <= 0:
            print("Non-positive number of lines. Please provide positive number")
            exit(1)
        else:
            return self.limited_lines()

    def export(self, filename: str, include_key=False):
        """
        Provide highlighter summary for this file
        Args:
            filename (str): The name of the destination for the HTML output
        """
        export_from_functionality(filename, self.chars, self.dict_color, include_key)

    def limited_lines(self):
        """
            If  numberOfLines were limited
        :return:
        """

        with open(self.filename, 'r') as file:
            sample_lines = file.read()

        str_lines = sample_lines.splitlines()

        str_lines = str_lines[0:self.number_of_lines]
        str_to_char = '\n'.join(str(e) for e in str_lines)

        lines = self.fill_char_array(str_to_char, str_lines)
        return lines

    def not_limited_lines(self):
        with open(self.filename, 'r') as file:
            sample_lines = file.read()

        str_lines = sample_lines.splitlines()
        lines = self.fill_char_array(sample_lines, str_lines)
        return lines

    def fill_char_array(self, string_to_char, array_to_lines):
        line_ctr = 0
        lines = []

        # initialise the char index
        for char in string_to_char:
            # put letter into a struct
            char_ind = CharIndex(char)
            self.chars.append(char_ind)

        for this_line in array_to_lines:
            line_length = len(this_line)     
            line_span = (0, len(this_line))       
            smallToken = SmallToken(line_span, this_line, int(line_ctr), self.chars)
            new_l = Line([smallToken])
            lines.append(new_l)
            line_ctr += line_length + 1

        return lines
