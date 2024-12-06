from .constants import MT5ServerConfig
from .pool import MT5ConnectionPools

# Expose MT5Pool as an alias for MT5ConnectionPools
MT5Pool = MT5ConnectionPools

__version__ = "0.1.0"
__all__ = ['MT5Pool', 'MT5ServerConfig']
