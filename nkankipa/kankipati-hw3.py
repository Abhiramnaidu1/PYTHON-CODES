"""
CS620
HW3
@author: Abhiram Naidu Kankipati
"""

from pandas import Series, DataFrame
import pandas as pd
import xml.etree.ElementTree as ET
import numpy as np



#20 pts for correct ticker_find implementation
def ticker_find(root, ticker):
   name = 'No data in SP500'
   for tick in root:
      if (ticker == tick.attrib['ticker']):
        name = tick.attrib['name']
  # add your code here
        return name


#20pts for correct calc_avg_open implementation
def calc_avg_open(sp500_data, ticker):
    avg = 0.0
    # add your code here
    avg = sp500_data[sp500_data.Symbol==ticker]['Open'].mean()
    return avg

#20pts for calc_vwap correct implementation
def calc_vwap(sp500_data, ticker):
    vwap = 0.0
    # add your code here
    eachDayAvg=((sp500_data['High']+sp500_data[sp500_data.Symbol==ticker]['Low']+sp500_data[sp500_data.Symbol==ticker]['Close'])/3)*sp500_data[sp500_data.Symbol==ticker]['Volume']
    totalSum=sp500_data[sp500_data.Symbol==ticker]['Volume'].sum()
    vwap=eachDayAvg.sum()/totalSum
    return vwap

#40pts for calc_mfi correct implementation
def calc_mfi(company_data):
    mfi = 0.0
    typical_price= (company_data['High']+company_data['Low']+company_data['Close'])/3
    money_flow = company_data['Volume']*typical_price
    typical_price_shift=typical_price.shift(periods=-1,fill_value=0)
    flow=pd.DataFrame()
    flow['value1']=typical_price
    flow['value2']=typical_price_shift
    flow['moneyflow'] = money_flow
    flow['less']=typical_price.lt(typical_price_shift)
    flow['great']=typical_price.gt(typical_price_shift)
    positive_flow=flow[flow.less==True]['moneyflow'].values
    negative_flow=flow[ flow.great==True]['moneyflow'].values[0:-1]
    money_ratio=sum(positive_flow)/negative_flow.sum()
    mfi=100-(100/(1+money_ratio))
    # add your code here
    return mfi

# --------------------------------------
# do not modify below this line
# --------------------------------------
def read_files():
    xmltree = ET.parse('SP500_symbols.xml')
    xmlroot = xmltree.getroot()
    sp500 = pd.read_csv('SP500_ind.csv')
    tickers = sp500['Symbol'].unique()
    return xmlroot,sp500,tickers

if __name__ == '__main__':
  xmlroot, sp500, tickers = read_files()

  for ticker in tickers:
    name = ticker_find(xmlroot, ticker)
    ticker_data = sp500[sp500.Symbol==ticker]
    print("Ticker:",ticker, "Name:", name,  "Avg: %.2f" % calc_avg_open(sp500, ticker), "VWAP: %.2f" % calc_vwap(sp500,ticker), "MFI:  %.2f" % calc_mfi(ticker_data))