import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import unirest
from matplotlib import rcParams
import os
import json

unirest.timeout(15) # 5s timeout

RAPIDAPI_KEY = os.environ.get('RAPIDAPI_KEY')
RAPIDAPI_HOST = os.environ.get('RAPIDAPI_HOST')

symbol_string = ""
inputdata = {}

def fetchStockData(symbol):
  
  response = unirest.get("https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-charts?region=US&lang=en&symbol=" + symbol + "&interval=1d&range=3mo",
    headers={
      "X-RapidAPI-Host": RAPIDAPI_HOST,
      "X-RapidAPI-Key": RAPIDAPI_KEY,
      "Content-Type": "application/json"
    }
  )
  print(response.code)
  if(response.code == 200):
    file_path = 'stock.dat'
    mode = 'a+' if os.path.exists(file_path) else 'w+'
    try:
        print('Opening stock.dat in mode: {}'.format(mode))
        with open(file_path, mode) as f:
            f.write(json.dumps(response.body))
            print('Data written successfuly to file: {}'.format(file_path))

    except Exception as e:
        print('EXCEPTION: Error while writing to file: {}, Data type {}'.format(file_path,type(response.body)))
        print(e)

    return response.body
  else:
    print('{} statusCode: {} Exception: {}'.format('Error in ccalling Yahoo Api',response.code,response.body))
    return None


def parseTimestamp(inputdata):

  timestamplist = []

  timestamplist.extend(inputdata["chart"]["result"][0]["timestamp"])
  timestamplist.extend(inputdata["chart"]["result"][0]["timestamp"])

  calendertime = []

  for ts in timestamplist:
    dt = datetime.fromtimestamp(ts)
    calendertime.append(dt.strftime("%m/%d/%Y"))

  return calendertime

def parseValues(inputdata):

  valueList = []
  valueList.extend(inputdata["chart"]["result"][0]["indicators"]["quote"][0]["open"])
  valueList.extend(inputdata["chart"]["result"][0]["indicators"]["quote"][0]["close"])

  return valueList


def attachEvents(inputdata):

  eventlist = []

  for i in range(0,len(inputdata["chart"]["result"][0]["timestamp"])):
    eventlist.append("open")	

  for i in range(0,len(inputdata["chart"]["result"][0]["timestamp"])):
    eventlist.append("close")

  return eventlist


if __name__ == "__main__":
 
  if os.environ.get('RAPIDAPI_KEY') and os.environ.get('RAPIDAPI_KEY'):
      print('Environment variables set, good to proceed')
  else:
      print('Environment variable not set for API key and host. Script terminates here')
      import sys
      sys.exit()

  try:

    while len(symbol_string) <= 2:
      symbol_string = raw_input("Enter the stock symbol: ")

    retdata = fetchStockData(symbol_string)

    

    if (None != inputdata): 

      inputdata["Timestamp"] = parseTimestamp(retdata)

      inputdata["Values"] = parseValues(retdata)

      inputdata["Events"] = attachEvents(retdata)

      df = pd.DataFrame(inputdata)
      print(df)

      sns.set(style="darkgrid")

      rcParams['figure.figsize'] = 13,5
      rcParams['figure.subplot.bottom'] = 0.2

      
      ax = sns.lineplot(x="Timestamp", y="Values", hue="Events",dashes=False, markers=True, 
                   data=df, sort=False)


      ax.set_title('Symbol: ' + symbol_string)
      
      plt.xticks(
          rotation=45, 
          horizontalalignment='right',
          fontweight='light',
          fontsize='xx-small'  
      )

      plt.show()

  except Exception as e:
    print('{} {}'.format('Error',e)) 	
