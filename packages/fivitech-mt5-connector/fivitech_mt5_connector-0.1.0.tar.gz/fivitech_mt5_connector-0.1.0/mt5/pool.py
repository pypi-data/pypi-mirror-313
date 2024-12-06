from typing import Dict, List, Optional, Callable, Any
from .connection.manager import MT5ConnectionManager
from .constants import MT5ServerConfig
from .exceptions import MT5ConnectionError
from .sinks import MT5UserSink, MT5DealSink, ServerInfo

class MT5ConnectionPools:
    _instance = None
    
    def __new__(cls, servers=None):
        if cls._instance is None:
            cls._instance = super(MT5ConnectionPools, cls).__new__(cls)
            cls._instance._initialized = False
        if servers is not None:
            # Convert dictionaries to MT5ServerConfig objects
            cls._instance._servers = [
                s if isinstance(s, MT5ServerConfig) else MT5ServerConfig(**s)
                for s in servers
            ]
        return cls._instance
    
    def __init__(self, servers=None):
        if self._initialized:
            return
            
        # Store server configurations
        self._servers = []
        if servers is not None:
            # Convert dictionaries to MT5ServerConfig objects
            self._servers = [
                s if isinstance(s, MT5ServerConfig) else MT5ServerConfig(**s)
                for s in servers
            ]
            
        # Initialize pools for demo and live servers
        self._demo_pools: Dict[int, MT5ConnectionManager] = {}
        self._live_pools: Dict[int, MT5ConnectionManager] = {}
        
        # Initialize sink dictionaries - one set of sinks per server
        self._user_sinks: Dict[int, MT5UserSink] = {}
        self._deal_sinks: Dict[int, MT5DealSink] = {}
        
        self._initialized = True
        print("DEBUG: MT5ConnectionPools initialized with multi-server support")
    
    @property
    def servers(self):
        """Get list of server configurations"""
        return self._servers
    
    def _get_or_create_sinks(self, server_config: MT5ServerConfig) -> tuple[MT5UserSink, MT5DealSink]:
        """Get or create sinks for a server"""
        if server_config.id not in self._user_sinks:
            server_info = ServerInfo(
                id=server_config.id,
                name=server_config.name,
                type=server_config.type
            )
            self._user_sinks[server_config.id] = MT5UserSink(server_info)
            self._deal_sinks[server_config.id] = MT5DealSink(server_info)
            
        return self._user_sinks[server_config.id], self._deal_sinks[server_config.id]
    
    def setup_sinks(self):
        """Setup sinks for all active connections"""
        print("Setting up MT5 sinks for all servers...")
        try:
            # Setup sinks for all demo servers
            for server_id, manager in self._demo_pools.items():
                if manager._connected:
                    config = next(s for s in self._servers if s.id == server_id)
                    user_sink, deal_sink = self._get_or_create_sinks(config)
                    manager.setup_user_sink(user_sink)
                    manager.setup_deal_sink(deal_sink)
            
            # Setup sinks for all live servers
            for server_id, manager in self._live_pools.items():
                if manager._connected:
                    config = next(s for s in self._servers if s.id == server_id)
                    user_sink, deal_sink = self._get_or_create_sinks(config)
                    manager.setup_user_sink(user_sink)
                    manager.setup_deal_sink(deal_sink)
                    
        except Exception as e:
            print(f"Warning: Error setting up sinks: {str(e)}")
    
    def add_user_callback(self, event: str, callback: Callable):
        """
        Add callback for user events
        
        The callback should accept two parameters:
        - data: The event data from MT5
        - server_info: ServerInfo object containing server id, name, and type
        """
        # Add callback to all user sinks
        for sink in self._user_sinks.values():
            sink.add_callback(event, callback)
    
    def add_deal_callback(self, event: str, callback: Callable):
        """
        Add callback for deal events
        
        The callback should accept two parameters:
        - data: The event data from MT5
        - server_info: ServerInfo object containing server id, name, and type
        """
        print(f"Adding deal callback for {event}")
        # Add callback to all deal sinks
        for sink in self._deal_sinks.values():
            sink.add_callback(event, callback)
    
    def get_demo(self, server_id: int) -> MT5ConnectionManager:
        """
        Get connection manager for specific demo server
        
        Args:
            server_id: ID of the demo server
            
        Returns:
            MT5ConnectionManager for the specified server
            
        Raises:
            MT5ConnectionError if server not found
        """
        if server_id not in self._demo_pools:
            config = next((s for s in self._servers if s.type == 'demo' and s.id == server_id), None)
            if not config:
                raise MT5ConnectionError(f"No demo server found with ID: {server_id}")
            self._demo_pools[server_id] = MT5ConnectionManager(config)
        return self._demo_pools[server_id]
    
    def get_live(self, server_id: int) -> MT5ConnectionManager:
        """
        Get connection manager for specific live server
        
        Args:
            server_id: ID of the live server
            
        Returns:
            MT5ConnectionManager for the specified server
            
        Raises:
            MT5ConnectionError if server not found
        """
        if server_id not in self._live_pools:
            config = next((s for s in self._servers if s.type == 'live' and s.id == server_id), None)
            if not config:
                raise MT5ConnectionError(f"No live server found with ID: {server_id}")
            self._live_pools[server_id] = MT5ConnectionManager(config)
        return self._live_pools[server_id]
    
    def get_all_demo_servers(self) -> List[MT5ConnectionManager]:
        """Get all demo server connections"""
        # Initialize connections for any configured demo servers that haven't been accessed yet
        for server in self._servers:
            if server.type == 'demo' and server.id not in self._demo_pools:
                self.get_demo(server.id)
        return list(self._demo_pools.values())
    
    def get_all_live_servers(self) -> List[MT5ConnectionManager]:
        """Get all live server connections"""
        # Initialize connections for any configured live servers that haven't been accessed yet
        for server in self._servers:
            if server.type == 'live' and server.id not in self._live_pools:
                self.get_live(server.id)
        return list(self._live_pools.values())
    
    def get_by_type(self, server_type: str, server_id: Optional[int] = None) -> MT5ConnectionManager:
        """
        Get connection by server type and optional ID
        
        Args:
            server_type: Type of server ('demo' or 'live')
            server_id: Optional specific server ID. If not provided, returns first available server
            
        Returns:
            MT5ConnectionManager for the specified server
            
        Raises:
            ValueError if invalid server type
            MT5ConnectionError if server not found
        """
        if server_type not in ['demo', 'live']:
            raise ValueError(f"Invalid server type: {server_type}")
            
        if server_id is not None:
            # Get specific server
            if server_type == 'demo':
                return self.get_demo(server_id)
            return self.get_live(server_id)
        
        # Get first available server of type
        config = next((s for s in self._servers if s.type == server_type), None)
        if not config:
            raise MT5ConnectionError(f"No {server_type} server configuration found")
            
        if server_type == 'demo':
            return self.get_demo(config.id)
        return self.get_live(config.id)
    
    def get_by_id(self, server_id: int) -> MT5ConnectionManager:
        """
        Get connection by server ID
        
        Args:
            server_id: Server ID to connect to
            
        Returns:
            MT5ConnectionManager for the specified server
            
        Raises:
            ValueError if server not found
        """
        config = next((s for s in self._servers if s.id == server_id), None)
        if not config:
            raise ValueError(f"No server found with ID: {server_id}")
        
        if config.type == 'demo':
            return self.get_demo(server_id)
        return self.get_live(server_id)
    
    def connect_all(self) -> Dict[str, bool]:
        """
        Connect to all configured servers
        
        Returns:
            Dict mapping server names to connection success status
        """
        results = {}
        
        # Try to connect to all servers in configuration
        for server in self._servers:
            try:
                connection = self.get_by_id(server.id)
                connection.connect()
                results[server.name] = True
            except Exception as e:
                results[server.name] = False
                print(f"Failed to connect to server {server.name}: {str(e)}")
        
        return results
    
    def disconnect_all(self):
        """Disconnect from all servers"""
        # Disconnect all demo servers
        for manager in self._demo_pools.values():
            try:
                manager.disconnect()
            except Exception as e:
                print(f"Error disconnecting from demo server: {str(e)}")
        
        # Disconnect all live servers
        for manager in self._live_pools.values():
            try:
                manager.disconnect()
            except Exception as e:
                print(f"Error disconnecting from live server: {str(e)}")
        
        # Clear the pools
        self._demo_pools.clear()
        self._live_pools.clear()
    
    def get_server(self, server_id: int) -> MT5ConnectionManager:
        """
        Get connection manager for a specific server by ID
        
        Args:
            server_id: Server ID to get connection for
            
        Returns:
            MT5ConnectionManager for the specified server
            
        Raises:
            MT5ConnectionError if server not found
        """
        config = next((s for s in self._servers if s.id == server_id), None)
        if not config:
            raise MT5ConnectionError(f"No server found with ID: {server_id}")
            
        if config.type == 'demo':
            return self.get_demo(server_id)
        return self.get_live(server_id)

# Global instance
mt5_pools = MT5ConnectionPools() 