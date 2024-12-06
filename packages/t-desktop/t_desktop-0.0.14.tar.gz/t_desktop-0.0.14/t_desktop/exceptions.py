class UsernameNotFoundError(Exception):
    """Operational System Username not found in env variables."""

    pass


class AppCrashException(Exception):
    """Application Crashed."""

    pass


class LoginMethodNotFoundError(Exception):
    """Custom exception raised when the login method is not found."""

    pass
