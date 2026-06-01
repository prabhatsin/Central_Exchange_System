

# from collections import deque
# from sortedcontainers import SortedList
# orderbook={ 
#     "AXIS":{
#     "ASK":{ 
#         "price_map":{},  # dict  { price → deque of orders }
#         "sorted_prices": SortedList() # ASC
        
#     },
#     "BID":{
#         "price_map":{}, # dict  { price → deque of orders }
#         "sorted_prices": SortedList(key=lambda x: -x)  # DESC
#         # Explore About the 'key' argument
               
#     }

#     }
# }


'''
What is a deque?
deque = Double Ended Queue
It is a linear data structure where you can add and remove from BOTH ends in O(1)
# Deque  which is double ended que is : Doubly Linked List of fixed blocks

'''

'''
input to the matching Engine
{ 
"userId":1,
"symbol": 'AXIS',
"side": 'SELL',
"type": 'MARKET',
"qty": 2,
"price": NULL,
}
'''
from collections import deque
from sortedcontainers import SortedList

orderbook = {
    "AXIS": {
        "asks": {
            "price_map": {
                # price → deque of individual orders
                67200: deque([
                    { "order_id": 1, "user_id": 101, "qty": 1.0, "filled_qty": 0 },
                    { "order_id": 2, "user_id": 205, "qty": 1.5, "filled_qty": 0 },
                ]),
                67250: deque([
                    { "order_id": 3, "user_id": 309, "qty": 0.8, "filled_qty": 0 },
                ]),
            },
            "sorted_prices": SortedList()  # [67200, 67250] ASC → best ask at index 0
        },
        "bids": {
            "price_map": {
                67100: deque([
                    { "order_id": 4, "user_id": 102, "qty": 0.5, "filled_qty": 0 },
                ]),
                67050: deque([
                    { "order_id": 5, "user_id": 201, "qty": 1.2, "filled_qty": 0 },
                ]),
            },
            "sorted_prices": SortedList(key=lambda x: -x)  # [67100, 67050] DESC → best bid at index 0
        }
    }
}


incoming_request={ 
"userId":1,
"symbol": 'AXIS',
"side": 'SELL',
"type": 'MARKET',
"qty": 2,
"price":None
}
# Note: I m confused that the incoming request will be a json or 
# an request body object wala
def match(incoming_request,orderbook):
    # step1: Access the orderbook of that particular asset
    asset_name=incoming_request["symbol"]
    orderbook_current_asset=orderbook[asset_name]
    # print(orderbook_current_asset )
    if incoming_request["type"]=="MARKET":
        if incoming_request["side"]=="SELL":
            bid_portion=orderbook_current_asset["bids"]
            bid_portion["sorted_prices"]=SortedList(bid_portion["price_map"].keys(),key=lambda x: -x)
            best_price=bid_portion["sorted_prices"][0]
            # This gives a list of orders corresponding to the best price       
            order_best_price=bid_portion["price_map"][best_price]
            for order in order_best_price :
                print(order)
                avail_qty=order["qty"]
                print(avail_qty)
                requested_qty=incoming_request["qty"]
                net_qty=avail_qty-requested_qty

                if net_qty>=0: 
                    #! This one  Bidder wants to buy all of the requested asset @ this highest price

                    # trade will happen i.e 
                    # The quantity of asset of this userid shouold increase 
                    # Balance should deduct and move to this req wala user


                    pass
                elif net_qty<0: 
                    #! This one  Bidder wants to buy all of the requested asset @ this highest price
                    # Move to next bidder with different user id and order id 

                    continue 
                    # apply the infinite loop till the time assets are sold or 
                    # Since its a market order eventuallyb it will get sold 
    
            # print(order_best_price)
            # avail_quantity=order_best_price['qty']
            # print(avail_quantity)
            # print(order_best_price)

            # Get the list of sorted price in descending 
            return None
          

            
match(incoming_request,orderbook)

























            # match_market_order()

#         # return orderbook_current_asset

# def match_market_order():
#     if incoming_request["side"]=="SELL":
#         #This should give  me the Orderbook for the current asset
#         pass


