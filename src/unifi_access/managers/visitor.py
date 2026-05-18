import datetime
from typing import Any, Dict, List, Optional, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import UniFiAccessClient


class VisitorManager:
    """High-level manager for UniFi Access visitor-related operations.

    This class wraps UniFi Access Developer API endpoints for creating,
    updating, and managing visitors and their credentials (NFC cards and PINs).
    All HTTP I/O is delegated to the provided `client` which must expose a
    private method `_make_request(method, path, ...)`.

    Notes for LLMs/MCP:
    - Return values generally mirror the UniFi Access API responses.
    - Unless otherwise noted, IDs are strings provided by the UniFi backend.
    - Pagination parameters are optional; when omitted, server defaults apply.
    """

    def __init__(self, client: Any) -> None:
        """Initialize the manager.

        Args:
            client: Low-level HTTP client with a `_make_request` method.
        """
        self.client = client

    def create_visitor(
            self,
            first_name: str,
            last_name: str,
            start_time: int,
            end_time: int,
            remarks: Optional[str] = None,
            mobile_phone: Optional[str] = None,
            email: Optional[str] = None,
            visitor_company: Optional[str] = None,
            visit_reason: str = "Others",
            resources: Optional[List] = None,
            week_schedule: Optional[List] = None,
            **kwargs: Any,
    ) -> Dict[str, Any]:
        """Create/register a new visitor.

        Args:
            first_name: Visitor's first name.
            last_name: Visitor's last name.
            start_time: ISO-8601 (no timezone) Example: "2025-12-25T17:00:00".
            end_time: ISO-8601 (no timezone) Example: "2025-12-25T17:00:00".
            remarks: Optional remarks/notes about the visitor.
            mobile_phone: Optional phone number.
            company_name: Optional company name associated with the visitor.
            email: Optional visitor email.
            visitor_company: Optional visitor company name (if different).

            visit_reason: Optional Default "Others", options: "Interview", "Business", "Cooperation", "Others".
            resources: List of doors or door groups and IDs obtained from "spaces" manager.  Example: [{"id": "9bee6e0e-108d4c52-9107-76f2c7dea4f1", "type": "door"}]
            week_schedule: Optional weekly schedule. The customizable scheduling strategy for each day from Sunday to Saturday. If not specified, it means access is allowed every day.
                Example week_schedule: {"sunday": [], "monday": [{"start_time": "10:00:00", "end_time": "17:00:59"}], "tuesday": [], "wednesday": [], "thursday": [], "friday": [], "saturday": []}
            **kwargs: Optional Additional fields that may be supported by the API.

        Returns:
            Visitor data as a dictionary.
        """
        path = "/developer/visitors"
        data = {
            'first_name': first_name,
            'last_name': last_name,
            'remarks': remarks,
            'mobile_phone': mobile_phone,
            "email": email,
            'visitor_company': visitor_company,
            'start_time': start_time,
            'end_time': end_time,
            'visit_reason': visit_reason,
            'resources': resources,
            'week_schedule': week_schedule,
        }

        return self.client._make_request("POST", path, json=data)

    def update_visitor(
            self,
            visitor_id: str,
            first_name: Optional[str] = None,
            last_name: Optional[str] = None,
            remarks: Optional[str] = None,
            mobile_phone: Optional[str] = None,
            company_name: Optional[str] = None,
            email: Optional[str] = None,
            visitor_company: Optional[str] = None,
            start_time: Optional[str] = None,
            end_time: Optional[str] = None,
            visit_reason: Optional[str] = None,
            resources: Optional[List] = None,
            week_schedule: Optional[List] = None,
            **kwargs: Any,
        ) -> Dict[str, Any]:
        """Update visitor details.

        Args:
            visitor_id: Target visitor's ID.
            first_name: New first name.
            last_name: New last name.
            remarks: Optional remarks/notes.
            mobile_phone: Optional phone number.
            company_name: Optional company name.
            email: Optional visitor email.
            visitor_company: Optional visitor company name.
            start_time: Optional new start time.
            end_time: Optional new end time.
            visit_reason: Optional new reason for visit.
            resources: Optional updated resources structure.
            week_schedule: Optional updated weekly schedule.
            **kwargs: Additional fields that may be supported by the API.

        Returns:
            Updated visitor data as a dictionary.
        """
        path = f"/developer/visitors/{visitor_id}"
        data = {
            'first_name': first_name,
            'last_name': last_name,
            'remarks': remarks,
            'mobile_phone': mobile_phone,
            "email": email,
            'visitor_company': visitor_company,
            'start_time': start_time,
            'end_time': end_time,
            'visit_reason': visit_reason,
            'resources': resources,
            'week_schedule': week_schedule,
        }
        return self.client._make_request("PUT", path, json=data)


    def fetch_visitor(self, visitor_id: str) -> Dict[str, Any]:
        """Fetch a visitor's details.

        Args:
            visitor_id: The visitor's ID.

        Returns:
            Visitor data as a dictionary.

        Notes:
            - Request URL: /developer/visitors/:id
            - Permission Key: view:visitor
            - Method: GET
        """
        path = f"/developer/visitors/{visitor_id}"
        return self.client._make_request("GET", path)

    def fetch_all_visitors(
        self,
        page_num: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Fetch all visitors with optional pagination.

        Args:
            page_num: Page number (server default if omitted).
            page_size: Number of visitors per page (server default if omitted).

        Returns:
            A list of visitor data dictionaries.

        Notes:
            - Request URL: /developer/visitors
            - Permission Key: view:visitor
            - Method: GET
        """
        path = "/developer/visitors"
        params = {
            "page_num": page_num,
            "page_size": page_size
        }
        return self.client._make_request("GET", path, params=params)

    list_visitors = fetch_all_visitors


    def delete_visitor(
            self,
            visitor_id: str,
            is_force: Literal["true", "false"] = 'true',
    ) -> Dict[str, Any]:
        """Delete a visitor.

        Args:
            visitor_id: The visitor's ID.
            is_force: If true, physically delete this visitor; otherwise, update to canceled status. Default: true

        Returns:
            API response body (may be empty depending on API behavior).

        Notes:
            - Request URL: /developer/visitors/:id
            - Permission Key: edit:visitor
            - Method: DELETE
        """
        path = f"/developer/visitors/{visitor_id}"
        data = {"is_force": is_force}
        return self.client._make_request("DELETE", path, params=data)

    def assign_nfc_card_to_visitor(self, visitor_id: str, nfc_token: str) -> Dict[str, Any]:
        """Assign an NFC card to a visitor.

        Args:
            visitor_id: The visitor's ID.
            nfc_token: The NFC card token to assign.

        Returns:
            API response body as a dictionary.

        Notes:
            - Request URL: /developer/visitors/:id/nfc-card
            - Permission Key: edit:visitor
            - Method: POST
        """
        path = f"/developer/visitors/{visitor_id}/nfc-card"
        data = {"token": nfc_token}
        return self.client._make_request("POST", path, json=data)

    def unassign_nfc_card_from_visitor(self, visitor_id: str, nfc_token: str) -> Dict[str, Any]:
        """Unassign an NFC card from a visitor.

        Args:
            visitor_id: The visitor's ID.
            nfc_token: The NFC card token to unassign.

        Returns:
            API response body as a dictionary.

        Notes:
            - Request URL: /developer/visitors/:id/nfc-card
            - Permission Key: edit:visitor
            - Method: DELETE
        """
        path = f"/developer/visitors/{visitor_id}/nfc-card"
        data = {"token": nfc_token}
        return self.client._make_request("DELETE", path, json=data)

    def assign_pin_code_to_visitor(self, visitor_id: str, pin_code: str) -> Dict[str, Any]:
        """Assign a PIN code to a visitor.

        Args:
            visitor_id: The visitor's ID.
            pin_code: The PIN code to assign (hash or plain text, depending on API).

        Returns:
            API response body as a dictionary.

        Notes:
            - Request URL: /developer/visitors/:id/pin-code
            - Permission Key: edit:visitor
            - Method: POST
        """
        path = f"/developer/visitors/{visitor_id}/pin_codes"
        data = {"pin_code": pin_code}
        return self.client._make_request("PUT", path, json=data)

    def unassign_pin_code_from_visitor(self, visitor_id: str) -> Dict[str, Any]:
        """Unassign/remove a PIN code from a visitor.

        Args:
            visitor_id: The visitor's ID.

        Returns:
            API response body as a dictionary.

        Notes:
            - Request URL: /developer/visitors/:id/pin-code
            - Permission Key: edit:visitor
            - Method: DELETE
        """
        path = f"/developer/visitors/{visitor_id}/pin-code"
        return self.client._make_request("DELETE", path)

    def assign_qr_code_to_visitor(self, visitor_id: str) -> None:
        """Assign a QR code to a visitor."""
        path = f"/developer/visitors/{visitor_id}/qr-codes"
        return self.client._make_request("PUT", path)

    def unassign_qr_code_from_visitor(self, visitor_id: str) -> None:
        """Unassign/remove a QR code from a visitor."""
        path = f"/developer/visitors/{visitor_id}/qr-codes"
        return self.client._make_request("DELETE", path)

    def assign_license_plate_numbers_to_visitor(self, visitor_id: str, numbers: List[str]):
        path = f"/developer/visitors/{visitor_id}/license_plates"
        data = {"numbers": numbers}
        return self.client._make_request("PUT", path, json=data)

    def unassign_license_plate_numbers_from_visitor(self, visitor_id: str, license_plate_id: str):
        path = f"/developer/visitors/{visitor_id}/license_plates/{license_plate_id}"
        return self.client._make_request("DELETE", path)