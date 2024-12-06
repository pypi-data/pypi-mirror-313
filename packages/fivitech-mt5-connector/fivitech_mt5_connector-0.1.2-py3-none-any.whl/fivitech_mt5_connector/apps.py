from django.apps import AppConfig

class MT5Config(AppConfig):
  name = 'core.mt5'
  verbose_name = 'MT5 Manager'
  
  def ready(self):
    print("DEBUG 1: Starting ready method")
    try:
      print("DEBUG 2: About to import mt5_pools")
      from .pool import mt5_pools
      
      print("DEBUG 3: About to connect")
      # Initialize connections when Django is ready
      print("Connecting to MT5 servers")
      connection_results = mt5_pools.connect_all()
      print("MT5 Connection Results:", connection_results)
      mt5_pools.setup_sinks()
      print("DEBUG 4: About to setup callbacks")
      print("Setting up MT5 callbacks")
      # Setup test callbacks
      from .. import on_user_update, on_user_delete, on_deal_add  # Import callbacks
      mt5_pools.add_user_callback('user_update', on_user_update)
      mt5_pools.add_user_callback('user_delete', on_user_delete)
      mt5_pools.add_deal_callback('deal_add', on_deal_add)
      print("MT5 callbacks registered")
      print("DEBUG 5: Ready method completed")
        
    except Exception as e:
      print(f"ERROR in ready(): {str(e)}")
      raise 