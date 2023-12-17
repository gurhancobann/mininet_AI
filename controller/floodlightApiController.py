import requests
import json
import time
import shortestPath

def getDevices():
    url="http://127.0.0.1:8080/wm/device/"
    response=requests.get(url)
    response_json=response.json()
    #print("[INFO]*****Cihazlar*******\n",response_json["devices"])
    return response_json["devices"]

def getAllSwitchs():
    url="http://127.0.0.1:8080/wm/core/controller/switches/json"
    return requests.get(url).json()

def deleteAllFlows():
    url="http://127.0.0.1:8080/wm/staticentrypusher/clear/all/json"
    response=requests.get(url)
    response_json=response.json()
    print("[INFO]*****Silme Sonucu*****\n",response_json)
    return response_json


if __name__ == "__main__":
    deleteAllFlows()
    #tekrar=10
    # while tekrar>0:
    #     time.sleep(10)
    #     print(tekrar)
    #     tekrar=tekrar-1
    
    #switch ağırlıklarını bulduktan sonra alttaki şekliyle yapıp gönder en kısa yolu bulmakta.
    # edges = [
    #     ("A", "B", 7),
    #     ("A", "D", 5),
    #     ("B", "C", 8),
    #     ("B", "D", 9),
    #     ("B", "E", 7),
    #     ("C", "E", 5),
    #     ("D", "E", 15),
    #     ("D", "F", 6),
    #     ("E", "F", 8),
    #     ("E", "G", 9),
    #     ("F", "G", 11)
    # ]

    # print(shortestPath.shortestPath(edges,"A","E"))