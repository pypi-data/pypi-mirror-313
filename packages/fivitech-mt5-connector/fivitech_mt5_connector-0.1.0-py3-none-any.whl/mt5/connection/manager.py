from typing import Optional, Dict, List
import MT5Manager
from ..constants import MT5ServerConfig
from ..exceptions import MT5ConnectionError
from ..sinks import MT5UserSink, MT5DealSink

class MT5ConnectionManager:
  def __init__(self, server_config: MT5ServerConfig, data_folder: Optional[str] = None):
    """
    Initialize MT5 Connection Manager
    
    Args:
      server_config: Server configuration containing connection details
      data_folder: Optional custom data folder path for MT5Manager
    """
    self.server_config = server_config
    self._manager = MT5Manager.ManagerAPI(data_folder) if data_folder else MT5Manager.ManagerAPI()
    self._admin = MT5Manager.AdminAPI(data_folder) if data_folder else MT5Manager.AdminAPI()
    self._connected = False
    self._user_sink: Optional[MT5UserSink] = None
    self._deal_sink: Optional[MT5DealSink] = None
        
  def connect(self) -> bool:
    """
    Attempts to connect to MT5 server using the configured IPs with failover.
    Connects both ManagerAPI and AdminAPI instances.
    """
    if self._connected:
      return True
        
    for ip in self.server_config.ips:
      try:  
        # Connect ManagerAPI
        manager_result = self._manager.Connect(
          ip,
          self.server_config.username,
          self.server_config.manager_password,
          MT5Manager.ManagerAPI.EnPumpModes.PUMP_MODE_FULL,
          60000  # 1 minute timeout
        )
        
        if not manager_result:
          continue
            
        # Connect AdminAPI with the same credentials
        admin_result = self._admin.Connect(
          ip,
          self.server_config.username,
          self.server_config.manager_password,
          MT5Manager.AdminAPI.EnPumpModes.PUMP_MODE_FULL,
          60000  # 1 minute timeout
        )
        
        if not admin_result:
          # Disconnect manager if admin connection fails
          self._manager.Disconnect()
          continue
            
        self._connected = True
        return True
              
      except Exception as e:
        last_error = MT5Manager.LastError()
        # Ensure both are disconnected if either fails
        try:
          self._manager.Disconnect()
        except:
          pass
        try:
          self._admin.Disconnect()
        except:
          pass
        continue
            
    raise MT5ConnectionError(
      f"Failed to connect to all IPs for server {self.server_config.name}. "
      f"Last error: {MT5Manager.LastError()}"
    )
      
  def disconnect(self):
    """
    Safely disconnect from MT5 server (both ManagerAPI and AdminAPI)
    """
    if self._connected:
      if self._user_sink:
        self._manager.UserUnsubscribe(self._user_sink)
      if self._deal_sink:
        self._manager.DealUnsubscribe(self._deal_sink)
      try:
        self._manager.Disconnect()
      except:
        pass
      try:
        self._admin.Disconnect()
      except:
        pass
      self._connected = False
          
  @property
  def manager(self) -> MT5Manager.ManagerAPI:
    """
    Returns active ManagerAPI instance
    
    Raises:
        MT5ConnectionError: If not connected to MT5 server
    """
    if not self._connected:
      raise MT5ConnectionError("Not connected to MT5 server")
    return self._manager
  
  @property
  def admin(self) -> MT5Manager.AdminAPI:
    """
    Returns active AdminAPI instance
    
    Raises:
        MT5ConnectionError: If not connected to MT5 server
    """
    if not self._connected:
      raise MT5ConnectionError("Not connected to MT5 server")
    return self._admin
      
  def __enter__(self):
    """Context manager entry"""
    self.connect()
    return self
      
  def __exit__(self, exc_type, exc_val, exc_tb):
    """Context manager exit"""
    self.disconnect()
    
  def setup_user_sink(self, sink: MT5UserSink) -> bool:
    """Setup user event sink"""
    if not self._connected:
      raise MT5ConnectionError("Must be connected to setup sinks")
    
    if self._user_sink:
      self._manager.UserUnsubscribe(self._user_sink)
    
    self._user_sink = sink
    return self._manager.UserSubscribe(sink)
    
  def setup_deal_sink(self, sink: MT5DealSink) -> bool:
    """Setup deal event sink"""
    if not self._connected:
      raise MT5ConnectionError("Must be connected to setup sinks")
    
    if self._deal_sink:
      self._manager.DealUnsubscribe(self._deal_sink)
    
    self._deal_sink = sink
    return self._manager.DealSubscribe(sink)

class MT5ConnectionPool:
  def __init__(self, server_configs: List[MT5ServerConfig], data_folder: Optional[str] = None):
    """
    Initialize MT5 Connection Pool
    
    Args:
      server_configs: List of server configurations
      data_folder: Optional custom data folder path for MT5Manager
    """
    self.connections: Dict[str, MT5ConnectionManager] = {}
    self.data_folder = data_folder
    
    for config in server_configs:
      self.connections[config.name] = MT5ConnectionManager(config, data_folder)
  
  def connect_all(self) -> Dict[str, bool]:
    """
    Attempts to connect to all configured MT5 servers
    Returns dict of server names and their connection status
    """
    results = {}
    for name, connection in self.connections.items():
      try:
        connection.connect()
        results[name] = True
      except MT5ConnectionError as e:
        results[name] = False
    return results
  
  def disconnect_all(self):
    """
    Disconnects from all MT5 servers
    """
    for connection in self.connections.values():
      connection.disconnect()
  
  def get_connection(self, server_name: str) -> MT5ConnectionManager:
    """
    Get connection manager for specific server
    
    Args:
      server_name: Name of the server to get connection for
        
    Raises:
      KeyError: If server name doesn't exist
    """
    if server_name not in self.connections:
      raise KeyError(f"No connection found for server: {server_name}")
    return self.connections[server_name]
  
  def __enter__(self):
    """Context manager entry"""
    self.connect_all()
    return self
  
  def __exit__(self, exc_type, exc_val, exc_tb):
    """Context manager exit"""
    self.disconnect_all()
