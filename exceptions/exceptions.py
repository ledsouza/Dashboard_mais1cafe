class DatabaseError(Exception):
    """
    Custom exception class for database errors.

    Attributes:
        message (str): The error message associated with the exception.
    """

    def __init__(self, message):
        super().__init__(message)
        self.message = message
