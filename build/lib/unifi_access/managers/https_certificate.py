from typing import Any, Dict


class HttpsCertificateManager:
    """Manager for uploading and deleting HTTPS certificates for the API server.

    All HTTP I/O is delegated to `client` which must expose
    `_make_request(method, path, ...)`.
    """

    def __init__(self, client: Any) -> None:
        """Initialize the manager.

        Args:
            client: Low-level HTTP client with a `_make_request` method.
        """
        self.client = client

    def upload_https_certificate(self, key: Any, cert: Any) -> Dict[str, Any]:
        """Upload HTTPS key and cert for the UniFi Access API server.

        Args:
            key: Private key payload/file handle as expected by requests `files`.
            cert: Certificate payload/file handle as expected by requests `files`.

        Returns:
            API response body as a dictionary.

        Notes:
            - Request URL: /developer/api_server/certificates
            - Permission Key: edit:api_server
            - Method: POST
        """
        path = "/developer/api_server/certificates"
        files = {
            "key": key,
            "cert": cert
        }
        data = {
            "key": key,
            "cert": cert
        }
        print(files)
        result = self.client._make_request("POST", path, files=files)
        print(result)
        return result

    def delete_https_certificate(self) -> Dict[str, Any]:
        """Delete the configured HTTPS certificate from the API server.

        Returns:
            API response body (may be empty depending on API behavior).

        Notes:
            - Request URL: /developer/api_server/certificates/
            - Permission Key: edit:api_server
            - Method: DELETE
        """
        path = "/developer/api_server/certificates/"
        return self.client._make_request("DELETE", path)