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
        "AXIS": {"total":15,
                "locked":1
        },
        "HDFC": {"total":16,
                "locked":3
        }
    },

    2: {
        "INR": {
            "total": 50000,
            "locked": 5000
        },
        "TCS": {"total":15,
                "locked":1
        },
        "INFY":{"total": 25,
                "locked":2
        }
    },

    3: {
        "INR": {
            "total": 100000,
            "locked": 0
        },
        "RELIANCE": {"total":15,
                "locked":1
        }
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
  "stockId": 5,        # Usually name stock name in the incoming request ,
  "price": 300,        # We get the stockId from the name in the logic section 
  "qty": 10
}
'''

@app.post('/order')
def create_order(ord:orders):
    #user validation, 
    # Mistake do not verify the existence of user from the Orders table ,
    # Use USERS table as source of- verification

    '''
    user exists?
    stock exists?
    qty > 0?
    '''
    list_id=[key for key in USERS]

    # User_validation 
    #! TODO : User validation usually happens from JWT tokens this is the wrong approach 
    #! Just extract the user_id from the JWT token and attach here 
    if ord.userId not in list_id:
        return {'message':'User not found'}
    list_stId=[key for key in STOCKS]
    
    #! TODO : Resolve symbol → market_id
    #! Usually stock symbol appears in req body we extract the stock id for corresposnding 
    #! stock
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
            total_avai_bal=BALANCES[ord.userId]['INR']['total']
            prev_loced_bal=BALANCES[ord.userId]['INR']['locked']
            purchase_price=ord.price*ord.quantity
            net_aval_balance=total_avai_bal-purchase_price
            net_locked_bal=prev_loced_bal+purchase_price
            BALANCES[ord.userId]['INR']['total']==net_aval_balance
            BALANCES[ord.userId]['INR']['locked']==net_locked_bal
            # Save order to DB (status: PENDING)
            ORDERS.update(ord)
            # Call Matching Engine
            # Return Final Response

    #! For every faliure give a status code ,
    if ord.side=='SELL':
        if ord.qty>BALANCES[ord.userId][STOCKS[ord.stockId]['symbol']]:
            return {'message : Available Number  of assets are not enough'}
        # logic to LOCK THE ASSET
        else:
            stock_name=STOCKS[ord.stockId]["title"]
            total_avaialble_assest=BALANCES[ord.userId][stock_name]['total']
            prev_locked_asset=BALANCES[ord.userId][stock_name]['locked']
            net_aval_asset=total_avaialble_assest-ord.qty
            BALANCES[ord.userId][stock_name]['total']==net_aval_asset
            BALANCES[ord.userId][stock_name]['locked']==prev_locked_asset+ord.qty
            # Save order to DB (status: PENDING)
            ORDERS.update(ord)
            # Call Matching Engine
            # Return Final  Response
###! 
'''
The Balance deduction flow is like this , 
pahle total balance me se lock me gaya , qty*price (suppose buy order)
Now after matching engine is implemented wo amount will get removed from the 
lock and go into that account jisne wo stock Becha hai 


'''
#!--------------------------------------------------------------
#! write separate ;ogic for it 
    #? After the order is created give this order to MATCHING ENGINE ,




    





            
    
    
    
    




