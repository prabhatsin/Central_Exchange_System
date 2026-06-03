
#! This Script contains the matching logic of  'BUY' Part of a SPOT 'MARKET' Order 
from sortedcontainers import SortedList
# dont import sortedlist instead of SortedList , although both can be used , sortedlist 
# is the  name of the module whereas Sorted name is the direct class 
from collections import deque

#! TODO :::: After testing the functionalities , write everything in a class (OOPS)
orderbook={
    'HDFC':{
        'asks':{
            "pricemap":{
                6600:deque([{'user_id':45,'order_id':6,'qty':4,"filled":0},
                           {'user_id':56,'order_id':9,'qty':7,"filled":0},
                           {'user_id':67,'order_id':12,'qty':14,"filled":0},],
                ),

                6500:deque([{'user_id':1,'order_id':1,'qty':4,"filled":0},
                            {'user_id':5,'order_id':5,'qty':4,"filled":0},
                            {'user_id':6,'order_id':6,'qty':4,"filled":0},])
                
                },
            "sorted_prices":SortedList(key=lambda x:x)
            },

        'bids':{
            "pricemap":{
                6500:deque([{'user_id':1,'order_id':6,'qty':4,"filled":0},
                            {'user_id':1,'order_id':3,'qty':4,"filled":0},
                            {'user_id':1,'order_id':5,'qty':4,"filled":0},])
            },
            "sorted_prices":SortedList(key=lambda x:-x)
        }
    }
}
incoming_request={
    'userId': 23,
    'symbol':'HDFC',
    'qty':21,
    'side':'BUY',
    'type': 'MARKET',
    'price':None

}

def matching_engine(orderbook,incoming_request):
    asset_orderbook=orderbook["HDFC"]
    #since side is buy we get the oppositem i.e ]\
    ask_portion=asset_orderbook['asks']
    order_update=[]
    trade_done=[]
    if incoming_request['type']=='MARKET':
        price_list=list(ask_portion['pricemap'].keys())
        # print(price_list)
        sorted_price_list=SortedList(price_list)
        
        requested_quantity=incoming_request["qty"]

        while    len(sorted_price_list)>0 and requested_quantity>0:
            
            best_ask_price=sorted_price_list[0]

            while len(ask_portion["pricemap"][best_ask_price])>0 and requested_quantity>0:

                order=ask_portion["pricemap"][best_ask_price][0]
                # The quantity he has available to sell at this price
                remain_qty=order["qty"]-order['filled']
                # here remain=4,
                # requested= 8
                trade_qty=min(remain_qty,requested_quantity)
                # update the fill quantity 
                order["filled"]=order["filled"]+trade_qty

                trade={
                    'price':best_ask_price,
                    'qty':trade_qty,
                    'maker_id':order["user_id"],
                    'taker_id':incoming_request['userId']
                }
                trade_done.append(trade)
                remain_qty_after=order["qty"]-order['filled']
                requested_quantity=requested_quantity-trade_qty
                # print("The left requested quantity ",requested_quantity)
                import copy
                if remain_qty_after==0:
                    removed_item=ask_portion['pricemap'][best_ask_price].popleft()
                    removed_item["Status"]='filled'
                    # print(ask_portion['pricemap'][best_ask_price])
                    # print(removed_item)
                    order_update.append(removed_item)
                else:
                    unremoved_item=copy.copy(ask_portion["pricemap"][best_ask_price][0])
                    unremoved_item["status"]='partially_filled'
                    order_update.append(unremoved_item)
                    # print(type(removed_item))
            # Delete the best aked price from the sorted_list   
            sorted_price_list.discard(best_ask_price)
            # print("The sorted price list is",sorted_price_list)
            ask_portion['pricemap'].pop(best_ask_price,None)
            # print("The leftc part of the ask dict",ask_portion['pricemap'])
        # print("The final val;ue of requested_quantity",requested_quantity)
        # print('The final trade_list is', trade_done)
        print('The final order update list  is', order_update)


        #! Add a case where if no order left to match in the orderbook ,
        #! Nothing left for the match 





                

                

                








                
                




                # print(best_ask_price)
                # print(order)












        
matching_engine(orderbook,incoming_request)




     

