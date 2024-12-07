class BitwardenDownloadError(Exception):
    """Exception raised when a download operation fails."""

    pass


class UnsupportedPlatformException(Exception):
    """Exception raised when an unsupported platform is encountered."""

    pass


class BitwardenInstallError(Exception):
    """Exception raised when an installation operation fails."""

    pass


class BitwardenNotInstalledError(Exception):
    """Exception raised when the Bitwarden CLI is not installed."""

    pass


class VaultItemNotFoundError(Exception):
    """Exception raised when a vault item is not found."""

    pass


class VaultError(Exception):
    """Exception raised when an error occurs with the vault."""

    pass


class VaultItemError(Exception):
    """Exception raised when an error occurs with a vault item."""

    pass


class VaultAttatchmentNotFoundError(Exception):
    """Exception raised when an attachment is not found."""

    pass


class InvalidTOTPKeyError(Exception):
    """Exception raised when an invalid TOTP key is encountered."""

    pass


class UpdatePasswordError(Exception):
    """Exception raised when an error occurs during a password update operation."""

    pass
