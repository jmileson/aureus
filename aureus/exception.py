class AuruesException(Exception):
    pass


class InvalidResource(AuruesException):
    pass


class ResourceMissing(AuruesException):
    pass
