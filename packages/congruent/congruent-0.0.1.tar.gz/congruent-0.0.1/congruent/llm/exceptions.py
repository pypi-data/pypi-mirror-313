class LLMServiceError(Exception):
    """Base exception for LLM service errors."""

    pass


class ModelNotSupportedError(LLMServiceError):
    """Raised when no plugin can handle the requested model."""

    pass
