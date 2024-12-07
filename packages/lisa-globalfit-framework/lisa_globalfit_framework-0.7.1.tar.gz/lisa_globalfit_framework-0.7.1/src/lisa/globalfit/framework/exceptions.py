class FrameworkError(Exception):
    pass


class SerializationError(FrameworkError):
    pass


class DeserializationError(FrameworkError):
    pass
