# UniFi Access Python Client

A modern, thin API wrapper for the UniFi Access API. This library provides a clean and intuitive interface for managing UniFi Access devices, users, visitors, access policies, and more.

## Features

- **Thin API Wrapper**: Returns simple dictionaries for flexibility and performance
- **Comprehensive API Coverage**: Full support for all UniFi Access API endpoints
- **Async Support**: Built-in async client for high-performance applications
- **Easy Configuration**: Environment variable support with `.env` files
- **Webhook Support**: Built-in webhook listener and manager

## Installation

```bash
pip install unifi_access
```


## Quick Start

### Configuration

Create a `.env` file in your project root:

```env
UNIFI_ACCESS_BASE_URL=https://192.168.1.1
UNIFI_ACCESS_API_TOKEN=your-api-token-here
UNIFI_ACCESS_PORT=12445
UNIFI_SESSION_TIMEOUT=30
```
UNIFI_SESSION_TIMEOUT is optional and defaults to 15 seconds.  Increasing timeout time is sometimes required on busy systems with large amounts of users, doors, etc. and the Unifi console/NVR takes a little longer to process requests.

### Basic Setup

```python
from unifi_access.client import UniFiAccessClient

# Initialize with environment variables
client = UniFiAccessClient()

# Or initialize with explicit credentials
client = UniFiAccessClient(
    base_url="https://192.168.1.1",
    api_token="your-api-token",
    port="12445",
    verify_ssl=False
)
```
## Usage Examples

Most methods/functions are named identical to Unifi Access API documentation section headings.  IE:  From the unifi docs "7.5 Fetch All Door Groups" the method will be client.spaces.fetch_all_door_groups()

### User Management

```python
# Fetch all users - returns a list of dictionaries
users = client.users.fetch_all_users()

if users:
    user = users[0]
    print(f"User: {user.get('first_name')} {user.get('last_name')}")

    # Update user
    client.users.update_user(user['id'], first_name="NewName")
    
    # Assign an NFC card
    client.users.assign_nfc_card_to_user(user['id'], "card_token_123")
    
    # Get access policies
    policies = client.users.fetch_access_policies_assigned_to_user(user['id'])
```

### Visitor Management

```python
# Create a visitor - returns a dictionary
visitor = client.visitors.create_visitor(
    first_name="John",
    last_name="Doe",
    start_time=1688546460, # Unix timestamp in timezone of the location
    end_time=1688572799, 
    email="john.doe@example.com",
    resources=[
        {
            "id": "door_id_123",
            "type": "door"
        }
    ],
    week_schedule={
        "sunday": [],
        "monday": [],
        "tuesday": [
            # Single time slot
            {
                "start_time": "06:00:00", # 6 am
                "end_time": "18:00:00" # 6 pm
            }
        ],
        "wednesday": [],
        "thursday": [
            # Multiple time slots in single day.
            {
                "start_time": "06:00:00",
                "end_time": "09:00:00", # 9 am
            },
            {
                "start_time": "18:00:00", # 6 pm
                "end_time": "23:59:59" # Midnight
            }
        ],
        "friday": [],
        "saturday": []        
    }
)

# Manage visitor
client.visitors.assign_nfc_card_to_visitor(visitor['id'], "card_token_456")
client.visitors.assign_pin_code_to_visitor(visitor['id'], "1234")
client.visitors.update_visitor(visitor['id'], remarks="VIP visitor")
client.visitors.delete_visitor(visitor['id'])
```

### Door Management

```python
# Fetch all doors - returns a list of dictionaries
doors = client.spaces.fetch_all_doors()

if doors:
    door = doors[0]
    print(f"Door: {door.get('name')}")

    # Control doors
    client.spaces.unlock_door(door['id'])
    client.spaces.set_temporary_door_locking_rule(door['id'], "keep_unlock", 60)  # Keep unlocked for 1 hour
```

### Access Policy Management

```python
# List all access policies
policies = client.access_policies.fetch_all_access_policies()

if policies:
    policy = policies[0]
    print(f"Policy: {policy.get('name')}")

    # Manage policies
    client.access_policies.update_access_policy(policy['id'], name="New Policy Name")
    client.access_policies.delete_access_policy(policy['id'])
```

### Credential Management

```python
# Import 26-bit Wiegand cards
wiegand_cards = [
    {"facility_code": 100, "card_number": 1234},
    {"facility_code": 100, "card_number": 1235},
]
client.credentials.import_26bit_wiegand_cards(wiegand_cards)
```

### Async Support

```python
from unifi_access.client import AsyncUniFiAccessClient

# Use async client for high-performance applications
async with AsyncUniFiAccessClient() as client:
    users = await client.users.fetch_all_users()
    for user in users:
        print(f"{user.get('first_name')} {user.get('last_name')}")
```

## API Managers

The client provides the following manager interfaces. Click each to see available functions:

<details>
<summary><b>client.users</b> (User and user group management)</summary>

