class ServiceUnavailableError(Exception):
    pass


class BusinessError(Exception):
    """Service layer errors"""

    pass


class UnauthorizedException(Exception):
    """Access Not authorized."""

    pass


class ConflictValueException(Exception):
    """Conflict."""

    pass
