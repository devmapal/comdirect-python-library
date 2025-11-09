"""Token persistence utilities for Comdirect API client.

This module provides functionality to save and load authentication tokens
to/from persistent storage, enabling session recovery after application restart.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class TokenStorageError(Exception):
    """Exception raised for token storage/retrieval errors."""

    pass


class TokenPersistence:
    """Handles persistent storage of OAuth2 tokens.

    This class saves access tokens, refresh tokens, and expiration time to a JSON file.
    Tokens can be recovered from storage to avoid requiring reauthentication after
    application restart.

    The token file format:
    ```json
    {
        "access_token": "abc123def456...",
        "refresh_token": "xyz789...",
        "token_expiry": "2024-11-10T18:30:45.123456"
    }
    ```

    Security Considerations:
    - Token files are stored in plain text JSON
    - Ensure file permissions are restrictive (600 recommended)
    - Store token files in secure locations (not in version control)
    - Consider encrypting token files in production environments
    """

    def __init__(self, storage_path: Optional[str] = None):
        """Initialize token persistence handler.

        Args:
            storage_path: Optional file path for token storage.
                         If None, no persistence is used.
                         Parent directories must exist.

        Raises:
            TokenStorageError: If storage_path directory doesn't exist.
        """
        self.storage_path: Optional[Path] = None

        if storage_path:
            path = Path(storage_path)
            parent = path.parent

            # Verify parent directory exists
            if not parent.exists():
                raise TokenStorageError(f"Storage directory does not exist: {parent.absolute()}")

            if not parent.is_dir():
                raise TokenStorageError(
                    f"Storage path parent is not a directory: {parent.absolute()}"
                )

            self.storage_path = path
            logger.debug(f"Token persistence enabled at: {self.storage_path.absolute()}")

    def save_tokens(
        self,
        access_token: str,
        refresh_token: str,
        token_expiry: datetime,
    ) -> None:
        """Save tokens to persistent storage.

        Args:
            access_token: OAuth2 access token
            refresh_token: OAuth2 refresh token
            token_expiry: Token expiration datetime

        Raises:
            TokenStorageError: If unable to write to storage file
        """
        if not self.storage_path:
            return

        try:
            token_data = {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_expiry": token_expiry.isoformat(),
            }

            with open(self.storage_path, "w") as f:
                json.dump(token_data, f)

            # Set restrictive file permissions (owner read/write only)
            self.storage_path.chmod(0o600)

            logger.debug(
                f"Tokens saved to {self.storage_path.name} "
                f"(expires: {token_expiry.isoformat()})"
            )

        except (IOError, OSError) as e:
            raise TokenStorageError(f"Failed to save tokens: {e}")

    def load_tokens(
        self,
    ) -> Optional[tuple[str, str, datetime]]:
        """Load tokens from persistent storage.

        Returns:
            Tuple of (access_token, refresh_token, token_expiry) if tokens exist
            and are valid, None otherwise.

        Raises:
            TokenStorageError: If storage file is corrupted or invalid
        """
        if not self.storage_path:
            return None

        if not self.storage_path.exists():
            logger.debug(f"No token storage file found at {self.storage_path}")
            return None

        try:
            with open(self.storage_path, "r") as f:
                token_data = json.load(f)

            # Validate required fields
            required_fields = {"access_token", "refresh_token", "token_expiry"}
            if not all(field in token_data for field in required_fields):
                raise TokenStorageError(
                    f"Invalid token file format. Missing fields: "
                    f"{required_fields - set(token_data.keys())}"
                )

            # Parse token expiry
            token_expiry = datetime.fromisoformat(token_data["token_expiry"])

            # Check if tokens are already expired
            if token_expiry <= datetime.now():
                logger.warning("Loaded tokens are expired")
                return None

            logger.debug(f"Tokens loaded from storage " f"(expires: {token_expiry.isoformat()})")

            return (
                token_data["access_token"],
                token_data["refresh_token"],
                token_expiry,
            )

        except json.JSONDecodeError as e:
            raise TokenStorageError(f"Token file is corrupted (invalid JSON): {e}")
        except ValueError as e:
            raise TokenStorageError(f"Token file has invalid datetime format: {e}")
        except (IOError, OSError) as e:
            raise TokenStorageError(f"Failed to read tokens: {e}")

    def clear_tokens(self) -> None:
        """Delete the token storage file.

        Useful for logout or when invalidating stored credentials.
        """
        if not self.storage_path:
            return

        try:
            if self.storage_path.exists():
                self.storage_path.unlink()
                logger.debug(f"Token storage cleared: {self.storage_path}")
        except (IOError, OSError) as e:
            logger.error(f"Failed to clear token storage: {e}")
