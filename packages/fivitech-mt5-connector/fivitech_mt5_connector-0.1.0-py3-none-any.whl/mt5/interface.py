from typing import Dict, Optional, Union, List, Any
from datetime import datetime
import MT5Manager
from .helpers.user import MT5UserHelper
from .helpers.transaction import MT5TransactionHelper
from .helpers.order import MT5OrderHelper
from .helpers.deal import MT5DealHelper
from .exceptions import MT5ConnectionError

class MT5UserInterface:
    """Interface for MT5 user management operations."""
    
    def __init__(self, server_id=None, server_type=None):
        self.server_id = server_id
        self.server_type = server_type
        self._helper = MT5UserHelper()

    async def create(
        self,
        FirstName: Optional[str] = None,
        LastName: Optional[str] = None,
        Email: Optional[str] = None,
        MainPassword: Optional[str] = None,
        Group: Optional[str] = None,
        Leverage: Optional[int] = None,
        **kwargs
    ) -> MT5Manager.MTUser:
        """
        Create a new MT5 user account.
        
        Args:
            FirstName (str): First name of the user (required)
            LastName (str): Last name of the user (required)
            Email (str): Email address of the user (required)
            MainPassword (str): Main trading password (required, must meet complexity requirements)
            Group (str): Trading group for the user (required, e.g., 'demo\\test')
            Leverage (int): Trading leverage (required, e.g., 100)
            **kwargs: Additional user properties
            
        Returns:
            MT5Manager.MTUser: Created user object with Login and other properties
            
        Raises:
            ValueError: If required parameters are missing or invalid
            MT5ConnectionError: If connection to MT5 fails
        """
        params = {k: v for k, v in locals().items() 
          if k not in ('self', 'kwargs') and v is not None}
        params.update(kwargs)
        
        return await self._helper.create(
            params=params,
            master_pass=MainPassword or '',
            investor_pass=kwargs.get('InvestorPassword', '') or MainPassword or '',
            server_id=self.server_id,
            server_type=self.server_type
        )

    async def get(
        self, 
        login: Union[int, List[int]]
    ) -> Union[bool, Dict[int, bool]]:
        """
        Check if one or multiple users exist by login.
        
        Args:
            login: Single user login ID or list of login IDs
            
        Returns:
            If single login: bool - True if user exists, False otherwise
            If multiple logins: Dict[int, bool] - Dictionary mapping each login to its existence status
            
        Raises:
            ValueError: If login is invalid
            MT5ConnectionError: If connection to MT5 fails
        """
        return await self._helper.exists(
            login,
            server_id=self.server_id,
            server_type=self.server_type
        )

    async def get_account_details(
        self, 
        login: Union[int, List[int]]
    ) -> Union[MT5Manager.MTUser, Dict[int, MT5Manager.MTUser]]:
        """
        Get detailed account information for one or multiple users.
        
        Args:
            login: Single user login ID or list of login IDs
            
        Returns:
            If single login: Trading account object
            If multiple logins: Dictionary mapping each login to its trading account object
            
        Raises:
            ValueError: If login is invalid
            MT5ConnectionError: If user not found or connection fails
        """
        return await self._helper.get_account_details(
            login,
            server_id=self.server_id,
            server_type=self.server_type
        )

    async def update(
        self,
        login: int,
        params: dict
    ) -> MT5Manager.MTUser:
        """
        Update user account properties.
        
        Args:
            login (int): User's login ID (required)
            params: Dictionary containing user details to update
            
        Returns:
            MT5Manager.MTUser: Updated user object
            
        Raises:
            ValueError: If login is invalid
            MT5ConnectionError: If user not found or connection fails
        """
        return await self._helper.update(
            login,
            params,
            server_id=self.server_id,
            server_type=self.server_type
        )

    async def delete(self, login: int) -> bool:
        """
        Delete a user account.
        
        Args:
            login (int): User's login ID
            
        Returns:
            bool: True if deletion successful, False otherwise
            
        Raises:
            ValueError: If login is invalid
            MT5ConnectionError: If user not found or connection fails
        """
        return await self._helper.delete(
            login,
            server_id=self.server_id,
            server_type=self.server_type
        )

    async def archive(self, login: Union[int, List[int]]) -> Union[bool, Dict[int, bool]]:
        """
        Move one or multiple user accounts to the archive database.
        
        Args:
            login: Single user login ID or list of login IDs
            
        Returns:
            If single login: bool - True if archival successful
            If multiple logins: Dict[int, bool] - Dictionary mapping each login to its archive success status
            
        Raises:
            ValueError: If login is invalid or user not found
            MT5ConnectionError: If connection fails or operation fails
        """
        return await self._helper.archive(
            login,
            server_id=self.server_id,
            server_type=self.server_type
        )

    async def restore(
        self, 
        login: Union[int, List[int]]
    ) -> Union[MT5Manager.MTUser, Dict[int, MT5Manager.MTUser]]:
        """
        Restore one or multiple user accounts from the archive database.
        
        Args:
            login: Single user login ID or list of login IDs
            
        Returns:
            If single login: Restored user object
            If multiple logins: Dictionary mapping each login to its restored user object or None if restoration failed
            
        Raises:
            ValueError: If login is invalid or user not found in archive
            MT5ConnectionError: If connection fails or operation fails
        """
        return await self._helper.restore(
            login,
            server_id=self.server_id,
            server_type=self.server_type
        )

    async def change_password(
        self,
        login: int,
        password: str,
        password_type: str = 'main'
    ) -> bool:
        """
        Change user's password.
        
        Args:
            login (int): User's login ID
            password (str): New password (must meet complexity requirements)
            password_type (str): Type of password to change ('main' or 'investor')
            
        Returns:
            bool: True if password change successful
            
        Raises:
            ValueError: If login is invalid, password doesn't meet requirements,
                      or password_type is invalid
            MT5ConnectionError: If user not found or connection fails
        """
        return await self._helper.change_password(
            login,
            password=password,
            password_type=password_type,
            server_id=self.server_id,
            server_type=self.server_type
        )

    async def change_group(self, login: int, new_group: str) -> MT5Manager.MTUser:
        """
        Change user's trading group.
        
        Args:
            login (int): User's login ID
            new_group (str): New trading group name
            
        Returns:
            MT5Manager.MTUser: Updated user object
            
        Raises:
            ValueError: If login is invalid or group doesn't exist
            MT5ConnectionError: If user not found or connection fails
        """
        return await self._helper.change_group(
            login,
            new_group=new_group,
            server_id=self.server_id,
            server_type=self.server_type
        )

    async def set_user_rights(
        self,
        login: int,
        rights_to_set: Optional[List[int]] = None,
        rights_to_remove: Optional[List[int]] = None
    ) -> MT5Manager.MTUser:
        """
        Set or modify user rights.
        
        Args:
            login (int): User's login ID
            rights_to_set (List[int], optional): List of rights to enable
            rights_to_remove (List[int], optional): List of rights to disable
            
        Returns:
            MT5Manager.MTUser: Updated user object with new rights
            
        Raises:
            ValueError: If login is invalid or no rights specified
            MT5ConnectionError: If user not found or connection fails
        """
        return await self._helper.set_user_rights(
            login,
            rights_to_set=rights_to_set,
            rights_to_remove=rights_to_remove,
            server_id=self.server_id,
            server_type=self.server_type
        )

    async def change_status(self, login: int, enable: bool) -> MT5Manager.MTUser:
        """
        Enable or disable user account.
        
        Args:
            login (int): User's login ID
            enable (bool): True to enable account, False to disable
            
        Returns:
            MT5Manager.MTUser: Updated user object
            
        Raises:
            ValueError: If login is invalid
            MT5ConnectionError: If user not found or connection fails
        """
        return await self._helper.change_status(
            login,
            enable=enable,
            server_id=self.server_id,
            server_type=self.server_type
        )

    async def change_trade_status(self, login: int, enable: bool) -> MT5Manager.MTUser:
        """
        Enable or disable trading for user.
        
        Args:
            login (int): User's login ID
            enable (bool): True to enable trading, False to disable
            
        Returns:
            MT5Manager.MTUser: Updated user object
            
        Raises:
            ValueError: If login is invalid
            MT5ConnectionError: If user not found or connection fails
        """
        return await self._helper.change_trade_status(
            login,
            enable=enable,
            server_id=self.server_id,
            server_type=self.server_type
        )

    async def change_expert_status(self, login: int, enable: bool) -> MT5Manager.MTUser:
        """
        Enable or disable Expert Advisors for user.
        
        Args:
            login (int): User's login ID
            enable (bool): True to enable EAs, False to disable
            
        Returns:
            MT5Manager.MTUser: Updated user object
            
        Raises:
            ValueError: If login is invalid
            MT5ConnectionError: If user not found or connection fails
        """
        return await self._helper.change_expert_status(
            login,
            enable=enable,
            server_id=self.server_id,
            server_type=self.server_type
        )

    async def change_reports_status(self, login: int, enable: bool) -> MT5Manager.MTUser:
        """
        Enable or disable reports access for user.
        
        Args:
            login (int): User's login ID
            enable (bool): True to enable reports, False to disable
            
        Returns:
            MT5Manager.MTUser: Updated user object
            
        Raises:
            ValueError: If login is invalid
            MT5ConnectionError: If user not found or connection fails
        """
        return await self._helper.change_reports_status(
            login,
            enable=enable,
            server_id=self.server_id,
            server_type=self.server_type
        )

    async def check_balance(self, login: int) -> Dict[str, Any]:
        """
        Check user's balance for discrepancies.
        
        Args:
            login (int): User's login ID
            
        Returns:
            Dict[str, Any]: Balance check result with keys:
                - success (bool): True if check completed
                - has_discrepancy (bool): True if balance discrepancy found
                - error (str, optional): Error message if check failed
            
        Raises:
            ValueError: If login is invalid
            MT5ConnectionError: If user not found or connection fails
        """
        return await self._helper.check_balance(
            login,
            server_id=self.server_id,
            server_type=self.server_type
        )

    async def fix_balance(self, login: int) -> Dict[str, Any]:
        """
        Fix user's balance discrepancies.
        
        Args:
            login (int): User's login ID
            
        Returns:
            Dict[str, Any]: Balance fix result with keys:
                - success (bool): True if fix completed
                - was_fixed (bool): True if balance was fixed
                - error (str, optional): Error message if fix failed
            
        Raises:
            ValueError: If login is invalid
            MT5ConnectionError: If user not found or connection fails
        """
        return await self._helper.fix_balance(
            login,
            server_id=self.server_id,
            server_type=self.server_type
        )

