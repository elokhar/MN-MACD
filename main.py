import pandas as pd
import matplotlib.pyplot as plt
import math



def compute_ema(data, index, periods):

    N=periods
    alpha = 2/(N+1)
    numerator = 0
    denominator = 0
    
    
    for p_index in range(N):
        denominator += pow(1-alpha, p_index)
        data_index = index-p_index
        numerator += pow(1-alpha, p_index) * data[data_index]
    EMA=numerator/denominator 
    return EMA



def buy_sell(prices, macd, signal):

    dollars = 1000
    euro = 0
    capital = [0]*(len(prices))
    capital[34] = dollars + euro/prices[34]
    macd_to_signal = macd[34]>signal[34]

    for index in range(35,len(prices)):

        if macd_to_signal != (macd[index]>signal[index]):

            macd_to_signal = macd[index]>signal[index]

            if macd_to_signal == 1:
                sold = round(dollars,2)
                bought = round(sold*prices[index],2)
                dollars -= sold
                euro += bought
                print("I bought ",bought, "€ for", sold, "$. Exchange rate: ", round(prices[index],4))
                
            else:
                sold = round(euro)
                bought = round(sold/prices[index],2)
                dollars += bought
                euro -= sold
                print("I sold", sold, " € for", bought, "$. Exchange rate: ", round(prices[index],4))

        capital[index]=dollars+euro/prices[index]

    dollars=round(dollars,2)
    euro=round(euro,2)

    print("Now I have ", dollars, "$ and ", euro, "€")
    dollars += round(euro/prices[-1],2)
    print("After selling all €, I have ", dollars, "$")
    
    capital[-1]=dollars
    return capital
    


data = pd.read_csv('euro.csv', parse_dates=['Date'], 
    index_col=['Date'])
data = data[data["Country"]=="Euro"]
data = data.dropna()
data = data[-1000:]

values = data["Exchange rate"]

macd = [0]*len(data)
signal = [0]*len(data)

for index in range(25,len(data)):
    macd[index]=compute_ema(values,index,12)-compute_ema(values,index,26)

for index in range(34,len(data)):
    signal[index]=compute_ema(macd,index,9)


capital = buy_sell(values, macd, signal)
capital_df=data.rename(columns={"Exchange rate":"Capital"})
capital_df["Capital"]=capital
capital_df=capital_df[34:]
capital_df.plot(title="Total owned capital in USD")

data.plot(title="Euro to usd exchange rate")

macd_df = data.rename(columns={"Exchange rate":"MACD"})
macd_df["MACD"]=macd
ax = macd_df.plot(label="MACD", title="MACD and Signal lines")

signal_df = data.rename(columns={"Exchange rate":"Signal"})
signal_df["Signal"]=signal
signal_df.plot(ax=ax, label="Signal")

plt.legend()
plt.show()
