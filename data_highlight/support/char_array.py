class CharIndex:
    """
    storage structure used to describe the activity on a single character
    """

    def __init__(self, letter):
        self.letter = letter
        self.usages = []

class SingleUsage:
    """
    storage of a single activity
    """

    def __init__(self, tool_field, message):
        self.tool_field = tool_field
        self.message = message
