class UniFiAccessError(Exception):
    """Base exception for UniFi Access API errors."""
    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__(f"API error {code}: {message}")

class AuthenticationError(UniFiAccessError):
    """Raised when authentication fails (HTTP 401)."""
    pass

class PermissionError(UniFiAccessError):
    """Raised when the token lacks necessary permissions (HTTP 403)."""
    pass

class RateLimitError(UniFiAccessError):
    """Raised when too many requests are sent (HTTP 429)."""
    pass