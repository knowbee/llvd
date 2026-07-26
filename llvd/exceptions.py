class LLVDBaseException(Exception):
    """Base exception for all LLVD exceptions."""
    pass

class EmptyCourseList(LLVDBaseException):
    """Raised when parsing a learning path returns zero courses."""
    pass

class AuthenticationError(LLVDBaseException):
    """Raised when authentication fails."""
    pass

class NetworkError(LLVDBaseException):
    """Raised when network requests fail."""
    pass

class FileAccessError(LLVDBaseException):
    """Raised when file access operations fail."""
    pass

class ConfigurationError(LLVDBaseException):
    """Raised when there's an issue with configuration."""
    pass

class DownloadError(LLVDBaseException):
    """Raised when video download fails."""
    pass

class ParsingError(LLVDBaseException):
    """Raised when parsing operations fail."""
    pass
