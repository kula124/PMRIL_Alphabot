class FilterError(Exception):
    """Raised when there are too many objects in the image for given filter

    Attributes:
        message -- explanation of what went wrong with filtering
    """

    def __init__(self, message):
        self.message = message
