

import requests
import json
import time
import shortestPath

def getHosts():
    cihazlar={}
    url="http://127.0.0.1:8080/wm/device/"
    response=requests.get(url)
    response_json=response.json()
    #print("[INFO]*****Cihazlar*******\n",response_json["devices"])
    i=1
    for host in response_json["devices"]:
        if(len(host["ipv4"])>0):
           ip=str(host["ipv4"])
           ip=ip.replace("['","")
           ip=ip.replace("']","")
           ipSegments=(ip.split("."))
           mac=str(host["mac"])
           mac=mac.replace("['","")
           mac=mac.replace("']","")
           cihazlar[i]=["h"+ipSegments[3],ip,mac,host["attachmentPoint"][0]["switch"],host["attachmentPoint"][0]["port"]]
           i=i+1
    return cihazlar

def getAllSwitchs():
    url="http://127.0.0.1:8080/wm/core/controller/switches/json"
    switches={}
    for switch in requests.get(url).json():
        s=switch["switchDPID"].split(":")
        switches["s"+s[7]]=switch["switchDPID"]
    # print("********Switchler**********")
    # print(len(switches))
    # print(json.dumps(switches,indent=4))
    return switches

def deleteAllFlows():
    url="http://127.0.0.1:8080/wm/staticentrypusher/clear/all/json"
    response=requests.get(url)
    response_json=response.json()
    print("[INFO]*****Silme Sonucu*****\n",response_json)
    return response_json

def getAllLinks():
    url="http://127.0.0.1:8080/wm/topology/links/json"
    response=requests.get(url)
    response_json=response.json()
    return response_json

if __name__ == "__main__":
    deleteAllFlows()
    switches={}
    cihazlar={}
    links={}

    switches=getAllSwitchs()
    print(json.dumps(switches,indent=4))
    
    cihazlar=getHosts()
    print(json.dumps(cihazlar,indent=4))

    #links
    # links=getAllLinks()
    # print(json.dumps(links,indent=4))


    #cihazlar
    #cihazlar=getDevices()
    # cihaz=cihazlar[10]
    # ip=str(cihaz["ipv4"])
    # ip=ip.replace("['","")
    # ip=ip.replace("']","")
    # print(ip)
    # ip1=ip.split(".")
    # print(ip1[3])
    # for cihaz in cihazlar:
    #     if(len(cihaz["ipv4"])>0):
    #         ip=str(cihaz["ipv4"])
    #         ip=ip.split(".")
    #         print(ip[3])
    #         print(json.dumps(cihaz,indent=4))

    # for cihaz in cihazlar:
    #     if cihaz["ipv4"]==None:
    #         print(json.dumps(cihaz,indent=4))
    #print(json.dumps(getAllSwitchs(),indent=4))
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