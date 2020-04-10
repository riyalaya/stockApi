import yahooApi as ya

    #while len(symbol_string) <= 2:
          
    #symbol_string = raw_input("Enter the stock symbol: ")
with open('stock.txt','r') as f:
    retdata = f.read()
    print retdata
    inputdata = []
    if (None != inputdata): 
            inputdata["Timestamp"] = ya.parseTimestamp(retdata)
            inputdata["Values"] = ya.parseValues(retdata)
            inputdata["Events"] = ya.attachEvents(retdata)
            df = pd.DataFrame(inputdata)
