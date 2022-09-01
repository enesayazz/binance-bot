

class Strategies:
    """
    genel stratejiler modülü
    
    ileride yeni stratejiler eklendiğinde buraya metod olarak yazılabilir    
    
    """
    def __init__(self, dataframe):

        # obje oluşturulurken parametre olarak geçmiş mum verisi dataframe'i alır

        self.df = dataframe #geçmiş mum verisi

        self.long_signal_price = 0 #long sinyali geldiği andaki değer
        self.short_signal_price = 0 #short sinyali geldiği andaki değer
    
    def strategy_101_long(self, ticker): # long için izlenicek strateji
        # anlık fiyatın en son kırmızı mumun açılış değerini geçmesi gerekiyor        
        # ticker: anlık fiyat
        last_red_candle_open = self.df[self.df["Mum Rengi"] == 0]["Open"].iloc[-1] #son kırmızı mumun açılış değeri
        if ticker > last_red_candle_open:
            self.long_signal_price = ticker #sinyal değeri değişkene atandı
            return True
        else:
            self.long_signal_price = 0
            return False

    def strategy_101_short(self, ticker): # short için izlenicek strateji
        # anlık fiyatın en son yeşil mumun kapanış değerini geçmesi gerekiyor        
        # ticker: anlık fiyat
        last_green_candle_open = self.df[self.df["Mum Rengi"] == 0]["Close"].iloc[-1] #son yeşil mumun kapanış değeri
        if ticker > last_green_candle_open:
            self.short_signal_price = ticker #sinyal değeri değişkene atandı
            return True
        else:
            self.short_signal_price = 0
            return False

    def get_long_signal_price(self): #long sinyal değeri için fonksiyon
        return self.long_signal_price

    def get_short_signal_price(self): #short sinyal değeri için fonksiyon
        return self.short_signal_price

    def white_soldiers(self,ticker):
        last_green_candle_1 = self.df["Mum Rengi"].iloc[-1]
        last_green_candle_2 = self.df["Mum Rengi"].iloc[-2]
        last_green_candle_3 = self.df["Mum Rengi"].iloc[-3]
        if last_green_candle_1 == last_green_candle_2 == last_green_candle_3 == 1:
            self.soldier_signal_price = ticker
            return True
        else:
            self.soldier_signal_price = 0
            return False
    
    def get_white_soldiers_signal_price(self):
        return self.soldier_signal_price