class MT5TransactionInterface:
    """Interface for MT5 transaction operations."""
    
    def __init__(self, server_id=None, server_type=None):
        self.server_id = server_id
        self.server_type = server_type
        self._helper = MT5TransactionHelper()

    async def deposit(self, login: int, amount: float, comment: str) -> Dict:
        """Deposit funds to user account"""
        return await self._helper.deposit(
            login=login,
            amount=amount,
            comment=comment,
            server_id=self.server_id,
            server_type=self.server_type
        )

    async def withdraw(self, login: int, amount: float, comment: str) -> Dict:
        """Withdraw funds from user account"""
        return await self._helper.withdraw(
            login=login,
            amount=amount,
            comment=comment,
            server_id=self.server_id,
            server_type=self.server_type
        )

    async def credit_in(self, login: int, amount: float, comment: str) -> Dict:
        """Add credit to user account"""
        return await self._helper.credit_in(
            login=login,
            amount=amount,
            comment=comment,
            server_id=self.server_id,
            server_type=self.server_type
        )
    
    async def credit_out(self, login: int, amount: float, comment: str) -> Dict:
        """Remove credit from user account"""
        return await self._helper.credit_out(
            login=login,
            amount=amount,
            comment=comment,
            server_id=self.server_id,
            server_type=self.server_type
        )

    async def charge_in(self, login: int, amount: float, comment: str) -> Dict:
        """Add charge to user account"""
        return await self._helper.charge_in(
            login=login,
            amount=amount,
            comment=comment,
            server_id=self.server_id,
            server_type=self.server_type
        )
    
    async def charge_out(self, login: int, amount: float, comment: str) -> Dict:
        """Remove charge from user account"""
        return await self._helper.charge_out(
            login=login,
            amount=amount,
            comment=comment,
            server_id=self.server_id,
            server_type=self.server_type
        )

    async def correction(self, login: int, amount: float, comment: str) -> Dict:
        """Make balance correction"""
        return await self._helper.correction(
            login=login,
            amount=amount,
            comment=comment,
            server_id=self.server_id,
            server_type=self.server_type
        )

    async def bonus_in(self, login: int, amount: float, comment: str) -> Dict:
        """Add bonus to user account"""
        return await self._helper.bonus_in(
            login=login,
            amount=amount,
            comment=comment,
            server_id=self.server_id,
            server_type=self.server_type
        )

    async def bonus_out(self, login: int, amount: float, comment: str) -> Dict:
        """Remove bonus from user account"""
        return await self._helper.bonus_out(
            login=login,
            amount=amount,
            comment=comment,
            server_id=self.server_id,
            server_type=self.server_type
        )

    async def add_commission(self, login: int, amount: float, comment: str) -> Dict:
        """Add commission to user account"""
        return await self._helper.add_commission(
            login=login,
            amount=amount,
            comment=comment,
            server_id=self.server_id,
            server_type=self.server_type
        )

    async def add_rebate(self, login: int, amount: float, comment: str) -> Dict:
        """Add rebate to user account"""
        return await self._helper.add_rebate(
            login=login,
            amount=amount,
            comment=comment,
            server_id=self.server_id,
            server_type=self.server_type
        )

    async def compensation(self, login: int, amount: float, comment: str) -> Dict:
        """Add compensation to user account"""
        return await self._helper.compensation(
            login=login,
            amount=amount,
            comment=comment,
            server_id=self.server_id,
            server_type=self.server_type
        )
    
