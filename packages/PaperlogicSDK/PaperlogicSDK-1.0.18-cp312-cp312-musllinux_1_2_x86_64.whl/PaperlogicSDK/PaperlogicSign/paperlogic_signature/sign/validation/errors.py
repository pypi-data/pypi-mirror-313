from typing import Optional
from ..general import ValueErrorWithMessage
from ..ades.report import AdESStatus, AdESSubIndic


__all__ = [
    'SignatureValidationError',
    'ValidationInfoReadingError',
    'NoDSSFoundError',
]

class ValidationInfoReadingError(ValueErrorWithMessage):
    """Error reading validation info."""

    pass


class NoDSSFoundError(ValidationInfoReadingError):
    def __init__(self):
        super().__init__("No DSS found")

class SignatureValidationError(ValueErrorWithMessage):
    """Error validating a signature."""

    def __init__(
        self, failure_message, ades_subindication: Optional[AdESSubIndic] = None
    ):
        self.ades_subindication = ades_subindication
        if ades_subindication:
            msg = "%s [%s]" % (failure_message, ades_subindication)
        else:
            msg = failure_message
        super().__init__(msg)

    @property
    def ades_status(self) -> Optional[AdESStatus]:
        if self.ades_subindication is not None:
            return self.ades_subindication.status
        return None
