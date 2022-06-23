class SleepyDriveException(Exception):
    """
    The base class for all SleepyDrive exceptions.
    """
    pass


class AccountNotFound(SleepyDriveException):
    def __init__(self, message):
        super().__init__(message)


class InvalidCredentials(SleepyDriveException):
    def __init__(self, message):
        super().__init__(message)


class UnableToCreate(SleepyDriveException):
    def __init__(self, message):
        super().__init__(message)


class InvalidURL(SleepyDriveException):
    def __init__(self, message):
        super().__init__(message)


class InvalidFile(SleepyDriveException):
    def __init__(self, message):
        super().__init__(message)


class FileNotFound(SleepyDriveException):
    def __init__(self, message):
        super().__init__(message)


class InvalidParameter(SleepyDriveException):
    def __init__(self, message):
        super().__init__(message)
