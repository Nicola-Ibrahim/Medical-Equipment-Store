from rest_framework import exceptions


class UserSerializerNotFound(exceptions.NotFound):
    """Exception class for not found the appropriate user serializer

    Args:
        Exception (exceptions.NotFound): serializer does not found
    """

    def __init__(self, message=None):
        self.message = "Serializer not found" if not message else message
        super().__init__(self.message)


class UserFilterNotFound(exceptions.NotFound):
    """Exception class for not found the appropriate user filter

    Args:
        Exception (exceptions.NotFound): filter does not found
    """

    def __init__(self, message=None):
        self.message = "Filter not found" if not message else message
        super().__init__(self.message)


class UserModelNotFound(exceptions.NotFound):
    """Exception class for not found the appropriate user filter

    Args:
        Exception (exceptions.NotFound): filter does not found
    """

    def __init__(self, message=None):
        self.message = "Model not found" if not message else message
        super().__init__(self.message)