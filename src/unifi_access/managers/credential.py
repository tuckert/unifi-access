import csv
import io
from typing import Any, Dict, List, Optional, TYPE_CHECKING
from unifi_access.utils import encode_w26_24bit, decode_w26_24bit_hex

if TYPE_CHECKING:
    from ..client import UniFiAccessClient


class CredentialManager:
    """High-level manager for credential operations (PIN codes, NFC cards).

    This manager wraps UniFi Access Developer API endpoints related to
    credentials. All HTTP I/O is delegated to the provided `client` which must
    expose a private method `_make_request(method, path, ...)`.

    Notes for LLMs/MCP:
    - Return values mirror the UniFi Access API responses where possible.
    - IDs/tokens are strings provided by the UniFi backend.
    """

    def __init__(self, client: Any) -> None:
        """Initialize the manager.

        Args:
            client: Low-level HTTP client with a `_make_request` method.
        """
        self.client = client

    def generate_pin_code(self) -> Dict[str, Any]:
        """Generate a new PIN code.

        Returns:
            Generated PIN code details, e.g., {"pin_code": "123456"}.

        Notes:
            - Request URL: /developer/credentials/pin-code
            - Permission Key: edit:credential
            - Method: POST
        """
        path = "/developer/credentials/pin_codes"
        return self.client._make_request("POST", path)

    def enroll_nfc_card(self, device_id: str) -> Dict[str, Any]:
        """Enroll an NFC card for a specific device.

        Args:
            device_id: Target device ID (e.g., UA-Hub or reader) to enroll on.

        Returns:
            Enrollment session details (e.g., session ID and token).

        Notes:
            - Request URL: /developer/credentials/nfc-card/enrollment
            - Permission Key: edit:credential
            - Method: POST
        """
        path = "/developer/credentials/nfc-card/enrollment"
        data = {"device_id": device_id}
        return self.client._make_request("POST", path, json=data)

    def fetch_nfc_card_enrollment_status(self, session_id: str) -> Dict[str, Any]:
        """Fetch the enrollment status of an NFC card.

        Args:
            session_id: Session ID returned from `enroll_nfc_card`.

        Returns:
            Enrollment status details, e.g., {"status": "completed", "token": "nfc-token"}.

        Notes:
            - Request URL: /developer/credentials/nfc-card/enrollment/:session_id
            - Permission Key: view:credential
            - Method: GET
        """
        path = f"/developer/credentials/nfc_cards/sessions/{session_id}"
        return self.client._make_request("GET", path)

    def remove_session_created_for_nfc_card_enrollment(self, session_id: str) -> Dict[str, Any]:
        """Remove an NFC card enrollment session.

        Args:
            session_id: The session ID to remove.

        Returns:
            API response body (may be empty depending on API behavior).

        Notes:
            - Request URL: /developer/credentials/nfc-card/enrollment/:session_id
            - Permission Key: edit:credential
            - Method: DELETE
        """
        path = f"/developer/credentials/nfc_cards/sessions/{session_id}"
        return self.client._make_request("DELETE", path)

    def fetch_nfc_card(self, nfc_card_token: str) -> Dict[str, Any]:
        """Fetch details of an NFC card by token.

        Args:
            nfc_card_token: The NFC card's token.

        Returns:
            NFC card data as a dictionary.

        Notes:
            - Request URL: /developer/nfc-cards/:id
            - Permission Key: view:credential
            - Method: GET
        """
        path = f"/developer/credentials/nfc_cards/tokens/{nfc_card_token}"
        return self.client._make_request("GET", path)

    def fetch_all_nfc_cards(self) -> List[Dict[str, Any]]:
        """Fetch all NFC cards (token summaries).

        Returns:
            A list of NFC card data dictionaries.

        Notes:
            - Request URL: /developer/nfc-cards
            - Permission Key: view:credential
            - Method: GET
        """
        path = "/developer/credentials/nfc_cards/tokens"
        return self.client._make_request("GET", path)
    def list_nfc_cards(self) -> List[Dict[str, Any]]:
        return self.fetch_all_nfc_cards()

    def update_nfc_card(self, nfc_card_token: str, alias: str) -> Dict[str, Any]:
        """Update an NFC card's Alias."""
        path = f"/developer/credentials/nfc_cards/tokens/{nfc_card_token}"
        data = {"alias": alias}
        return self.client._make_request("PUT", path, json=data)

    def delete_nfc_card(self, nfc_card_token: str) -> Dict[str, Any]:
        """Delete an NFC card.

        Args:
            nfc_card_token: The NFC card's token.

        Returns:
            API response body (may be empty depending on API behavior).

        Notes:
            - Request URL: /developer/nfc-cards/:id
            - Permission Key: edit:credential
            - Method: DELETE
        """
        path = f"/developer/credentials/nfc_cards/tokens/{nfc_card_token}"
        return self.client._make_request("DELETE", path)

    def fetch_the_touch_pass_list(self,
                                  page_num: Optional[int] = None,
                                  page_size: Optional[int] = None,
                                  status: Optional[str] = None,
                                  ):
        path = "/developer/credentials/touch_passes"
        params = {}
        if page_num:
            params["page_num"] = page_num
        if page_size:
            params["page_size"] = page_size
        if status:
            params["status"] = status
        return self.client._make_request("GET", path, params=params)

    def search_touch_pass(self, condition: str):
        path = "/developer/credentials/touch_passes/search"
        params = {"condition": condition}
        return self.client._make_request("GET", path, params=params)

    def fetch_all_assignable_touch_passes(self):
        path = "/developer/credentials/touch_passes/assignable"
        return self.client._make_request("GET", path)

    def update_touch_pass(self, touch_pass_id: str, card_name: Optional[str], status: Optional[str], bundles: Optional[List[Dict[str, Any]]]):
        path = f"/developer/credentials/touch_passes/{touch_pass_id}"
        data = {"status": status}
        if card_name:
            data["card_name"] = card_name
        if bundles:
            data["bundles"] = bundles
        return self.client._make_request("PUT", path, json=data)

    def fetch_touch_pass_details(self, touch_pass_id: str):
        path = f"/developer/credentials/touch_passes/{touch_pass_id}"
        return self.client._make_request("GET", path)

    def purchase_touch_passes(self, count: int):
        path = f"/developer/credentials/touch_passes"
        params = {"count": count}
        return self.client._make_request("POST", path, params=params)

    def download_qr_code_image(self, visitor_id: str):
        path = f"/developer/credentials/touch_passes/qr_codes/{visitor_id}"
        return self.client._make_request("GET", path)

    def import_third_party_nfc_cards(self, file_path: str):
        path = "/developer/credentials/nfc_cards/import"
        with open(file_path, "rb") as f:
            files = {"file": f}
            return self.client._make_request("POST", path, files=files)

    def import_third_party_nfc_cards_as_list(self, nfc_cards: List[Dict[str, Any]]):
        """Import third-party NFC cards from a list of dictionaries.

        Args:
            nfc_cards: A list of dicts with keys "nfc_id" and "alias".
        """
        path = "/developer/credentials/nfc_cards/import"
        output = io.StringIO()
        writer = csv.writer(output)
        for card in nfc_cards:
            writer.writerow([card["nfc_id"], card["alias"]])
        
        file_content = output.getvalue().encode('utf-8')

        files = {"file": ('nfc_cards.csv', io.BytesIO(file_content), 'text/csv')}
        return self.client._make_request("POST", path, files=files)


    def import_26bit_wiegand_cards(self, cards: List[Dict[str, Any]]):
        """Import 26-bit Wiegand cards from a list of dictionaries.

        Args:
            cards: A list of dicts with keys "facility" and "card".
        """

        for card in cards:
            card["nfc_id"] = encode_w26_24bit(card["facility_code"], card["card_number"])
            card['alias'] = f'{card["facility_code"]} - {card["card_number"]}'

        return self.import_third_party_nfc_cards_as_list(cards)
