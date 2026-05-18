from typing import Any, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import UniFiAccessClient


class AccessPolicyManager:
    """High-level manager for UniFi Access access policy operations.

    This manager wraps endpoints for access policies, holiday groups, and
    schedules. All HTTP I/O is delegated to the provided `client` which must
    expose a private method `_make_request(method, path, ...)`.

    Notes for LLMs/MCP:
    - Return values mirror UniFi Access API responses where possible.
    - IDs are strings provided by the UniFi backend.
    - Pagination parameters are optional unless explicitly required.
    """

    def __init__(self, client: Any) -> None:
        """Initialize the manager.

        Args:
            client: Low-level HTTP client with a `_make_request` method.
        """
        self.client = client

    # --- Access Policy Methods ---

    def create_access_policy(
        self,
        name: str,
        resource: List[Dict[str, str]],
        schedule_id: List[str],
    ) -> Dict[str, Any]:
        """Create a new access policy.

        Args:
            name: Name of the access policy.
            resource: List of doors or door groups.
                Each object should be: {"id": "uuid", "type": "door" | "door_group"}
            schedule_id: ID of the associated schedule.

        Returns:
            Access policy data as a dictionary.

        Notes:
            - Request URL: /developer/access-policies
            - Permission Key: edit:access_policy
            - Method: POST
        """
        path = "/developer/access_policies"
        data = {
            "name": name,
            "resource": resource
        }
        if schedule_id:
            data["schedule_id"] = schedule_id
        return self.client._make_request("POST", path, json=data)

    def update_access_policy(
        self,
        policy_id: str,
        name: Optional[str] = None,
        resource: Optional[List[Dict[str, str]]] = None,
        schedule_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update an existing access policy.

        Args:
            policy_id: Target access policy ID.
            name: New name for the policy.
            resource: New list of doors or door groups.
                Each object should be: {"id": "uuid", "type": "door" | "door_group"}
            schedule_id: New schedule ID.

        Returns:
            Updated access policy data as a dictionary.

        Notes:
            - Request URL: /developer/access-policies/:id
            - Permission Key: edit:access_policy
            - Method: PUT
        """
        path = f"/developer/access_policies/{policy_id}"
        data = {}
        if name:
            data["name"] = name
        if resource is not None:
            data["resource"] = resource
        if schedule_id is not None:
            data["schedule_id"] = schedule_id
        return self.client._make_request("PUT", path, json=data)

    def delete_access_policy(self, policy_id: str) -> Dict[str, Any]:
        """Delete an access policy.

        Args:
            policy_id: The access policy's ID.

        Returns:
            API response body (may be empty depending on API behavior).

        Notes:
            - Request URL: /developer/access-policies/:id
            - Permission Key: edit:access_policy
            - Method: DELETE
        """
        path = f"/developer/access_policies/{policy_id}"
        return self.client._make_request("DELETE", path)

    def fetch_access_policy(self, policy_id: str) -> Dict[str, Any]:
        """Fetch an access policy's details.

        Args:
            policy_id: The access policy's ID.

        Returns:
            Access policy data as a dictionary.

        Notes:
            - Request URL: /developer/access-policies/:id
            - Permission Key: view:access_policy
            - Method: GET
        """
        path = f"/developer/access_policies/{policy_id}"
        return self.client._make_request("GET", path)

    def fetch_all_access_policies(self) -> List[Dict[str, Any]]:
        """Fetch all access policies.

        Returns:
            A list of access policy data dictionaries.

        Notes:
            - Request URL: /developer/access-policies
            - Permission Key: view:access_policy
            - Method: GET
        """
        path = "/developer/access_policies"
        return self.client._make_request("GET", path)

    # --- Holiday Group Methods ---

    def create_holiday_group(
        self,
        name: str,
        description: Optional[str],
        holidays: Optional[List[Dict[str, Any]]],
    ) -> Dict[str, Any]:
        """Create a new holiday group.

        Args:
            name: Name of the holiday group.
            description: Optional description of the holiday group.
            holidays: Optional list of holiday dicts.
                Each holiday should be: {"description": "description", "name": "Holiday name",
                                        "repeat": True, "is_template": False, "start_time": "2023-08-25T00:00:00Z",
                                        "end_time": "2023-08-25T00:00:00Z"}
            holidays: Optional list of holiday dicts.

        Returns:
            Holiday group data as a dictionary.

        Notes:
            - Request URL: /developer/holiday-groups
            - Permission Key: edit:policy
            - Method: POST
        """
        path = "/developer/access_policies/holiday_groups"
        data = {"name": name}
        if holidays:
            data["holidays"] = holidays
        return self.client._make_request("POST", path, json=data)

    def update_holiday_group(
        self,
        group_id: str,
        name: Optional[str],
        description: Optional[str],
        holidays: Optional[List[Dict[str, Any]]],
    ) -> Dict[str, Any]:
        """Update an existing holiday group.

        Args:
            group_id: Holiday group ID.
            name: New name for the group.
            description: New description for the group.
            holidays: New list of holiday dicts.

        Returns:
            API response body as a dictionary.

        Notes:
            - Request URL: /developer/holiday-groups/:id
            - Permission Key: edit:holiday_group
            - Method: PUT
        """
        path = f"/developer/access_policies/holiday_groups/{group_id}"
        data = {}
        if name:
            data["name"] = name
        if description:
            data["description"] = description
        if holidays is not None:
            data["holidays"] = holidays
        return self.client._make_request("PUT", path, json=data)

    def delete_holiday_group(self, group_id: str) -> Dict[str, Any]:
        """Delete a holiday group.

        Args:
            group_id: The holiday group's ID.

        Returns:
            API response body (may be empty depending on API behavior).

        Notes:
            - Request URL: /developer/holiday-groups/:id
            - Permission Key: edit:holiday_group
            - Method: DELETE
        """
        path = f"/developer/access_policies/holiday_groups/{group_id}"
        return self.client._make_request("DELETE", path)

    def fetch_holiday_group(self, group_id: str) -> Dict[str, Any]:
        """Fetch a holiday group's details.

        Args:
            group_id: The holiday group's ID.

        Returns:
            Holiday group data as a dictionary.

        Notes:
            - Request URL: /developer/holiday-groups/:id
            - Permission Key: view:holiday_group
            - Method: GET
        """
        path = f"/developer/access_policies/holiday_groups/{group_id}"
        return self.client._make_request("GET", path)

    def fetch_all_holiday_groups(self) -> List[Dict[str, Any]]:
        """Fetch all holiday groups.

        Returns:
            A list of holiday group data dictionaries.

        Notes:
            - Request URL: /developer/holiday-groups
            - Permission Key: view:holiday_group
            - Method: GET
        """
        path = "/developer/access_policies/holiday_groups"
        return self.client._make_request("GET", path)

    # --- Schedule Methods ---
    def create_schedule(
        self,
        name: str,
        week_schedule: Optional[Dict[str, Any]] = None,
        holiday_group_id: Optional[str] = None,
        holiday_schedule: Optional[List[dict]] = None,
    ) -> Dict[str, Any]:
        """Create a schedule for access policies.

        Args:
            name: Schedule name.
            week_schedule: Weekly schedule structure.
            holiday_group_id: Holiday group ID to associate.
            holiday_schedule: Optional schedule for holiday-specific overrides.

        Returns:
            Schedule data as a dictionary.
        """
        path = "/developer/access_policies/schedules"
        data = {"name": name}

        #TODO Bug in unifi api.  temporary fix below.  Set a holiday schedule because an empty one throws errors on the front end
        data['holiday_schedule'] = [
            {'start_time': '12:00:00',
             'end_time': '13:00:00',}
        ]

        data['week_schedule'] = {
                'monday':[],
                'tuesday':[],
                'wednesday':[],
                'thursday':[],
                'friday':[],
                'saturday':[],
                'sunday':[],
            }

        if week_schedule:
            data['week_schedule'] = week_schedule
        if holiday_group_id:
            data['holiday_group_id'] = holiday_group_id
        if holiday_schedule:
            data['holiday_schedule'] = holiday_schedule
        return self.client._make_request("POST", path, json=data)

    def update_schedule(
        self,
        schedule_id: str,
        name: Optional[str] = None,
        week_schedule: Optional[Dict[str, Any]] = None,
        holiday_group_id: Optional[str] = None,
        holiday_schedule: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Update an existing schedule.

        Args:
            schedule_id: The schedule's ID.
            name: New name for the schedule.
            week_schedule: New weekly schedule structure.
            holiday_group_id: New holiday group ID.
            holiday_schedule: New holiday-specific schedule.

        Returns:
            API response body as a dictionary.

        Notes:
            - Request URL: /developer/schedules/:id
            - Permission Key: edit:schedule
            - Method: PUT
        """
        path = f"/developer/access_policies/schedules/{schedule_id}"
        data = {}
        if name:
            data["name"] = name
        if week_schedule:
            data['week_schedule'] = week_schedule
        if holiday_group_id:
            data['holiday_group_id'] = holiday_group_id
        if holiday_schedule:
            data['holiday_schedule'] = holiday_schedule
        return self.client._make_request("PUT", path, json=data)

    def delete_schedule(self, schedule_id: str) -> Dict[str, Any]:
        """Delete a schedule.

        Args:
            schedule_id: The schedule's ID.

        Returns:
            API response body (may be empty depending on API behavior).

        Notes:
            - Request URL: /developer/schedules/:id
            - Permission Key: edit:schedule
            - Method: DELETE
        """
        path = f"/developer/access_policies/schedules/{schedule_id}"
        return self.client._make_request("DELETE", path)

    def fetch_schedule(self, schedule_id: str) -> Dict[str, Any]:
        """Fetch a schedule's details.

        Args:
            schedule_id: The schedule's ID.

        Returns:
            Schedule data as a dictionary.

        Notes:
            - Request URL: /developer/schedules/:id
            - Permission Key: view:schedule
            - Method: GET
        """
        path = f"/developer/access_policies/schedules/{schedule_id}"
        return self.client._make_request("GET", path)

    def fetch_all_schedules(self) -> List[Dict[str, Any]]:
        """Fetch all schedules.

        Returns:
            A list of schedule data dictionaries.

        Notes:
            - Request URL: /developer/schedules
            - Permission Key: view:schedule
            - Method: GET
        """
        path = "/developer/access_policies/schedules"
        return self.client._make_request("GET", path)
