import time
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import pandas as pd
import numpy as np
import strategies
from decimal import Decimal as D





class robot:
    def __init__(self, api_key, api_secret,parite,period,quantity,marj):
        self.api_key = api_key
        self.api_secret = api_secret
        self.period = period
        self.parite = parite
        self.quantity = quantity
        self.client = Client(api_key, api_secret)
        self.ticker = None
        self.marj = marj
        self.last = None
        rule_book = {}
        self.transaction = None
        self.signal = None
        self.last_red = 0

    def historical_data(self):
        
        klines = self.client.get_historical_klines(self.parite, self.period, "1 day ago UTC")
        df = pd.DataFrame(klines, columns =['Open Time', 'Open','High','Low','Close','Volume','Close time','Quote asset volume','Number of trades','Taker buy base asset volume','Taker buy quote asset volume','Can be ignored']).astype(float)
        df['Mum Rengi'] = np.where(df['Close']-df['Open']>=0,1,0)
        df['Mum Boyu'] = df['High']-df['Low']
        dfi = df[:-1]
        self.last_red_candle_ID =dfi[dfi["Mum Rengi"] == 0]["Open Time"].iloc[-1]
        self.data = df
    

    def adjusted_ticker(self):
        info = self.client.get_symbol_info(symbol=self.parite)
        self.price_filter = float(info['filters'][0]['tickSize'])
    
    def spot_ticker(self):
        price=self.client.get_ticker(symbol=self.parite)
        self.lastPrice=float(price['lastPrice'])
        self.askPrice=float(price['askPrice'])
        self.bidPrice=float(price['bidPrice'])
    
                   
    def buy_and_sell(self):
        order_market_buy = self.client.order_market_buy(
                    symbol=self.parite,
                    quantity=self.quantity)
        self.last_red = self.last_red_candle_ID
        self.spot_ticker()
        self.adjusted_ticker()
        order_limit_sell = self.client.order_limit_sell(
                        symbol=self.parite,
                        quantity=self.quantity,
                        #price=(D.from_float(self.bidPrice*self.marj).quantize(D(str(self.price_filter))))).astype(str)
                        price=str(self.lastPrice*self.marj))
        self.transaction = f"{self.parite} isimli paritede\n {self.quantity} miktarda\n {self.bidPrice} işlem yapıldı\n"
        
    def buy_and_sell_soldiers(self):
            order_market_buy = self.client.order_market_buy(
                    symbol=self.parite,
                    quantity=self.quantity)
            self.last_red = self.last_red_candle_ID
            self.spot_ticker()
            self.adjusted_ticker()
            order_limit_sell = self.client.order_limit_sell(
                        symbol=self.parite,
                        quantity=self.quantity,
                        price=D.from_float(self.bidPrice*self.marj*2).quantize(D(str(self.price_filter))))
            self.transaction = f"{self.parite} isimli paritede\n {self.quantity} miktarda\n {self.bidPrice} işlem yapıldı\n"
    
 #--------------------- ADD BUY ORDERS FOR STRATEGIES ABOVE AND ADD STRATEGIES BELOW ----------------------------

    def kural1(self):
        self.historical_data() #GET DATA
        self.data = self.data[:-1] # PREPARE THE DATA
        str_101 = strategies.Strategies(self.data) # GET STRATEGIES

        self.ticker = self.spot_ticker() 
        print("-----------------------------")
        self.signal = str_101.strategy_101_long(self.lastPrice) # SPECIFY THE STRATEGY
        print("sinyal bekleniyor")
        print("last red",self.last_red)
        print("last red candle id",self.last_red_candle_ID)
        if self.signal and self.last_red != self.last_red_candle_ID:  # IF TRUE BUY
            self.buy_and_sell()
            print(f"sinyal : {self.signal}")
        else:
            print('sinyal yok')
    
    def kural2(self):
        self.historical_data()
        self.data = self.data[:-1]
        str_101 = strategies.Strategies(self.data)
        
        self.ticker = self.spot_ticker()
        print("-----------------------------")
        self.signal = str_101.white_soldiers(self.lastPrice)
        print("3 beyaz asker bekleniyor")

        if self.signal:
            self.buy_and_sell_soldiers()
            print(f"sinyal : {self.signal}")
        else:
            print('white soldiers not exist')





# NECESSARY INFORMATIONS
api_key ="api"  # binance api key
api_secret = "secret" # binance api secret key
parite = "parite" # desired parite 
period = "5m" # graph time
quantity = 1.5 # how much
marj = 1.005 # profit

long_bot1 = robot(api_key, api_secret, parite, period, quantity, marj)


while True:
    

    try:
        ''' add new strategies here '''
        long_bot1.kural1() 
        long_bot1.kural2()
        time.sleep(5)

    except Exception as e: 
        print(e)


    
