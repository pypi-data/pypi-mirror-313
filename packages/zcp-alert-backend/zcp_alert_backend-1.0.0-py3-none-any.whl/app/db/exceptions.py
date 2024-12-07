"""
Exceptions for AlertRequest

"""

from bson.errors import InvalidId


class ObjectNotFoundException(Exception):
    def __init__(self, object_id: str):
        self.object_id = object_id
        self.message = f"The ID '{object_id}' was not found"
        super().__init__(self.message)


class InvalidObjectIDException(InvalidId):
    """Invalid ObjectId exception"""


class ValueErrorException(Exception):
    """Value Error exception"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
