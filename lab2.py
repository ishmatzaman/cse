
def trading_agent(price, avg_price, stock_level):
    
    discount_threshold = 0.20 
    critical_stock_level = 10  
    minimum_order_quantity = 10  
    normal_order_quantity = 15 
    
   
    discounted_price = avg_price * (1 - discount_threshold)
    
 
    if price < discounted_price and stock_level > critical_stock_level:
        tobuy = normal_order_quantity
    elif stock_level <= critical_stock_level:
        tobuy = minimum_order_quantity
    else:
        tobuy = 0
    
    return tobuy

average_price = 600
current_price = 450  
stock_level = 5     

order_quantity = trading_agent(current_price, average_price, stock_level)


if order_quantity > 0:
    print(f"Order {order_quantity} units of smartphones.")
else:
    print("No need to place an order.")