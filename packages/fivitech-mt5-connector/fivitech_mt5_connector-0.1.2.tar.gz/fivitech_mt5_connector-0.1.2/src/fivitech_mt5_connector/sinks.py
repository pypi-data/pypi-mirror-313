from typing import Callable, Dict, Any, Optional, NamedTuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class ServerInfo:
    """Server information passed to callbacks"""
    id: int
    name: str
    type: str  # 'demo' or 'live'

class BaseMT5Sink:
    """Base class for MT5 event sinks"""
    def __init__(self, server_info: ServerInfo):
        self._callbacks: Dict[str, list[Callable]] = {}
        self._server_info = server_info
    
    def add_callback(self, event: str, callback: Callable):
        """Add callback for specific event"""
        if event not in self._callbacks:
            self._callbacks[event] = []
        self._callbacks[event].append(callback)
    
    def _trigger_callbacks(self, event: str, data: Any):
        """
        Trigger all callbacks for an event
        
        Args:
            event: Event name
            data: Event data
            
        Each callback will receive (data, server_info) as arguments
        """
        for callback in self._callbacks.get(event, []):
            try:
                callback(data, self._server_info)
            except Exception as e:
                logger.error(f"Error in {event} callback for server {self._server_info.name}: {str(e)}")

class MT5UserSink(BaseMT5Sink):
    """Sink for user-related events"""
    def OnUserDelete(self, user) -> None:
        self._trigger_callbacks('user_delete', user)
        
    def OnUserUpdate(self, user) -> None:
        self._trigger_callbacks('user_update', user)

class MT5DealSink(BaseMT5Sink):
    """Sink for deal-related events"""
    def OnDealAdd(self, deal) -> None:
        self._trigger_callbacks('deal_add', deal) 