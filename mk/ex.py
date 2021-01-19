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


class ValidateError(MkError):
    def __init__(self, msg):
        super().__init__(msg)
