class InvalidType(Exception):
    def __init__(self, message):
        self.message = message

class MissingField(Exception):
    def __init__(self, message):
        self.message = message

class FieldsNotInHeader(Exception):
    def __init__(self, message):
        self.message = message

class InvalidField(Exception):
    def __init__(self, message):
        self.message = message

class LockedField(Exception):
    def __init__(self, message):
        self.message = message

class DataNotUnique(Exception):
    def __init__(self, message):
        self.message = message