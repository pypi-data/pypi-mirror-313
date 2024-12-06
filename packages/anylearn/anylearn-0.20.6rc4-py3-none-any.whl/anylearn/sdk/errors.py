class AnylearnError(Exception):
    """Base Anylearn error."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class AnylearnInvalidResponseError(AnylearnError):
    """Raised when the response is invalid."""


class AnylearnArtifactDuplicationError(AnylearnError):
    """Raised when an artifact is duplicated."""


class AnylearnArtifactTooLargeError(AnylearnError):
    """Raised when an artifact is too large."""


class AnylearnNotSupportedError(AnylearnError):
    """Raised when the operation is not supported."""
