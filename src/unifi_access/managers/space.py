from typing import Any, Dict, List, Optional, TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from ..client import UniFiAccessClient


class SpaceManager:
    """High-level manager for space-related operations (doors, door groups).

    Wraps endpoints for door groups and doors including control operations like
    unlock, temporary lock rules, and emergency status. All HTTP I/O is
    delegated to `client` which must expose `_make_request(method, path, ...)`.
    """

    def __init__(self, client: Any) -> None:
        """Initialize the manager.

        Args:
            client: Low-level HTTP client with a `_make_request` method.
        """
        self.client = client

    def fetch_door_group_topology(self) -> Dict[str, Any]:
        """Fetch the topology of door groups.

        Returns:
            Door group topology details as a dictionary.

        Notes:
            - Request URL: /developer/door_groups/topology
            - Permission Key: view:space
            - Method: GET
        """
        path = "/developer/door_groups/topology"
        return self.client._make_request("GET", path)

    def create_door_group(
            self,
            name: str,
            door_ids: List[str]
    ) -> Dict[str, Any]:
        """Create a new door group.

        Args:
            name: Name of the door group.
            door_ids: List of door IDs to include in the group.

        Returns:
            Door group data as a dictionary.

        Notes:
            - Request URL: /developer/door_groups
            - Permission Key: edit:space
            - Method: POST
        """
        path = "/developer/door_groups"
        data = {
            "group_name": name,
            "resources": door_ids  # list of door ids
        }
        return self.client._make_request("POST", path, json=data)

    def fetch_door_group(self, group_id: str) -> Dict[str, Any]:
        """Fetch a door group's details.

        Args:
            group_id: The door group's ID.

        Returns:
            Door group data as a dictionary.

        Notes:
            - Request URL: /developer/door_groups/:id
            - Permission Key: view:space
            - Method: GET
        """
        path = f"/developer/door_groups/{group_id}"
        return self.client._make_request("GET", path)

    def update_door_group(
        self,
        group_id: str,
        name: Optional[str] = None,
        door_ids: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Update an existing door group.

        Args:
            group_id: The door group's ID.
            name: New name for the group (optional).
            door_ids: New list of door IDs (optional).

        Returns:
            Updated door group data as a dictionary.

        Notes:
            - Request URL: /developer/door_groups/:id
            - Permission Key: edit:space
            - Method: PUT
        """
        path = f"/developer/door_groups/{group_id}"
        data = {}
        if name:
            data["group_name"] = name
        if door_ids is not None:
            data["resources"] = door_ids
        return self.client._make_request("PUT", path, json=data)

    def fetch_all_door_groups(self) -> List[Dict[str, Any]]:
        """Fetch all door groups.

        Returns:
            A list of door group data dictionaries.

        Notes:
            - Request URL: /developer/door_groups
            - Permission Key: view:space
            - Method: GET
        """
        path = "/developer/door_groups"
        return self.client._make_request("GET", path)

    def delete_door_group(self, group_id: str) -> Dict[str, Any]:
        """Delete a door group.

        Args:
            group_id: The door group's ID.

        Returns:
            API response body (may be empty depending on API behavior).

        Notes:
            - Request URL: /developer/door_groups/:id
            - Permission Key: edit:space
            - Method: DELETE
        """
        path = f"/developer/door_groups/{group_id}"
        return self.client._make_request("DELETE", path)

    def fetch_door(self, door_id: str) -> Dict[str, Any]:
        """Fetch a door's details.

        Args:
            door_id: The door's ID.

        Returns:
            Door data as a dictionary.

        Notes:
            - Request URL: /developer/doors/:id
            - Permission Key: view:space
            - Method: GET
        """
        path = f"/developer/doors/{door_id}"
        return self.client._make_request("GET", path)

    def fetch_all_doors(self) -> List[Dict[str, Any]]:
        """Fetch all doors.

        Returns:
            A list of door data dictionaries.

        Notes:
            - Request URL: /developer/doors
            - Permission Key: view:space
            - Method: GET
        """
        path = "/developer/doors"
        return self.client._make_request("GET", path)

    def unlock_door(
        self,
        door_id: str,
        reader_id: Optional[str] = None,
        entry_method: Optional[Literal["in", "out"]] = None,
        control_cmd: Optional[Literal["open", "close", "stop"]] = None,
        actor_id: Optional[str] = None,
        actor_name: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Remotely unlock a door.

        Args:
            door_id: The door's ID.
            reader_id: Displays the greeting message only on the device with the specified ID.
            entry_method: In double-driveway mode, "in" and "out" define the gate opening direction.
            control_cmd: In three-button mode (UA Hub gate), supported commands are "open", "close", and "stop".
            actor_id: Custom actor ID to be shown in logs and webhooks.
            actor_name: Custom actor name to be shown in logs and webhooks.
            extra: Custom passthrough data included as-is in webhook payloads.

        Returns:
            API response body as a dictionary.

        Notes:
            - Request URL: /developer/doors/:id/unlock
            - Permission Key: edit:space
            - Method: PUT
            - UniFi Access Requirement: Version 2.2.6 or later for UA-Ultra
        """
        if entry_method and entry_method not in ["in", "out"]:
            raise ValueError("entry_method must be 'in' or 'out'")

        if control_cmd and control_cmd not in ["open", "close", "stop"]:
            raise ValueError("control_cmd must be 'open', 'close', or 'stop'")

        if actor_id and not actor_name or actor_name and not actor_id:
            raise ValueError("actor_id and actor_name must be provided together")

        params = {}
        if reader_id:
            params["reader_id"] = reader_id
        if entry_method:
            params["entry_method"] = entry_method
        if control_cmd:
            params["control_cmd"] = control_cmd

        payload = {
            "actor_id": actor_id,
            "actor_name": actor_name,
            "extra": extra
        }
        path = f"/developer/doors/{door_id}/unlock"
        return self.client._make_request("PUT", path, json=payload, params=params)

    def set_temporary_door_locking_rule(
        self,
        door_id: str,
        type: Literal["keep_lock", "keep_unlock", "custom", "reset", "lock_early", "lock_now"],
        interval: Optional[int] = None
    ) -> Dict[str, Any]:
        """Set a temporary door locking (and unlocking) rule.

        Args:
            door_id: The door's ID.
            type: Rule type. Options: "keep_lock", "keep_unlock", "custom", "reset", "lock_early", "lock_now".
            interval: The duration of the custom unlock time in minutes.

        Returns:
            API response body as a dictionary.

        Notes:
            - Request URL: /developer/doors/:id/lock_rule
            - Permission Key: edit:space
            - Method: PUT
            - UniFi Access Requirement: Version 3.1.30 or later for EAH8, UA-Hub-Door-Mini, UA-Ultra
        """
        path = f"/developer/doors/{door_id}/lock_rule"
        data = {
            "type": type,
        }
        if interval is not None:
            data["interval"] = interval
        return self.client._make_request("PUT", path, json=data)

    def fetch_door_lock_rule(self, door_id: str) -> Dict[str, Any]:
        """Fetch the current door locking rule.

        Args:
            door_id: The door's ID.

        Returns:
            Door locking rule details as a dictionary.

        Notes:
            - Request URL: /developer/doors/:id/lock_rule
            - Permission Key: view:space
            - Method: GET
        """
        path = f"/developer/doors/{door_id}/lock_rule"
        return self.client._make_request("GET", path)

    def set_door_emergency_status(self, lockdown: bool, evacuation: bool) -> Dict[str, Any]:
        """Set the emergency status for doors.

        Args:
            lockdown: If true, keep all doors locked.
            evacuation: If true, keep all doors unlocked.

        Returns:
            API response body as a dictionary.

        Notes:
            - Request URL: /developer/doors/settings/emergency
            - Permission Key: edit:space
            - Method: POST
        """
        path = f"/developer/doors/settings/emergency"
        data = {
            "lockdown": lockdown,
            "evacuation": evacuation
        }
        return self.client._make_request("POST", path, json=data)

    def fetch_door_emergency_status(self) -> Dict[str, Any]:
        """Fetch the current emergency status of doors.

        Returns:
            Door emergency status details as a dictionary.

        Notes:
            - Request URL: /developer/doors/settings/emergency
            - Permission Key: view:space
            - Method: GET
        """
        path = f"/developer/doors/settings/emergency"
        return self.client._make_request("GET", path)
