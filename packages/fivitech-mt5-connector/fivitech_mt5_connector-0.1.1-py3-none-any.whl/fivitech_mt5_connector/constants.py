from typing import List
from dataclasses import dataclass

@dataclass
class MT5ServerConfig:
    """Configuration for an MT5 server
    
    Args:
        id: Unique server ID
        name: Server name
        type: Server type ('demo' or 'live')
        ips: List of IP addresses for failover
        username: Manager username/login
        manager_password: Manager password for server operations
        api_password: API password for MT5 WebAPI access
    """
    id: int
    name: str
    type: str  # 'demo' or 'live'
    ips: List[str]  # List of IP addresses for failover
    username: str
    manager_password: str
    api_password: str

    def __post_init__(self):
        """Validate configuration after initialization"""
        if self.type not in ['demo', 'live']:
            raise ValueError(f"Invalid server type: {self.type}. Must be 'demo' or 'live'")
        
        if not self.ips:
            raise ValueError("At least one IP address must be provided")
        
        if not isinstance(self.id, int):
            raise ValueError("Server ID must be an integer")