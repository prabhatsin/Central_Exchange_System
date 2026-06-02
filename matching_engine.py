

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
                    { "order_id": 1, "user_id": 101, "qty": 10, "filled_qty": 0 },
                    { "order_id": 2, "user_id": 205, "qty": 15, "filled_qty": 0 },
                ]),
                67250: deque([
                    { "order_id": 3, "user_id": 309, "qty": 8, "filled_qty": 0 },
                ]),
            },
            "sorted_prices": SortedList()  # [67200, 67250] ASC → best ask at index 0
        },
        "bids": {
            "price_map": {
                67100: deque([
                    { "order_id": 4, "user_id": 102, "qty": 5, "filled_qty": 0 },
                    { "order_id": 11, "user_id": 305, "qty": 6, "filled_qty": 0 },
                    { "order_id": 15, "user_id": 408, "qty": 3, "filled_qty": 0 },
                ]),
                67050: deque([
                    { "order_id": 5, "user_id": 201, "qty": 12, "filled_qty": 0 },
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
"qty": 19,
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
           # In this part u are assigning the values to initial empty soreted price object 
    bid_portion["sorted_prices"]=SortedList(bid_portion["price_map"].keys(),key=lambda x: -x)
    if incoming_request["type"]=="MARKET":
        #! We modifies andn play around with the bid portion if side is SELL 
        # This gives a list of orders corresponding to the best price 
        requested_qty=incoming_request["qty"] 
        orders_to_update= []   #? This will be used to update orders db later 
        trades_executed = []   #? This will be used to updatwe fills table 
        while len(bid_portion["sorted_prices"]) >0:
            best_price=bid_portion["sorted_prices"][0]
            orderList_best_price=bid_portion["price_map"][best_price]
            
            while len(orderList_best_price)>0:

                order=orderList_best_price[0]
                # print("The order value is ",order)
                order_id=order["order_id"]
                remain_qty=order["qty"]-order["filled_qty"]
                trade_qty=min(remain_qty,requested_qty)
                trade_record={
                    "price":best_price,
                    "qty" : trade_qty,
                    "maker_id":order["user_id"],

                    "taker_id":incoming_request["userId"]
                        }
                trades_executed.append(trade_record)
                order["filled_qty"]=order["filled_qty"]+trade_qty
                remain_qty_after=order["qty"]-order["filled_qty"]
                # Upgrade the incoming_request["qty"]
                requested_qty=requested_qty-trade_qty
                # print("The left out part of ",requested_qty)
                # print(trades_executed)
                if remain_qty_after==0:
                    removed_item=orderList_best_price.popleft()

                    orders_to_update.append(removed_item)

                else:
                    pass 
                    # Write a else condition for partial fill status update 

        
            
                #! Stop the loop if all of incoming_request['qty'] is sold 
                if requested_qty==0:
                    #? use this condition in the along with the whiole loop better approach 
                    print("The loop breaks here --------")
                    break
            print("Final Value of requested qty",requested_qty)
            print("My final order update is",orders_to_update)
            # print("Final trade record",trades_executed)
            print(orderList_best_price)
            del bid_portion["price_map"][best_price]
            bid_portion["sorted_prices"].discard(best_price)
                

        

        
            

match(incoming_request,orderbook)

























            # match_market_order()

#         # return orderbook_current_asset

# def match_market_order():
#     if incoming_request["side"]=="SELL":
#         #This should give  me the Orderbook for the current asset
#         pass


