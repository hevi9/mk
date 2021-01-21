from mk.location import Location


class MkError(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class DuplicateSourceError(MkError):
    location: Location
    id: str

    def __init__(self, msg, id: str, location: Location):
        super().__init__(f"Duplicate {id} in {location}: {msg}")
        self.location = location
        self.id = id


class FieldError(MkError):
    location: Location
    field: str

    def __init__(self, msg, field: str, location: Location):
        super().__init__(f"Error in field {field} in {location}: {msg}")
        self.location = location
        self.field = field


class ValidateError(MkError):
    def __init__(self, msg):
        super().__init__(msg)
