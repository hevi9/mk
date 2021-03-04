from mk.location import Location


class MkError(Exception):
    """ """


class DuplicateSourceError(MkError):
    location: Location
    id2: str

    def __init__(self, msg, id2: str, location: Location):
        super().__init__(f"Duplicate {id2} in {location}: {msg}")
        self.location = location
        self.id2 = id2


class FieldError(MkError):
    location: Location
    field: str

    def __init__(self, msg, field: str, location: Location):
        super().__init__(f"Error in field {field} in {location}: {msg}")
        self.location = location
        self.field = field


class ValidateError(MkError):
    """ """
