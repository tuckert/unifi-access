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
```

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
    start_time="2026-01-10T09:00:00",
    end_time="2026-01-10T17:00:00",
    email="john.doe@example.com"
)

# Manage visitor
client.visitors.assign_nfc_card(visitor['id'], "card_token_456")
client.visitors.assign_pin_code(visitor['id'], "1234")
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
    client.spaces.set_temporary_door_lock_rule(door['id'], "keep_unlock", 3600)  # Keep unlocked for 1 hour
```

### Access Policy Management

```python
# List all access policies
policies = client.access_policies.list_access_policies()

if policies:
    policy = policies[0]
    print(f"Policy: {policy.get('name')}")

    # Manage policies
    client.access_policies.update_access_policy(policy['id'], name="New Policy Name")
    client.access_policies.delete_access_policy(policy['id'])
```

### Async Support

```python
from client import AsyncUniFiAccessClient

# Use async client for high-performance applications
async with AsyncUniFiAccessClient() as client:
    users = await client.users.fetch_all_users()
    for user in users:
        print(f"{user.get('first_name')} {user.get('last_name')}")
```

## API Managers

The client provides the following manager interfaces:

- **`client.users`**: User and user group management
- **`client.visitors`**: Visitor management
- **`client.access_policies`**: Access policy management
- **`client.credentials`**: Credential management (NFC cards, PIN codes)
- **`client.spaces`**: Door and door group management
- **`client.devices`**: Device management
- **`client.system_logs`**: System log retrieval
- **`client.https_certificates`**: HTTPS certificate management
- **`client.notifications`**: Notification management


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
