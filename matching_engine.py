

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
#! TODO : MAKE A VISIBLE GRAPH OF THE MATCHING ENGINE , IN TREE FORMAT OR OTHER FORMATS EXPLORE 
#! There are other ways to fill the orderbook other than FIFO , explore them 
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
                    { "order_id": 4, "user_id": 102, "qty": 0.5, "filled_qty": 0.1 },
                    { "order_id": 11, "user_id": 305, "qty": 1.0, "filled_qty": 0 },
                    { "order_id": 15, "user_id": 408, "qty": 0.3, "filled_qty": 0 },
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
#? We have ton manually implement FIFO Structure in the Machine engine 
#? I.e  filled_qty section will get filled in order in which thet appeqar in  orderbook 
#? Consider the bids section price 67100 it has thrtee orders so whenever 
#? Someone comes to sell first all of userId 102 will get filled then , then userId 305 then 408 and ... 
# ? It should not happen that 
def match(incoming_request,orderbook):
    # step1: Access the orderbook of that particular asset
    asset_name=incoming_request["symbol"]
    asset_book=orderbook[asset_name]
    bid_portion=asset_book["bids"]
    ask_portion=asset_book["asks"]
    # print(orderbook_current_asset )
    if incoming_request["type"]=="MARKET":
        #! We modifies andn play around with the bid portion if side is SELL 
        # In this part u are assigning the values to initial empty soreted price object 
        bid_portion["sorted_prices"]=SortedList(bid_portion["price_map"].keys(),key=lambda x: -x)
        best_price=bid_portion["sorted_prices"][0]
        # This gives a list of orders corresponding to the best price       
        orderList_best_price=bid_portion["price_map"][best_price]
        for order in orderList_best_price :
            # print(order)
            order_id=order["order_id"]
            # This gives available qty for this particular order_id
            remain_qty=order["qty"]-order["filled_qty"] # This is the quantiy which needs to be filled for the user to moove out of orderbook
            # print(avail_qty)
            requested_qty=incoming_request["qty"]  # This is the quantity to be sold 
            trade_qty=min(remain_qty,requested_qty)
            if remain_qty<requested_qty:
            # In this case the order will get completed but this particular maker wont move out of order book
                trade_qty=remain_qty

                #This trade part is used to update the fills table 
                trade_record={
                    "price":best_price,
                    "qty" : trade_qty,
                    "maker_id":order["user_id"],
                    "taker_id":incoming_request["userId"]
                        }
            
            # upgrade the  the filled qty of this order id by filled+trade_qty
            order["filled_qty"]=order["filled_qty"]+trade_qty
            print("This is the Order ",order)
            if remain_qty==0:
                removed_item=order.popleft()
                print(type(removed_item))
                print("Item to be removed",removed_item)
                
            # print(remain_qty)
            break 
                
            
match(incoming_request,orderbook)

























            # match_market_order()

#         # return orderbook_current_asset

# def match_market_order():
#     if incoming_request["side"]=="SELL":
#         #This should give  me the Orderbook for the current asset
#         pass


