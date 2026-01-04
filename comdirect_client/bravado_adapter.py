"""Custom HTTP client adapter for bravado-asyncio that injects Comdirect auth headers."""

import json
import logging
import time
import uuid
from typing import Any, Callable, Optional

from bravado_asyncio.http_client import AsyncioClient
from bravado.exception import HTTPError

logger = logging.getLogger(__name__)


class ComdirectBravadoClient(AsyncioClient):
    """Custom bravado-asyncio HTTP client that injects Comdirect authentication headers.

    This adapter extends AsyncioClient to automatically inject:
    - Authorization header with Bearer token
    - x-http-request-info header with session and request IDs
    - Optional per-request custom headers (via request_config)
    """

    def __init__(
        self,
        get_access_token: Callable[[], Optional[str]],
        get_session_id: Callable[[], str],
        generate_request_id: Callable[[], str],
        *args: Any,
        **kwargs: Any,
    ):
        """Initialize the Comdirect Bravado client adapter.

        Args:
            get_access_token: Callable that returns the current access token
            get_session_id: Callable that returns the current session ID (generates if None)
            generate_request_id: Callable that generates a request ID
            *args: Additional arguments passed to AsyncioClient
            **kwargs: Additional keyword arguments passed to AsyncioClient
        """
        super().__init__(*args, **kwargs)
        self._get_access_token = get_access_token
        self._get_session_id = get_session_id
        self._generate_request_id = generate_request_id
        # Store for response header access
        self._last_response_headers: Optional[dict[str, str]] = None

    def request(
        self,
        request_params: dict[str, Any],
        operation: Optional[Any] = None,
        request_config: Optional[dict[str, Any]] = None,
    ) -> Any:
        """Make an HTTP request with injected Comdirect headers.

        Args:
            request_params: Request parameters (method, url, headers, etc.)
            operation: Bravado operation object (optional)
            request_config: Additional request configuration (optional)
                Can contain 'custom_headers' dict for per-request headers

        Returns:
            Future that resolves to the HTTP response
        """
        # Get or create headers dict
        headers = request_params.get("headers", {})
        if not isinstance(headers, dict):
            headers = dict(headers) if headers else {}
        request_params["headers"] = headers

        # Inject Authorization header
        access_token = self._get_access_token()
        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"

        # Inject x-http-request-info header
        session_id = self._get_session_id()
        request_id = self._generate_request_id()
        headers["x-http-request-info"] = json.dumps(
            {
                "clientRequestId": {
                    "sessionId": session_id,
                    "requestId": request_id,
                }
            }
        )

        # Inject per-request custom headers if provided
        # request_config can be a dict or RequestConfig object
        if request_config:
            if isinstance(request_config, dict):
                # Handle dict-style request_config
                if "custom_headers" in request_config:
                    custom_headers = request_config["custom_headers"]
                    if isinstance(custom_headers, dict):
                        headers.update(custom_headers)
            else:
                # Handle RequestConfig object - check headers attribute
                if hasattr(request_config, "headers") and request_config.headers:
                    if isinstance(request_config.headers, dict):
                        headers.update(request_config.headers)

        # Ensure Accept header is set
        if "Accept" not in headers:
            headers["Accept"] = "application/json"

        logger.debug(
            f"Making {request_params.get('method', 'UNKNOWN')} request to "
            f"{request_params.get('url', 'UNKNOWN')} with auth headers"
        )

        # Call parent request method
        future = super().request(request_params, operation, request_config)
        
        # Wrap future to capture response headers
        # Note: This is a simplified approach - full header capture would require
        # wrapping the response object, which is complex with bravado-asyncio
        return future

    def get_last_response_headers(self) -> Optional[dict[str, str]]:
        """Get headers from the last response (if available).
        
        Note: This is a simplified implementation. Full header access would require
        more complex response wrapping.
        
        Returns:
            Response headers dict or None
        """
        return self._last_response_headers