- `create_user`
- `update_user`
- `fetch_user`
- `fetch_all_users`
- `delete_user`
- `search_users`
- `assign_access_policy_to_user`
- `assign_nfc_card_to_user`
- `unassign_nfc_card_from_user`
- `assign_pin_code_to_user`
- `unassign_pin_code_from_user`
- `create_user_group`
- `fetch_all_user_groups`
- `fetch_user_group`
- `update_user_group`
- `delete_user_group`
- `assign_users_to_user_group`
- `unassign_users_from_user_group`
- `fetch_users_in_a_user_group`
- `fetch_all_users_in_a_user_group`
- `fetch_access_policies_assigned_to_user`
- `assign_access_policy_to_user_group`
- `fetch_access_policies_assigned_to_user_group`
- `assign_touch_pass_to_user`
- `unassign_touch_pass_from_user`
- `batch_assign_touch_passes_to_users`
- `assign_license_plate_numbers_to_user`
- `unassign_license_plate_number_from_user`
- `upload_user_profile_picture`
</details>

<details>
<summary><b>client.visitors</b> (Visitor management)</summary>

- `create_visitor`
- `update_visitor`
- `fetch_visitor`
- `fetch_all_visitors`
- `delete_visitor`
- `assign_nfc_card_to_visitor`
- `unassign_nfc_card_from_visitor`
- `assign_pin_code_to_visitor`
- `unassign_pin_code_from_visitor`
- `assign_qr_code_to_visitor`
- `unassign_qr_code_from_visitor`
- `assign_license_plate_numbers_to_visitor`
- `unassign_license_plate_numbers_from_visitor`
</details>

<details>
<summary><b>client.access_policies</b> (Access policy management)</summary>

- `create_access_policy`
- `update_access_policy`
- `delete_access_policy`
- `fetch_access_policy`
- `fetch_all_access_policies`
- `create_holiday_group`
- `update_holiday_group`
- `delete_holiday_group`
- `fetch_holiday_group`
- `fetch_all_holiday_groups`
- `create_schedule`
- `update_schedule`
- `delete_schedule`
- `fetch_schedule`
- `fetch_all_schedules`
</details>

<details>
<summary><b>client.credentials</b> (Credential management)</summary>

- `generate_pin_code`
- `enroll_nfc_card`
- `fetch_nfc_card_enrollment_status`
- `remove_session_created_for_nfc_card_enrollment`
- `fetch_nfc_card`
- `fetch_all_nfc_cards` (alias: `list_nfc_cards`)
- `update_nfc_card`
- `delete_nfc_card`
- `fetch_the_touch_pass_list`
- `search_touch_pass`
- `fetch_all_assignable_touch_passes`
- `update_touch_pass`
- `fetch_touch_pass_details`
- `purchase_touch_passes`
- `download_qr_code_image`
- `import_third_party_nfc_cards`
- `import_third_party_nfc_cards_as_list`
- `import_26bit_wiegand_cards`
</details>

<details>
<summary><b>client.spaces</b> (Door and door group management)</summary>

- `fetch_door_group_topology`
- `create_door_group`
- `fetch_door_group`
- `update_door_group`
- `fetch_all_door_groups`
- `delete_door_group`
- `fetch_door`
- `fetch_all_doors`
- `unlock_door`
- `set_temporary_door_locking_rule`
- `fetch_door_lock_rule`
- `set_door_emergency_status`
- `fetch_door_emergency_status`
</details>

<details>
<summary><b>client.devices</b> (Device management)</summary>

- `fetch_devices`
- `fetch_access_devices_access_method_settings`
- `update_access_devices_access_method_settings`
- `trigger_doorbells`
</details>

<details>
<summary><b>client.system_logs</b> (System log retrieval)</summary>

- `fetch_system_logs`
- `export_system_logs`
- `fetch_resources_in_system_logs`
- `fetch_static_resources_in_system_logs`
</details>

<details>
<summary><b>client.https_certificates</b> (HTTPS certificate management)</summary>

- `upload_https_certificate`
- `delete_https_certificate`
</details>

<details>
<summary><b>client.notifications</b> (Notification management)</summary>

- `fetch_webhook_endpoints_list`
- `add_webhook_endpoint`
- `update_webhook_endpoint`
- `delete_webhook_endpoint`
</details>

<details>
<summary><b>client.identity</b> (Identity management)</summary>

- `send_invitations`
- `fetch_available_resources`
- `assign_resources_to_users`
- `fetch_user_resources`
- `assign_resources_to_user_groups`
- `fetch_user_group_resources`
</details>


## Requirements

- Python 3.8+
- httpx >= 0.23.0


## License

MIT License - see LICENSE file for details

## Author

Travis Tucker

## Links

- [Documentation](https://github.com/tuckert/unifi-access)
- [Bug Tracker](https://github.com/tuckert/unifi-access/issues)
- [Source Code](https://github.com/tuckert/unifi-access)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