class MT5OrderInterface:
    """Interface for MT5 order operations."""
    
    def __init__(self, server_id=None, server_type=None):
        self.server_id = server_id
        self.server_type = server_type
        self._helper = MT5OrderHelper()
    
    async def get_open(self, login: int) -> List[MT5Manager.MTOrder]:
        """Get open orders for a user"""
        return await self._helper.get_open(
            login=login,
            server_id=self.server_id,
            server_type=self.server_type
        )
    
    async def add(self, params: dict) -> MT5Manager.MTOrder:
        """Create an order"""
        return await self._helper.add(
            params=params,
            server_id=self.server_id,
            server_type=self.server_type
        )

    async def delete(self, ticket: int) -> bool:
        """
        Delete a trade order
        
        Args:
            ticket: Order ticket number
            
        Returns:
            bool: True if order was successfully deleted
            
        Raises:
            ValueError: If ticket is invalid
            MT5ConnectionError: If deletion fails
        """
        return await self._helper.delete(
            ticket=ticket,
            server_id=self.server_id,
            server_type=self.server_type
        )

class MT5DealInterface:
    """Interface for MT5 deal operations."""
    
    def __init__(self, server_id=None, server_type=None):
        self.server_id = server_id
        self.server_type = server_type
        self._helper = MT5DealHelper()

    async def get_paged(
        self,
        login: int,
        from_date: Union[datetime, int],
        to_date: Union[datetime, int],
        offset: int = 0,
        total: int = 100
    ) -> List[MT5Manager.MTDeal]:
        """Get deals for a user"""
        return await self._helper.get_paged(
            login=login,
            from_date=from_date,
            to_date=to_date,
            offset=offset,
            total=total,
            server_id=self.server_id,
            server_type=self.server_type
        )

class MT5Interface:
    """Main interface for MT5 operations"""
    
    def __init__(self, server_id=None, server_type=None):
        self.server_id = server_id
        self.server_type = server_type
        self.user = MT5UserInterface(server_id, server_type)
        self.transaction = MT5TransactionInterface(server_id, server_type)
        self.order = MT5OrderInterface(server_id, server_type)
        self.deal = MT5DealInterface(server_id, server_type)
    
    @classmethod
    def for_server_id(cls, server_id: int) -> 'MT5Interface':
        """Create interface instance for specific server ID"""
        return cls(server_id=server_id)
    
    @classmethod
    def for_server_type(cls, server_type: str, server_id: Optional[int] = None) -> 'MT5Interface':
        """Create interface instance for specific server type"""
        return cls(server_type=server_type, server_id=server_id)
