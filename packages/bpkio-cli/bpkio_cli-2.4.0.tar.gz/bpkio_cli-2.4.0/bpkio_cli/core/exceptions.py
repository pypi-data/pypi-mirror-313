class BroadpeakIoCliError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class UnexpectedContentError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class UsageError(BroadpeakIoCliError):
    def __init__(self, message):
        super().__init__(message)
