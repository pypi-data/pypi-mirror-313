import pytest
from datetime import datetime, timedelta
from fivitech_mt5_connector.exceptions import MT5ConnectionError

@pytest.mark.asyncio
async def test_deal_update(mt5_demo_connection):
    """Test updating a deal"""
    # First get a deal to update
    deals = await mt5_demo_connection.deal.get_paged(
        login=12345,  # Use a known test login
        from_date=datetime.now() - timedelta(days=1),
        to_date=datetime.now(),
        offset=0,
        total=1
    )
    
    assert deals, "No deals found to test update"
    
    # Try to update the deal
    deal_id = deals[0].Deal
    updated_deal = await mt5_demo_connection.deal.update(
        deal_id=deal_id,
        params={
            'Comment': 'Updated by test',
            'Profit': 100.50,
            'Commission': 1.50
        }
    )
    
    assert updated_deal is not None
    assert updated_deal.Comment == 'Updated by test'
    assert updated_deal.Profit == 100.50
    assert updated_deal.Commission == 1.50

@pytest.mark.asyncio
async def test_deal_update_invalid_id(mt5_demo_connection):
    """Test updating a deal with invalid ID"""
    with pytest.raises(ValueError):
        await mt5_demo_connection.deal.update(
            deal_id=-1,
            params={'Comment': 'Test'}
        )

@pytest.mark.asyncio
async def test_deal_update_nonexistent(mt5_demo_connection):
    """Test updating a nonexistent deal"""
    with pytest.raises(MT5ConnectionError):
        await mt5_demo_connection.deal.update(
            deal_id=999999999,
            params={'Comment': 'Test'}
        ) 