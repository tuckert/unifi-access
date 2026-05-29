from typing import Any, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import UniFiAccessClient


class UserManager:
    """High-level manager for UniFi Access user-related operations.

    This class wraps the UniFi Access Developer API endpoints related to users
    and user groups. All methods delegate HTTP I/O to the provided `client`,
    which must expose a private method `'_make_request(method, path, ...)`.

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


    def create_user(
        self,
        first_name: str,
        last_name: str,
        user_email: Optional[str] = None,
        employee_number: Optional[str] = None,
        onboard_time: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Create/register a new user.

        Args:
            first_name: User's first name.
            last_name: User's last name.
            user_email: Optional user email address.
            employee_number: Optional external employee number.
            onboard_time: Optional onboarding timestamp (Unix epoch seconds).

        Returns:
            API response body as a dictionary.

        Notes:
            - Request URL: /developer/users
            - Permission Key: edit:user
            - Method: POST
        """
        path = "/developer/users"
        data = {
            "first_name": first_name,
            "last_name": last_name
        }
        if user_email:
            data["user_email"] = user_email
        if employee_number:
            data["employee_number"] = employee_number
        if onboard_time:
            data["onboard_time"] = onboard_time

        return self.client._make_request("POST", path, json=data)

    def update_user(self, user_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Update user details.

        Args:
            user_id: Target user's ID.
            **kwargs: Updatable fields. Supported keys: `first_name`,
                `last_name`, `user_email`, `employee_number`, `status`.

        Returns:
            Updated user data as a dictionary.

        Notes:
            - Request URL: /developer/users/:id
            - Permission Key: edit:user
            - Method: PUT
        """
        path = f"/developer/users/{user_id}"
        allowed_fields = ["first_name", "last_name", "user_email", "employee_number", "status"]
        data = {k: v for k, v in kwargs.items() if k in allowed_fields}
        return self.client._make_request("PUT", path, json=data)

    def fetch_user(self, user_id: str, include_access_policies: bool = False) -> Dict[str, Any]:
        """Fetch a user's details.

        Args:
            user_id: The user's ID.
            include_access_policies: Whether to expand and include assigned
                access policies in the response.

        Returns:
            User data as a dictionary.

        Notes:
            - Request URL: /developer/users/:id
            - Permission Key: view:user
            - Method: GET
        """
        path = f"/developer/users/{user_id}"
        params = {"expand[]": "access_policy"} if include_access_policies else {}
        return self.client._make_request("GET", path, params=params)

    def fetch_all_users(
        self,
        page_num: Optional[int] = None,
        page_size: Optional[int] = None,
        include_access_policies: bool = False,
    ) -> List[Dict[str, Any]]:
        """Fetch all users with optional pagination.

        Args:
            page_num: Page number (server default if omitted).
            page_size: Number of users per page (server default if omitted).
            include_access_policies: Whether to expand and include access
                policies for each user in the response.

        Returns:
            A list of user data dictionaries.

        Notes:
            - Request URL: /developer/users
            - Permission Key: view:user
            - Method: GET
        """
        path = "/developer/users"
        params = {
            "page_num": page_num,
            "page_size": page_size
        }
        if include_access_policies:
            params["expand[]"] = "access_policy"
        return self.client._make_request("GET", path, params=params)

    def delete_user(self, user_id: str) -> Dict[str, Any]:
        """Delete a user.

        Args:
            user_id: The user's ID.

        Returns:
            API response body (may be empty depending on API behavior).

        Notes:
            - Request URL: /developer/users/:id
            - Permission Key: edit:user
            - Method: DELETE
        """
        path = f"/developer/users/{user_id}"
        return self.client._make_request("DELETE", path)

    def search_users(
            self,
            keyword: Optional[str] = None,
            user_id: Optional[str] = None,
            only_admin: Optional[bool] = None,
            status: Optional[str] = None,
            page_num: Optional[int] = None,
            page_size: Optional[int] = None,
        ) -> List[Dict[str, Any]]:
        """Search users by keyword and filters.

        Args:
            keyword: Free-text search keyword.
            user_id: Filter by a specific user ID.
            only_admin: If true, return only admin users.
            status: Filter by user status (e.g., 'ACTIVE', 'INACTIVE').
            page_num: Optional page number.
            page_size: Optional page size.

        Returns:
            A list of matching user data dictionaries.

        Notes:
            - Request URL: /developer/users/search
            - Permission Key: view:user
            - Method: GET
        """
        path = "/developer/users/search"
        params = {}
        if keyword:
            params["keyword"] = keyword
        if user_id:
            params["user_id"] = user_id
        if only_admin:
            params["only_admin"] = only_admin
        if status:
            params["status"] = status
        if page_num:
            params["page_num"] = page_num
        if page_size:
            params["page_size"] = page_size
        return self.client._make_request("GET", path, params=params)


    def assign_access_policy_to_user(self, user_id: str, access_policy_ids: List[str]) -> Dict[str, Any]:
        """Assign one or more access policies to a user.

        Args:
            user_id: Target user's ID.
            access_policy_ids: List of access policy IDs to assign.

        Returns:
            API response body as a dictionary.

        Notes:
            - Request URL: /developer/users/:id/access_policies
            - Permission Key: edit:user
            - Method: PUT
        """
        path = f"/developer/users/{user_id}/access_policies"
        data = {
            "access_policy_ids": access_policy_ids
        }
        return self.client._make_request("PUT", path, json=data)

    def assign_nfc_card_to_user(self, user_id: str, card_token: str, force_add: bool = True) -> Dict[str, Any]:
        """Assign or add an NFC card to a user.

        Args:
            user_id: Target user's ID.
            card_token: NFC card token.
            force_add: If true, force adding even if the card is in use.

        Returns:
            API response body as a dictionary.

        Notes:
            - Request URL: /developer/users/:id/nfc_cards
            - Permission Key: edit:user
            - Method: PUT
        """
        path = f"/developer/users/{user_id}/nfc_cards"
        data = {
            "token": card_token,
            "force_add": force_add
        }
        return self.client._make_request("PUT", path, json=data)

    def unassign_nfc_card_from_user(self, user_id: str, card_token: str) -> Dict[str, Any]:
        """Unassign an NFC card from a user.

        Args:
            user_id: Target user's ID.
            card_token: NFC card token to remove.

        Returns:
            API response body as a dictionary.

        Notes:
            - Request URL: /developer/users/:id/nfc_cards/delete
            - Permission Key: edit:user
            - Method: PUT
        """
        path = f"/developer/users/{user_id}/nfc_cards/delete"
        data = {
            "token": card_token
        }
        return self.client._make_request("PUT", path, json=data)

    def assign_pin_code_to_user(self, user_id: str, pin_code: str) -> Dict[str, Any]:
        """Assign a PIN code to a user.

        Args:
            user_id: Target user's ID.
            pin_code: The PIN code to assign.

        Returns:
            API response body as a dictionary.

        Notes:
            - Request URL: /developer/users/:id/pin_codes
            - Permission Key: edit:user
            - Method: PUT
        """
        path = f"/developer/users/{user_id}/pin_codes"
        data = {
            "pin_code": pin_code
        }
        return self.client._make_request("PUT", path, json=data)

    def unassign_pin_code_from_user(self, user_id: str) -> Dict[str, Any]:
        """Remove/unassign the PIN code from a user.

        Args:
            user_id: Target user's ID.

        Returns:
            API response body as a dictionary.

        Notes:
            - Request URL: /developer/users/:id/pin_codes
            - Permission Key: edit:user
            - Method: DELETE
        """
        path = f"/developer/users/{user_id}/pin_codes"
        return self.client._make_request("DELETE", path)

    def create_user_group(self, name: str, up_id: Optional[str] = None) -> Dict[str, Any]:
        """Create a new user group.

        Args:
            name: Group name.
            up_id: Optional upstream ID.

        Returns:
            User group data as a dictionary.

        Notes:
            - Request URL: /developer/user_groups
            - Permission Key: edit:user_group
            - Method: POST
            - UniFi Access Requirement: Version 2.2.6 or later
        """
        path = "/developer/user_groups"
        data = {
            "name": name
        }
        if up_id:
            data["up_id"] = up_id
        return self.client._make_request("POST", path, json=data)

    def fetch_all_user_groups(self) -> List[Dict[str, Any]]:
        """Fetch all user groups.

        Returns:
            A list of user group data dictionaries.

        Notes:
            - Request URL: /developer/user_groups
            - Permission Key: view:user_group
            - Method: GET
            - UniFi Access Requirement: Version 2.2.6 or later
        """
        path = "/developer/user_groups"
        return self.client._make_request("GET", path)

    def fetch_user_group(self, group_id: str) -> Dict[str, Any]:
        """Fetch a specific user group by ID.

        Args:
            group_id: User group ID.

        Returns:
            User group data as a dictionary.

        Notes:
            - Request URL: /developer/user_groups/:id
            - Permission Key: view:user_group
            - Method: GET
            - UniFi Access Requirement: Version 2.2.6 or later
        """
        path = f"/developer/user_groups/{group_id}"
        return self.client._make_request("GET", path)

    def update_user_group(
        self,
        group_id: str,
        name: Optional[str] = None,
        up_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update a user group.

        Args:
            group_id: Target user group ID.
            name: New group name (optional).
            up_id: New upstream ID (optional).

        Returns:
            Updated user group data as a dictionary.

        Notes:
            - Request URL: /developer/user_groups/:id
            - Permission Key: edit:user_group
            - Method: PUT
            - UniFi Access Requirement: Version 2.2.6 or later
        """
        path = f"/developer/user_groups/{group_id}"
        data = {}
        if name:
            data["name"] = name
        if up_id:
            data["up_id"] = up_id
        return self.client._make_request("PUT", path, json=data)

    def delete_user_group(self, group_id: str) -> Dict[str, Any]:
        """Delete a user group.

        Args:
            group_id: User group ID.

        Returns:
            API response body (may be empty depending on API behavior).

        Notes:
            - Request URL: /developer/user_groups/:id
            - Permission Key: edit:user_group
            - Method: DELETE
            - UniFi Access Requirement: Version 2.2.6 or later
        """
        path = f"/developer/user_groups/{group_id}"
        return self.client._make_request("DELETE", path)

    def assign_users_to_user_group(self, group_id: str, user_ids: List[str]) -> Dict[str, Any]:
        """Assign users to a user group.

        Args:
            group_id: User group ID.
            user_ids: List of user IDs to assign.

        Returns:
            API response body as a dictionary.

        Notes:
            - Request URL: /developer/user_groups/:id/users
            - Permission Key: edit:user_group
            - Method: POST
            - UniFi Access Requirement: Version 2.2.6 or later
        """
        path = f"/developer/user_groups/{group_id}/users"
        data = user_ids
        return self.client._make_request("POST", path, json=data)

    def unassign_users_from_user_group(self, group_id: str, user_ids: List[str]) -> Dict[str, Any]:
        """Unassign users from a user group.

        Args:
            group_id: User group ID.
            user_ids: List of user IDs to remove from the group.

        Returns:
            API response body as a dictionary.

        Notes:
            - Request URL: /developer/user_groups/:id/users/delete
            - Permission Key: edit:user_group
            - Method: POST
            - UniFi Access Requirement: Version 2.2.6 or later
        """
        path = f"/developer/user_groups/{group_id}/users/delete"
        data = user_ids
        return self.client._make_request("POST", path, json=data)

    def fetch_users_in_a_user_group(self, group_id: str) -> List[Dict[str, Any]]:
        """Fetch users currently assigned to a specific group.

        Args:
            group_id: User group ID.

        Returns:
            A list of user data dictionaries.

        Notes:
            - Request URL: /developer/user_groups/:id/users
            - Permission Key: view:user_group
            - Method: GET
            - UniFi Access Requirement: Version 2.2.6 or later
        """
        path = f"/developer/user_groups/{group_id}/users"
        return self.client._make_request("GET", path)

    def fetch_all_users_in_a_user_group(self, group_id: str) -> List[Dict[str, Any]]:
        """Fetch all users in a group, bypassing pagination if supported.

        Args:
            group_id: User group ID.

        Returns:
            A list of user data dictionaries.

        Notes:
            - Request URL: /developer/user_groups/:id/users/all
            - Permission Key: view:user_group
            - Method: GET
            - UniFi Access Requirement: Version 2.2.6 or later
        """
        path = f"/developer/user_groups/{group_id}/users/all"
        return self.client._make_request("GET", path)

    def fetch_access_policies_assigned_to_user(
        self,
        user_id: str,
        only_user_policies: str = 'false',
    ) -> List[Dict[str, Any]]:
        """Fetch access policies assigned to a user.

        Args:
            user_id: Target user's ID.
            only_user_policies: Pass 'true' to include only user-specific
                policies; 'false' to include inherited policies as well.

        Returns:
            A list of access policy data dictionaries.

        Notes:
            - Request URL: /developer/users/:id/access_policies
            - Permission Key: view:user
            - Method: GET
        """
        path = f"/developer/users/{user_id}/access_policies"
        data = {
            "only_user_policies": only_user_policies
        }
        return self.client._make_request("GET", path, params=data)

    def assign_access_policy_to_user_group(self, group_id: str, access_policy_ids: List[str]) -> Dict[str, Any]:
        """Assign one or more access policies to a user group.

        Args:
            group_id: User group ID.
            access_policy_ids: List of access policy IDs to assign.

        Returns:
            API response body as a dictionary.

        Notes:
            - Request URL: /developer/user_groups/:id/access_policies
            - Permission Key: edit:user_group
            - Method: PUT
            - UniFi Access Requirement: Version 2.2.6 or later
        """
        path = f"/developer/user_groups/{group_id}/access_policies"
        data = {
            "access_policy_ids": access_policy_ids
        }
        return self.client._make_request("PUT", path, json=data)

    def fetch_access_policies_assigned_to_user_group(self, group_id: str) -> List[Dict[str, Any]]:
        """Fetch access policies assigned to a specific user group.

        Args:
            group_id: User group ID.

        Returns:
            A list of access policy data dictionaries.

        Notes:
            - Request URL: /developer/user_groups/:id/access_policies
            - Permission Key: view:user_group
            - Method: GET
            - UniFi Access Requirement: Version 2.2.6 or later
        """
        path = f"/developer/user_groups/{group_id}/access_policies"
        return self.client._make_request("GET", path)

    def assign_touch_pass_to_user(self, user_id: str, touch_pass_id: str) -> Dict[str, Any]:
        """Assign a touch pass to a user.

        Args:
            user_id: Target user's ID.
            touch_pass_id: Touch pass ID to assign.

        Returns:
            API response body as a dictionary.

        Notes:
            - Request URL: /developer/users/:id/touch_passes/:touch_pass_id
            - Permission Key: edit:user
            - Method: PUT
        """
        path = f"/developer/users/{user_id}/touch_passes/{touch_pass_id}"
        return self.client._make_request("PUT", path)

    def unassign_touch_pass_from_user(self, user_id: str, touch_pass_id: str) -> Dict[str, Any]:
        """Unassign/remove a touch pass from a user.

        Args:
            user_id: Target user's ID.
            touch_pass_id: Touch pass ID to remove.

        Returns:
            API response body as a dictionary.

        Notes:
            - Request URL: /developer/users/:id/touch_passes/:touch_pass_id
            - Permission Key: edit:user
            - Method: DELETE
        """
        path = f"/developer/users/{user_id}/touch_passes/{touch_pass_id}"
        return self.client._make_request("DELETE", path)

    def batch_assign_touch_passes_to_users(self, user_ids: List[str], emails: Optional[List[Dict[str, str]]]) -> Dict[str, Any]:
        """Assigning unassigned Touch Passes to users using their email addresses.

        Args:
            user_ids: List of user IDs.
            emails: Optional list of email dictionaries.

        Returns:
            API response body as a dictionary.

        Notes:
            - Request URL: /developer/users/touch_passes/assign
            - Permission Key: edit:user
            - Method: PUT
        """
        path = "/developer/users/touch_passes/assign"
        data = {
            "user_ids": user_ids,
        }
        if emails:
            data["emails"] = emails
        return self.client._make_request("PUT", path, json=data)

    def assign_license_plate_numbers_to_user(self, user_id: str, license_plate_numbers: List[str]) -> Dict[str, Any]:
        """Assign license plate numbers to a user.

        Args:
            user_id: Target user's ID.
            license_plate_numbers: List of license plate numbers.

        Returns:
            API response body as a dictionary.

        Notes:
            - Request URL: /developer/users/:id/license_plates
            - Permission Key: edit:user
            - Method: PUT
        """
        path = f"/developer/users/{user_id}/license_plates"
        return self.client._make_request("PUT", path, json=license_plate_numbers)

    def unassign_license_plate_number_from_user(self, user_id: str, license_plate_id: str) -> Dict[str, Any]:
        """Unassign a license plate number from a user.

        Args:
            user_id: Target user's ID.
            license_plate_id: License plate ID to remove.

        Returns:
            API response body as a dictionary.

        Notes:
            - Request URL: /developer/users/:id/license_plates/:license_plate_id
            - Permission Key: edit:user
            - Method: DELETE
        """
        path = f"/developer/users/{user_id}/license_plates/{license_plate_id}"
        return self.client._make_request("DELETE", path)

    def upload_user_profile_picture(self, user_id: str, image_data: bytes) -> Dict[str, Any]:
        """Upload a user profile picture.

        Args:
            user_id: Target user's ID.
            image_data: Raw image bytes.

        Returns:
            API response body as a dictionary.

        Notes:
            - Request URL: /developer/users/:id/avatar
            - Permission Key: edit:user
            - Method: POST
        """
        path = f"/developer/users/{user_id}/avatar"
        return self.client._make_request("POST", path, data=image_data)

