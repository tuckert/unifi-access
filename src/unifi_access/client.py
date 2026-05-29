try:
    import httpx
except ImportError:
    httpx = None

from dotenv import load_dotenv

load_dotenv()

import os
import logging

from .exceptions import UniFiAccessError, AuthenticationError, PermissionError, RateLimitError
from .managers.user import UserManager
from .managers.visitor import VisitorManager
from .managers.access_policy import AccessPolicyManager
from .managers.credential import CredentialManager
from .managers.space import SpaceManager
from .managers.device import DeviceManager
from .managers.system_log import SystemLogManager
from .managers.https_certificate import HttpsCertificateManager
from .managers.notification import NotificationManager
from .managers.identity import IdentityManager


logger = logging.getLogger(__name__)


def _preview(value, max_len: int = 500):
    """Return a safe, truncated preview string for debug logs."""
    try:
        text = str(value)
    except Exception:
        return '<unprintable>'
    if text is None:
        return 'None'
    text = text.strip()
    if len(text) > max_len:
        return text[:max_len] + '…'  # ellipsis
    return text


class UniFiAccessClient:
    """Client for interacting with the UniFi Access API."""

    users: UserManager
    visitors: VisitorManager
    access_policies: AccessPolicyManager
    credentials: CredentialManager
    spaces: SpaceManager
    devices: DeviceManager
    system_logs: SystemLogManager
    https_certificates: HttpsCertificateManager
    notifications: NotificationManager
    identity: IdentityManager

    def __init__(
            self,
            base_url=os.getenv('UNIFI_ACCESS_BASE_URL'),
            api_token=os.getenv('UNIFI_ACCESS_API_TOKEN'),
            port='12445',
            verify_ssl=False
    ):
        """
        Initialize the client.

        Args:
            base_url (str): The base URL of the API (e.g., 'https://console-ip:12445').
            api_token (str): The API token from UniFi Portal.
            verify_ssl (bool): Whether to verify SSL certificates (default: True).
        """
        # Check env variables for base_url, api_token, and port and use if not provided on initialization.
        if not base_url:
            base_url = os.getenv('UNIFI_ACCESS_BASE_URL')
        if not api_token:
            api_token = os.getenv('UNIFI_ACCESS_API_TOKEN')
        if not port:
            port = os.getenv('UNIFI_ACCESS_PORT', '12445')

        # Validate required dependencies
        if httpx is None:
            raise UniFiAccessError(
                "MISSING_DEPENDENCY",
                "httpx is required but not installed. Please install the 'httpx' package."
            )

        # Validate required settings
        if not base_url or not str(base_url).strip():
            raise UniFiAccessError(
                "MISSING_ENV",
                "Base URL is not configured. Set 'UNIFI_ACCESS_BASE_URL' in your environment/.env or pass base_url explicitly."
            )
        if not api_token or not str(api_token).strip():
            raise UniFiAccessError(
                "MISSING_ENV",
                "API token is not configured. Set 'UNIFI_ACCESS_API_TOKEN' in your environment/.env or pass api_token explicitly."
            )

        # Normalize and validate port
        if isinstance(port, str):
            port = port.strip()
        if not port:
            port = '12445'
        if not str(port).isdigit():
            raise UniFiAccessError(
                "INVALID_CONFIG",
                "UNIFI_ACCESS_PORT must be numeric (e.g., '12445')."
            )

        # Normalize base URL
        base_url = str(base_url).strip().rstrip('/')
        if not (base_url.startswith('http://') or base_url.startswith('https://')):
            # Default to https if scheme omitted
            base_url = f"https://{base_url}"

        self.base_url = base_url
        self.port = str(port)
        self.api_token = str(api_token).strip()
        self.verify_ssl = verify_ssl
        logger.debug(
            "Initializing UniFiAccessClient base_url=%s port=%s verify_ssl=%s",
            self.base_url,
            self.port,
            self.verify_ssl,
        )
        self.session = httpx.Client(
            verify=self.verify_ssl
        )
        self.session.headers.update({
            'Authorization': f"Bearer {self.api_token}",
        })
        self.session.timeout = int(os.getenv('UNIFI_SESSION_TIMEOUT', 15))
        logger.debug("Session configured: timeout=%s seconds", self.session.timeout)
        self.base_url += f":{self.port}/api/v1"
        logger.debug("Computed base API URL: %s", self.base_url)

        self.users = UserManager(self)
        self.visitors = VisitorManager(self)
        self.access_policies = AccessPolicyManager(self)
        self.credentials = CredentialManager(self)
        self.spaces = SpaceManager(self)
        self.devices = DeviceManager(self)
        self.system_logs = SystemLogManager(self)
        self.https_certificates = HttpsCertificateManager(self)
        self.notifications = NotificationManager(self)
        self.identity = IdentityManager(self)


    def _make_request(self, method, path, raw_response=False, **kwargs):
        """
        Make an HTTP request to the API.

        Args:
            method (str): HTTP method (e.g., 'GET', 'POST').
            path (str): API endpoint path (e.g., '/api/v1/developer/users').
            raw_response (bool): Whether to return the raw response content.
            **kwargs: Additional arguments for requests (e.g., json, params).

        Returns:
            dict, list or bytes: The 'data' field from the API response, or raw bytes if raw_response is True.

        Raises:
            UniFiAccessError: If the API returns an error.
            AuthenticationError: If HTTP 401 is received.
            PermissionError: If HTTP 403 is received.
            RateLimitError: If HTTP 429 is received.
        """
        url = f"{self.base_url}{path}"
        # Prepare safe previews for debug
        params_preview = _preview(kwargs.get('params')) if 'params' in kwargs else None
        json_preview = _preview(kwargs.get('json')) if 'json' in kwargs else None
        logger.debug(
            "HTTP request: %s %s params=%s json=%s",
            method,
            url,
            params_preview,
            json_preview,
        )
        response = self.session.request(method, url, **kwargs)
        logger.debug("HTTP response: %s %s -> %s", method, url, response.status_code)

        if response.status_code != 200:
            if response.status_code == 401:
                raise AuthenticationError("CODE_AUTH_FAILED", "Authentication failed")
            elif response.status_code == 403:
                raise PermissionError("CODE_UNAUTHORIZED", "Permission denied")
            elif response.status_code == 429:
                raise RateLimitError("TOO_MANY_REQUESTS", "Rate limit exceeded")
            else:
                logger.debug(
                    "Non-200 response body preview: %s",
                    _preview(getattr(response, 'text', '')),
                )
                raise UniFiAccessError(f"HTTP_{response.status_code}", response.text)

        if raw_response:
            return response.content

        data = response.json()
        if isinstance(data, dict) and data.get("code") != "SUCCESS":
            logger.debug("API error code=%s msg=%s", data.get("code"), _preview(data.get("msg")))
            raise UniFiAccessError(data.get("code"), data.get("msg"))
        if isinstance(data, list):
            logger.debug("Response data is a list with %d items", len(data))
            return data
        logger.debug("Response data keys: %s", list(data.keys()))
        return data.get("data")

    def process_response(self, response):
        """
        Process an HTTP response from the UniFi Access API.

        Args:
            response (requests.Response): The HTTP response to process.

        Returns:
            dict or list: The 'data' field from the API response.

        Raises:
            UniFiAccessError: If the API returns an error.
            AuthenticationError: If HTTP 401 is received.
            PermissionError: If HTTP 403 is received.
            RateLimitError: If HTTP 429 is received.
        """
        if response.status_code != 200:
            if response.status_code == 401:
                raise AuthenticationError("CODE_AUTH_FAILED", "Authentication failed")
            elif response.status_code == 403:
                raise PermissionError("CODE_UNAUTHORIZED", "Permission denied")
            elif response.status_code == 429:
                raise RateLimitError("TOO_MANY_REQUESTS", "Rate limit exceeded")
            else:
                logger.debug(
                    "process_response non-200: %s body=%s",
                    response.status_code,
                    _preview(getattr(response, 'text', '')),
                )
                raise UniFiAccessError(f"HTTP_{response.status_code}", response.text)

        data = response.json()
        if isinstance(data, dict) and data.get("code") != "SUCCESS":
            logger.debug("process_response API error code=%s msg=%s", data.get("code"), _preview(data.get("msg")))
            raise UniFiAccessError(data.get("code"), data.get("msg"))
        if isinstance(data, list):
            return data
        return data.get("data")

    def check_connection(self):
        try:
            logger.debug("Checking connection via users.fetch_all_users()")
            if self.credentials.generate_pin_code():
                logger.debug("Connection check succeeded")
                return True
            else:
                logger.debug("Connection check returned falsy result")
                return False
        except Exception:
            logger.exception("Connection check failed with exception")
            return False


