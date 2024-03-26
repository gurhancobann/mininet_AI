import pandas as pd
import pickle

def yukHesapla(avgRTT,latency,hopCount,lowBandwidth,yukOrani):
    with open("./model/rfrModel.pkl",'rb') as file:
        model=pickle.load(file)
        x=pd.DataFrame({"avgRTT":[avgRTT],"latency":[latency],"hopCount":[hopCount],"bandwidth":[lowBandwidth],"yukOrani":[yukOrani]})
        y=model.predict(x)
    return y[0]

if __name__ == '__main__':
    tahmin=yukHesapla(277.266,62,3,1000000,10017.09523)
    print(tahmin)