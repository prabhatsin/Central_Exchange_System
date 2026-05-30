from fastapi import FastAPI
from pydantic import BaseModel
app=FastAPI()
ORDERS={ }
USERS = {
    1: {
        "username": "prabhat",
        "password": "abc123"
    },
    2: {
        "username": "rahul",
        "password": "rahul@123"
    },
    3: {
        "username": "amit",
        "password": "amit@456"
    }
}


BALANCES = {
    1: {
        "INR": {
            "total": 35000,
            "locked": 10000
        },
        "AXIS": 20,
        "HDFC": 30
    },

    2: {
        "INR": {
            "total": 50000,
            "locked": 5000
        },
        "TCS": 15,
        "INFY": 25
    },

    3: {
        "INR": {
            "total": 100000,
            "locked": 0
        },
        "RELIANCE": 50
    }
}


STOCKS = {
    1: {
        "title": "Apple Inc.",
        "symbol": "AAPL"
    },
    2: {
        "title": "Microsoft Corporation",
        "symbol": "MSFT"
    },
    3: {
        "title": "Tesla Inc.",
        "symbol": "TSLA"
    }
}
class orders(BaseModel):
    userId:int
    side:str
    type:str
    stockId:int
    price:int
    qty:int

'''
incoming request:
{
  "userId": 1,
  "side": "BUY",
  "type": "LIMIT",
  "stockId": 5,
  "price": 300,
  "qty": 10
}
'''

'''
user exists?
stock exists?
qty > 0?
'''
@app.post('/order')
def create_order(ord:orders):
    #user validation, 
    # Mistake do not verify the existence of user from the Orders table ,
    # Use USERS table as source of- verification
    list_id=[key for key in USERS]
    if ord.userId not in list_id:
        return {'message':'User not found'}
    list_stId=[key for key in STOCKS]
    if ord.stockId not in list_stId:
        return {'message':'Stock not found'}
    if ord.qty<=0:
        return{'message':'The Quantity mentioned is invalid'}
    # BALANCE /ASSET CHECK
    if ord.side=='BUY':
        if ord.qty*ord.price>(BALANCES[ord.userId]['INR']['total']-BALANCES[ord.userId]['INR']['total']):
            return{"message":"Not Enough Avaibalbe balance on the user"}
        # logic to LOCK THE BALANCE 
        else:
            current_avai_bal=BALANCES[ord.userId]['INR']['total']
            prev_loced_bal=BALANCES[ord.userId]['INR']['locked']
            purchase_price=ord.price*ord.quantity
            net_aval_balance=current_avai_bal-purchase_price
            net_locked_bal=prev_loced_bal+purchase_price
            BALANCES[ord.userId]['INR']['total']==net_aval_balance
            BALANCES[ord.userId]['INR']['locked']==net_locked_bal


    if ord.side=='SELL':
        if ord.qty>BALANCES[ord.userId][STOCKS[ord.stockId]['symbol']]:
            return {'message : Available no of assets are not enough'}
        # logic to LOCK THE ASSET
        else:
            # Do One thing first change the structure of balance 
            # Similar to the INR do it for each asset as well 

    





            
    
    
    
    




