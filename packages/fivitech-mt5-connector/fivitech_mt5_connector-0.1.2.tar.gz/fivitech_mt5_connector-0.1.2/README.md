# MT5 Connector

A Python package for connecting to and managing MetaTrader5 servers.

## Installation

```bash
pip install fivitech-mt5-connector
```

## Documentation

For detailed documentation, see [DOCUMENTATION.md](DOCUMENTATION.md)

## Changelog

For changelog, see [CHANGELOG.md](CHANGELOG.md)

## Usage

```python
from fivitech_mt5_connector import MT5Pool

# Configure your MT5 servers
servers = [
    {
        "id": 1,
        "type": "demo",
        "name": "Demo Server",
        "username": "manager",
        "manager_password": "your_manager_password",
        "api_password": "your_api_password",
        "ips": ["127.0.0.1", "localhost"]
    }
]

# Initialize the pool
pool = MT5Pool(servers)

# Connect to all servers
connection_status = pool.connect_all()

# Or connect to specific server
pool.connect_server(1)

# Add a new server dynamically
pool.add_server({
    "id": 2,
    "type": "live",
    "name": "Live Server",
    "username": "manager",
    "manager_password": "your_manager_password",
    "api_password": "your_api_password",
    "ips": ["server1.domain.com", "server2.domain.com"]
})

# Connect to the new server
pool.connect_server(2)

# Update server configuration
pool.update_server(2, {
    "name": "Updated Live Server",
    "ips": ["new.server.com"]
})

# Disconnect specific server
pool.disconnect_server(2)

# Remove server from pool
pool.remove_server(2)

# Add custom callbacks if needed
def my_deal_callback(deal, server_info):
    print(f"New deal on {server_info.name}: {deal.Deal}")

pool.add_deal_callback('deal_add', my_deal_callback)

# Get a specific server connection
demo_server = pool.get_server(1)
live_server = pool.get_server(101)

# Disconnect all servers when done
pool.disconnect_all()
```

## Features

- Dynamic server management (add/remove/update servers)
- Individual server connection control
- Multiple server connections management
- Account operations
- Transaction handling
- User management
- Deal monitoring
- Default and custom callbacks for deals and user events

## Server Configuration

Each server in the configuration requires:
- `id`: Unique integer identifier
- `type`: Either 'demo' or 'live'
- `name`: Server name
- `username`: Manager username/login
- `manager_password`: Manager password for server operations
- `api_password`: API password for MT5 WebAPI access
- `ips`: List of IP addresses for failover

## Server Management Methods

### Adding Servers
```python
pool.add_server({
    "id": 1,
    "type": "demo",
    "name": "Demo Server",
    "username": "manager",
    "manager_password": "password",
    "api_password": "api_password",
    "ips": ["127.0.0.1"]
})
```

### Updating Servers
```python
pool.update_server(1, {
    "name": "Updated Name",
    "ips": ["new.ip.address"]
})
```

### Removing Servers
```python
pool.remove_server(1)
```

### Connection Control
```python
# Connect specific server
pool.connect_server(1)

# Disconnect specific server
pool.disconnect_server(1)

# Connect all servers
pool.connect_all()

# Disconnect all servers
pool.disconnect_all()
```

## Requirements

- Python 3.7+
- MT5Manager>=5.0.3906
- pandas>=1.0.0
- numpy>=1.19.0
- pytz>=2021.1
- requests>=2.26.0
- python-dateutil>=2.8.2

## License

Proprietary - All rights reserved 