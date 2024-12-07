# CryptoApi

__CryptoAPI__ is a powerful Python library designed to simplify interaction with various cryptocurrency APIs.

 It offers a user-friendly typed interface to .
1) fetch real-time market data
2) historical data
3) execute trades.

**Key Features:**

-   ****Real-time Data****: Access to real-time market data, including prices, volumes, and order books.
-   ****Historical Data****: Retrieve historical price and trading data.
-   ****WebSockets****: Establish persistent connections for live updates and event-driven programming.
-   ****REST API****: Interact with RESTful APIs for flexible data retrieval with **typed responses and parameters**.
-   ****Asynchronous Support****: Efficiently handle multiple API requests concurrently.
-   ****Error Handling****: Robust error handling and informative error messages.
-****Typed API**  -Responeses of requests are returned as pydantic types 

** EXAMPLE app.py **
    import numpy as np
    from binance_client.BinanceAuth import BinanceAuth
    from binance_client.BinanceFuturesClient import BinanceFuturesClient
    from binance_client.BinanceTrader import BinanceTrader

    
    api_key=os.environ['BINANCE_API_KEY'] # you can store your credintials in environment variables
    api_secret=os.environ['BINANCE_API_SECRET']

    auth_data=BinanceAuth(api_key,api_secret) #pass your binance credintials

    symbols = ["BTCUSDT", "ADAUSDT"] # choose symbols
    trader=BinanceTrader(auth_data,symbols,is_paper_trading=True) # create BinanceTrader so you have access to trading functionality
    


    def run_test_cases(trader: BinanceTrader):

        def log_hedge(row:TicketRow): #function which reacts to price changes
            print(row)
            prices_dict=row.prices
            keys=trader.symbols
            betas=[1,-1]


            order_dict=row.prices.copy()

            sum=0.0

            for i in range(0,len(keys) -1) :
                key=keys[i]
                price=np.log(prices_dict[key])* abs(betas[i])
                order_dict[key]=price
                sum+=price

            
            for i in range(0,len(keys) -1) :
                v=order_dict[key]
                v/=sum
                v= v if betas[i]>1 else -v
                order_dict[key]=v


            print("order_dict")
            print(order_dict)
            return trader.modify_order(order_dict)
        
        def getBetas()->tuple[float,float]:{
            1,-1 
        }
        
        trader.setSingleOnNextUpdate(log_hedge)

        trader.run()

You have just written a simple function that reacts to prices, of course you can refine it, e.g. calculate beta coefficients from regression and add additional explaination variables eg.inflation .
After entering the quantity in `modify_order`, the difference from the current orders is converted into market orders.


# Stages of development
1) fetch real-time market data execute trades (binance,REST)
2) websocket support , hedging positions

