from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .pool import MT5Pool

@api_view(['GET'])
@permission_classes([AllowAny])
def check_mt5_connections(request, mt5_pool: MT5Pool):
    """
    Get connection status for all MT5 servers
    
    Args:
        request: HTTP request
        mt5_pool: Initialized MT5Pool instance
    
    Returns:
        {
            "demo_servers": [
                {
                    "id": 1,
                    "name": "Demo Server 1",
                    "connected": true,
                    "ips": ["127.0.0.1"]
                },
                ...
            ],
            "live_servers": [
                {
                    "id": 101,
                    "name": "Live Server 1",
                    "connected": true,
                    "ips": ["104.46.38.179"]
                },
                ...
            ]
        }
    """
    demo_servers = []
    live_servers = []
    
    # Get all servers from the pool
    for server in mt5_pool.servers:
        try:
            connection = mt5_pool.get_server(server.id)
            server_info = {
                'id': server.id,
                'name': server.name,
                'connected': connection._connected,
                'ips': server.ips
            }
            
            if server.type == 'demo':
                demo_servers.append(server_info)
            else:
                live_servers.append(server_info)
                
        except Exception as e:
            server_info = {
                'id': server.id,
                'name': server.name,
                'connected': False,
                'ips': server.ips,
                'error': str(e)
            }
            
            if server.type == 'demo':
                demo_servers.append(server_info)
            else:
                live_servers.append(server_info)
    
    status = {
        'demo_servers': demo_servers,
        'live_servers': live_servers
    }
    
    return Response(status)
