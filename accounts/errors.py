from rest_framework import exceptions


class UserSerializerNotFound(exceptions.NotFound):
    """Exception class for not found the appropriate user serializer

    Args:
        Exception (exceptions.NotFound): the serializer does not found
    """

    def __init__(self, message=None):
        self.message = "Serializer not found" if not message else message
        super().__init__(self.message)
