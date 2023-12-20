

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

def getPath(src_dpid:str, dst_dpid:str, path_num:str):
    url="http://127.0.0.1:8080/wm/routing/paths/{src_dpid}/{dst_dpid}/{path_num}/json"
    response=requests.get(url)
    response_json=response.json()
    return response_json["results"]

if __name__ == "__main__":
    deleteAllFlows()
    switches={}
    cihazlar={}
    links={}
    paths={}

    edges=[]
    # switches=getAllSwitchs()
    # print(json.dumps(switches,indent=4))
    
    # cihazlar=getHosts()
    # print(json.dumps(cihazlar,indent=4))

    #links
    links=getAllLinks()
    print(json.dumps(links,indent=4))


    # paths=getPath("00:00:00:00:00:00:00:10","00:00:00:00:00:00:00:02","3")
    # print(json.dumps(links,indent=4))

    # switchler arası en uygun yol için kenarlar oluşturuluyor

    # for link in links:
    #     edges.append((str(link["src-switch"]),str(link["dst-switch"]),link["latency"]))
    #     edges.append((str(link["dst-switch"]),str(link["src-switch"]),link["latency"]))
    # print("En kısa yol")
    # for i in range(14):
    #     if i+1<10:
    #         ek1="0"+str(i+1)
    #     else:
    #         ek1=str(i+1)
    #     for j in range(14):
    #         if j+1<10:
    #             ek2="0"+str(j+1)
    #         else:
    #             ek2=str(j+1)
    #         print(ek1+" -> "+ek2) 
    #         print(shortestPath.shortestPath(edges,"00:00:00:00:00:00:00:"+ek1,"00:00:00:00:00:00:00:"+ek2))
            # print(shortestPath.shortestPath(edges,"00:00:00:00:00:00:00:10","00:00:00:00:00:00:00:02"))

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
    # edges2 = [
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
    # print(json.dumps(edges2,indent=4))
    

    # edges3=[
    #     ("00:00:00:00:00:00:00:03", "00:00:00:00:00:00:00:06", 8),
    #     ("00:00:00:00:00:00:00:11","00:00:00:00:00:00:00:14",8),
    #     ("00:00:00:00:00:00:00:10","00:00:00:00:00:00:00:13",9),
    #     ("00:00:00:00:00:00:00:08","00:00:00:00:00:00:00:11",13),
    #     ("00:00:00:00:00:00:00:01","00:00:00:00:00:00:00:03",10),
    #     ("00:00:00:00:00:00:00:09","00:00:00:00:00:00:00:12",10),
    #     ("00:00:00:00:00:00:00:05","00:00:00:00:00:00:00:06",10),
    #     ("00:00:00:00:00:00:00:09","00:00:00:00:00:00:00:10",12),
    #     ("00:00:00:00:00:00:00:01","00:00:00:00:00:00:00:02",8),
    #     ("00:00:00:00:00:00:00:02","00:00:00:00:00:00:00:08",9),
    #     ("00:00:00:00:00:00:00:06","00:00:00:00:00:00:00:14",9),
    #     ("00:00:00:00:00:00:00:06","00:00:00:00:00:00:00:13",10),
    #     ("00:00:00:00:00:00:00:04","00:00:00:00:00:00:00:09",9),
    #     ("00:00:00:00:00:00:00:07","00:00:00:00:00:00:00:08",13),
    #     ("00:00:00:00:00:00:00:10","00:00:00:00:00:00:00:11",10),
    #     ("00:00:00:00:00:00:00:01","00:00:00:00:00:00:00:04",9),
    #     ("00:00:00:00:00:00:00:11","00:00:00:00:00:00:00:12",9),
    #     ("00:00:00:00:00:00:00:02","00:00:00:00:00:00:00:03",10),
    #     ("00:00:00:00:00:00:00:04","00:00:00:00:00:00:00:05",12),
    #     ("00:00:00:00:00:00:00:12","00:00:00:00:00:00:00:13",10),
    #     ("00:00:00:00:00:00:00:05","00:00:00:00:00:00:00:07",10)
    # ]
    # print("En kısa yol 2")
    # print(shortestPath.shortestPath(edges3,"00:00:00:00:00:00:00:05","00:00:00:00:00:00:00:08"))