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
    #*********** cihaz ismi eklemek için
    # i=1
    # for host in response_json["devices"]:
    #     if(len(host["ipv4"])>0):
    #        ip=str(host["ipv4"])
    #        ip=ip.replace("['","")
    #        ip=ip.replace("']","")
    #        ipSegments=(ip.split("."))
    #        mac=str(host["mac"])
    #        mac=mac.replace("['","")
    #        mac=mac.replace("']","")
    #        cihazlar[i]=["h"+ipSegments[3],ip,mac,host["attachmentPoint"][0]["switch"],host["attachmentPoint"][0]["port"]]
    #        i=i+1
    #return cihazlar
    i=1
    for host in response_json["devices"]:
        if(len(host["attachmentPoint"])>0):
            cihazlar[i]=[host["attachmentPoint"][0]["switch"],host["attachmentPoint"][0]["port"]]
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
    url="http://127.0.0.1:8080/wm/routing/paths/"+src_dpid+"/"+dst_dpid+"/"+path_num+"/json"
    response=requests.get(url)
    response_json=response.json()
    return response_json["results"]

def getPort(switch:str):
    url="http://127.0.0.1:8080/wm/core/switch/"+switch+"/port/json"
    response=requests.get(url)
    response_json=response.json()
    return response_json["port_reply"]

def flowPusher(flow:dict):
    url="http://127.0.0.1:8080/wm/staticentrypusher/json"
    post_response=requests.post(url,json=flow)
    post_response_json=post_response.json()
    print(post_response_json)

def clearAllFlow():
    url="http://127.0.0.1:8080/wm/staticentrypusher/clear/all/json"
    post_response=requests.post(url)
    post_response_json=post_response.json()
    print(post_response_json)

def clearFlow(switch):
    url="http://127.0.0.1:8080/wm/staticentrypusher/clear/{switch}/json"
    post_response=requests.post(url)
    post_response_json=post_response.json()
    print(post_response_json)

def enableStatistics():
    url="http://127.0.0.1:8080/wm/statistics/config/enable/json"
    data=''
    response=requests.post(url,data=data)
    post_response_json=response.json()
    print(post_response_json)

def getSwitchStatsByPort(switch:str, port):
    port=str(port)
    url=f"http://127.0.0.1:8080/wm/statistics/bandwidth/{switch}/{port}/json"
    response=requests.get(url)
    response_json=response.json()
    print(json.dumps(response_json,indent=4))

if __name__ == "__main__":
    #deleteAllFlows()
    enableStatistics()
    getSwitchStatsByPort("00:00:00:00:00:00:00:01",4)
    switches={}
    cihazlar={}
    links={}
    paths={}

    edges=[]
    yollar=[]
    portlar=[]
# #akış düzenleme
#     flow_s13_s6={
#         "switch":"00:00:00:00:00:00:00:13",
#         "name":"flow_s13_s6",
#         "cookie":"0",
#         "priority":"32768",
#         "eth_type":"0x0800",
#         "in_port" : "4",
#         "active":"true",
#         "actions":"output=2"
#     }
#     #clearFlow("00:00:00:00:00:00:00:13")
#     #flowPusher(flow_s13_s6)

#     #*************Kurulum Algoritması Deneme****************
#     #1. adım ve 2. adım
#     cihazlar=getHosts()
#     #print(json.dumps(cihazlar,indent=4))
 
#     #3. adım
#     links=getAllLinks()
#     #print(json.dumps(links,indent=4))
#     for link in links:
#         edges.append((str(link["src-switch"]),str(link["dst-switch"]),link["latency"]))
#         edges.append((str(link["dst-switch"]),str(link["src-switch"]),link["latency"]))
#     #print(json.dumps(edges,indent=4))
#     #4. Adım
#     sira=0
    
#     for i in range(len(cihazlar)):
#         for j in range(len(cihazlar)-1):
#             yollar.append(shortestPath.shortestPath(edges,cihazlar[i+1][0],cihazlar[j+2][0]))
    
#     print("Cihaz Sayısı : "+str(len(cihazlar)))
#     print("yol sayısı: "+str(len(yollar)))
#     print(yollar[0])
#     print(json.dumps(cihazlar,indent=4))
#     for i in range(len(cihazlar)):
#         ports=getPort(cihazlar[i+1][0])
#         for j in range(len(ports[0]["port"])):
#             if(cihazlar[i+1][1]!=ports[0]["port"][j]["port_number"])and ports[0]["port"][j]["port_number"]!="local":
#                 print("cihaz portu: "+cihazlar[i+1][1]+" switch portu: "+ports[0]["port"][j]["port_number"])
#                 flow1={
#                     "switch":cihazlar[i+1][0],
#                     "name":cihazlar[i+1][0]+"_"+cihazlar[i+1][1]+"_"+ports[0]["port"][j]["port_number"],
#                     "cookie":"0",
#                     "priority":"32768",
#                     "eth_type":"0x0800",
#                     "in_port" : cihazlar[i+1][1],
#                     "active":"true",
#                     "actions":"output="+ports[0]["port"][j]["port_number"]
#                 }
#                 flow2={
#                     "switch":cihazlar[i+1][0],
#                     "name":cihazlar[i+1][0]+"_"+ports[0]["port"][j]["port_number"]+"_"+cihazlar[i+1][1],
#                     "cookie":"0",
#                     "priority":"32768",
#                     "eth_type":"0x0800",
#                     "in_port" : ports[0]["port"][j]["port_number"],
#                     "active":"true",
#                     "actions":"output="+cihazlar[i+1][1]
#                 }
#                 #flowPusher(flow1)
#                 #flowPusher(flow2)
#         #print(json.dumps(ports[0]["port"][1]["port_number"],indent=4))
#     for i in range(len(yollar)):
#         if(yollar[i][0]>0):
#             #print(str(i)+"- latency: "+str(yollar[i][0])+" Kaynak: "+yollar[i][1][0]+" Hedef: "+yollar[i][1][1])
#             for port in getPath(yollar[i][1][0],yollar[i][1][1],"2"):
#                 portlar.append((port["path"][0]["port"], port["path"][1]["port"]))
    
    #print(portlar)

    #Tüm linkler arasındaki en kısa yollar hesaplanıyor mu? testi
    # print("En kısa yol")
    # for i in range(len(cihazlar)):
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
 
 
    # switches=getAllSwitchs()
    # print(json.dumps(switches,indent=4))
    
    # cihazlar=getHosts()
    # print(json.dumps(cihazlar,indent=4))

    #links
    # links=getAllLinks()
    # print(json.dumps(links,indent=4))

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