class AsyncUniFiAccessClient:
    """Async client for interacting with the UniFi Access API."""

    users: UserManager
    visitors: VisitorManager
    access_policies: AccessPolicyManager
    credentials: CredentialManager
    spaces: SpaceManager
    devices: DeviceManager
    system_logs: SystemLogManager
    https_certificates: HttpsCertificateManager
    notifications: NotificationManager

    def __init__(self, base_url, api_token, port='12445', verify_ssl=False, cert_data=None, key_data=None):
        self.base_url = base_url.rstrip('/')
        self.port = port
        self.api_token = api_token
        self.verify_ssl = verify_ssl
        self.cert_data = cert_data
        self.key_data = key_data
        self.headers = {
            'Authorization': f"Bearer {self.api_token}",
            # 'accept': 'application/json',
            # 'content-type': 'application/json'
        }
        logger.debug(
            "Initializing AsyncUniFiAccessClient base_url=%s port=%s verify_ssl=%s",
            self.base_url,
            self.port,
            self.verify_ssl,
        )
        self.session = httpx.AsyncClient(
            headers=self.headers,
            verify=self.verify_ssl,
            timeout=int(os.getenv('UNIFI_SESSION_TIMEOUT', 15)),
        )

        self.base_url += f":{self.port}/api/v1"
        logger.debug("Computed async base API URL: %s", self.base_url)

        self.users = UserManager(self)
        self.visitors = VisitorManager(self)
        self.access_policies = AccessPolicyManager(self)
        self.credentials = CredentialManager(self)
        self.spaces = SpaceManager(self)
        self.devices = DeviceManager(self)
        self.system_logs = SystemLogManager(self)
        self.https_certificates = HttpsCertificateManager(self)
        self.notifications = NotificationManager(self)

    async def _make_request(self, method, path, raw_response=False, **kwargs):
        """
        Make an asynchronous HTTP request to the API.

        Args:
            method (str): HTTP method (e.g., 'GET', 'POST').
            path (str): API endpoint path (e.g., '/api/v1/developer/users').
            raw_response (bool): Whether to return the raw response content.
            **kwargs: Additional arguments for requests (e.g., json, params).

        Returns:
            dict, list or bytes: The 'data' field from the API response, or raw bytes if raw_response is True.

        Raises:
            UniFiAccessError: If the API returns an error.
            AuthenticationError: If HTTP 401 is received.
            PermissionError: If HTTP 403 is received.
            RateLimitError: If HTTP 429 is received.
        """
        url = f"{self.base_url}{path}"
        params_preview = _preview(kwargs.get('params')) if 'params' in kwargs else None
        json_preview = _preview(kwargs.get('json')) if 'json' in kwargs else None
        logger.debug(
            "HTTP async request: %s %s params=%s json=%s",
            method,
            url,
            params_preview,
            json_preview,
        )
        response = await self.session.request(method, url, **kwargs)
        logger.debug("HTTP async response: %s %s -> %s", method, url, response.status_code)

        if response.status_code != 200:
            if response.status_code == 401:
                raise AuthenticationError("CODE_AUTH_FAILED", "Authentication failed")
            elif response.status_code == 403:
                raise PermissionError("CODE_UNAUTHORIZED", "Permission denied")
            elif response.status_code == 429:
                raise RateLimitError("TOO_MANY_REQUESTS", "Rate limit exceeded")
            else:
                logger.debug(
                    "Async non-200 response body preview: %s",
                    _preview(getattr(response, 'text', '')),
                )
                raise UniFiAccessError(f"HTTP_{response.status_code}", response.text)

        if raw_response:
            return response.content

        data = response.json()
        if isinstance(data, dict) and data.get("code") != "SUCCESS":
            logger.debug("Async API error code=%s msg=%s", data.get("code"), _preview(data.get("msg")))
            raise UniFiAccessError(data.get("code"), data.get("msg"))
        if isinstance(data, list):
            return data
        return data.get("data")

    async def process_response(self, response):
        if response.status_code != 200:
            if response.status_code == 401:
                raise AuthenticationError("CODE_AUTH_FAILED", "Authentication failed")
            elif response.status_code == 403:
                raise PermissionError("CODE_UNAUTHORIZED", "Permission denied")
            elif response.status_code == 429:
                raise RateLimitError("TOO_MANY_REQUESTS", "Rate limit exceeded")
            else:
                logger.debug(
                    "async process_response non-200: %s body=%s",
                    response.status_code,
                    _preview(getattr(response, 'text', '')),
                )
                raise UniFiAccessError(f"HTTP_{response.status_code}", response.text)

        data = response.json()
        if isinstance(data, dict) and data.get("code") != "SUCCESS":
            logger.debug("async process_response API error code=%s msg=%s", data.get("code"), _preview(data.get("msg")))
            raise UniFiAccessError(data.get("code"), data.get("msg"))
        if isinstance(data, list):
            return data
        return data.get("data")

    async def check_connection(self):
        try:
            logger.debug("Async checking connection via credentials.generate_pin_code()")
            pin_code = self.credentials.generate_pin_code()
            ok = bool(pin_code)
            logger.debug("Async connection check result: %s", ok)
            return ok
        except Exception:
            logger.exception("Async connection check failed with exception")
            return False
