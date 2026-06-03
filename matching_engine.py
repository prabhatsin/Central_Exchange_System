

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

'''
sortedcontainers is your biggest advantage in Python — it replaces the
 need to manually maintain sorted arrays
and gives you near Red-Black Tree performance without implementing one yourself.

what is this Red-Black Tree

'''

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

# Note:I m confused that the incoming request will be a json or an request body object wala
#! First in first out (FIFO)
#? We have to manually implement FIFO Structure in the Matching engine 
#? i.e  filled_qty section will get filled in order in which thet appear in  orderbook 
#? Consider the bids section price 67100 it has thrtee orders so whenever 
#? Someone comes to sell first all of userId 102 will get filled then , then userId 305 then 408 and ... 
def match(incoming_request,orderbook):
    # step1: Access the orderbook of that particular asset
    asset_name=incoming_request["symbol"]
    asset_book=orderbook[asset_name]
    bid_portion=asset_book["bids"]
    ask_portion=asset_book["asks"]
    # In this part u are assigning the values to initial empty soreted price object 
    bid_portion["sorted_prices"]=SortedList(bid_portion["price_map"].keys(),key=lambda x: -x)
    if incoming_request["type"]=="MARKET":
        #! We modifies and play around with the bid portion if side is SELL 
        requested_qty=incoming_request["qty"] 
        # We have defined both the varioables outside the loop otherwise they get empty after the loop exits
        orders_to_update= []   #? This will be used to update orders db later 
        trades_executed = []   #? This will be used to updatwe fills table 
        #! Observe: As the trade happens requested_qty and  len(bid_portion["sorted_prices"]) and len(orderList_best_price)  keeps on decreasing 
        #! Thats the reason we keep it in the while condition 
        while len(bid_portion["sorted_prices"]) >0 and requested_qty > 0:
            # The beauty of using and in an infinite while loop is 
            # It act as a termination condition for the loop 
            # As soon as any any one condition is not met i.e any one of them becomes 0  , it comes out of the loop .
            best_price=bid_portion["sorted_prices"][0]
            # This gives a list of orders corresponding to the best price 
            orderList_best_price=bid_portion["price_map"][best_price]
            while len(orderList_best_price) >0 and requested_qty >0:
                order=orderList_best_price[0]
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
                #! Observe We are calculationg the remaining quantity twice once before trade and once after 
                #! and that aslo with two separate variables , we are doing so first (remain-qty) is used for trade logic ,
                #! and other one (remain_qty_after) is being used when order is filled in order to pop that order out of orderbook
                remain_qty_after=order["qty"]-order["filled_qty"]
                # Upgrade the incoming_request["qty"] , as soon as the trade is executed 
                requested_qty=requested_qty-trade_qty

                # print("The remaining quantity after each innerloop execution ",remain_qty)
                # print("The requested qty aft6er each inner loop execution is ",requested_qty)
                import copy
                if remain_qty_after==0:
                    # As soon as the all of the qty any user_id wanted to fill gets filled we pop that trade out of the orderbook
                    removed_item=orderList_best_price.popleft()
                    
                    removed_item.update({"status":"filled"})
                    # print("The order to be removed ", removed_item)
                    
                    #Take the filled order out of orderbook and insert it in db/ anyother list (for now)
                    orders_to_update.append(removed_item)
                
                else:
                    # unremoved_item=orderList_best_price[0]
                    # What happens is if we execute the above step then due to pass by reference of python
                    # unremoved_item is NOT a copy
                    # it is a REFERENCE to the same object in deque
                    # modifying it = modifying the original in deque
                    unremoved_item=copy.copy(orderList_best_price[0])

                    unremoved_item.update({"status":"partially_filled"})
                    orders_to_update.append(unremoved_item)

                    # Write a else condition for partial fill status update 

            # print("Final Value of requested qty after each price value of  iteration",requested_qty)
            
            #! After the inner loop has run complete one iteration we need to upgrade the best price  
            del bid_portion["price_map"][best_price] # Removing the whole dict of current best price 
            bid_portion["sorted_prices"].discard(best_price)#Remove the current best price  from the price list
            
        print("Final trade record",trades_executed)
        print("My final order update is",orders_to_update)
            
                
match(incoming_request,orderbook)


'''
#! Balance update ????????????? 
how exactly is theb Balance part getting updated or effected ??? 

'''

'''

Additional order types you may need to consider:

Cancel Order — not a new order but a core operation your engine must handle
IOC (Immediate or Cancel) — Limit order but unfilled portion is cancelled instantly
FOK (Fill or Kill) — must fill completely or cancel entirely, no partial fills
Post Only — Limit order that is rejected if it would match immediately (maker only)

'''

























            # match_market_order()

#         # return orderbook_current_asset

# def match_market_order():
#     if incoming_request["side"]=="SELL":
#         #This should give  me the Orderbook for the current asset
#         pass


