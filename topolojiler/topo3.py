#!usr/bin/python

import sys
import pingparsing
sys.path.append("../controller")
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch, Host, CPULimitedHost
from mininet.topo import Topo
from mininet.link import TCLink
from time import sleep, perf_counter

import json
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor
import threading
from threading import Thread
import floodlightRestApi
import subprocess
import pandas as pd
from nfstream import NFStreamer

class NsfnetTopo(Topo):
	"""
	Topology link:
	"""
	def build(self, **params):
	
		h1=self.addHost('h1', ip='10.0.0.1')
		h2=self.addHost('h2', ip='10.0.0.2')
		h3=self.addHost('h3', ip='10.0.0.3')
		h4=self.addHost('h4', ip='10.0.0.4')
		h5=self.addHost('h5', ip='10.0.0.5')
		h6=self.addHost('h6', ip='10.0.0.6')
		h7=self.addHost('h7', ip='10.0.0.7')
		h8=self.addHost('h8', ip='10.0.0.8')
		h9=self.addHost('h9', ip='10.0.0.9')
		h10=self.addHost('h10', ip='10.0.0.10')
		h11=self.addHost('h11', ip='10.0.0.11')
		h12=self.addHost('h12', ip='10.0.0.12')
		h13=self.addHost('h13', ip='10.0.0.13')
		h14=self.addHost('h14', ip='10.0.0.14')
	
		s1=self.addSwitch('s1',dpid='00:00:00:00:00:00:00:01',protocols="OpenFlow13")
		s2=self.addSwitch('s2',dpid='00:00:00:00:00:00:00:02',protocols="OpenFlow13")
		s3=self.addSwitch('s3',dpid='00:00:00:00:00:00:00:03',protocols="OpenFlow13")
		s4=self.addSwitch('s4',dpid='00:00:00:00:00:00:00:04',protocols="OpenFlow13")
		s5=self.addSwitch('s5',dpid='00:00:00:00:00:00:00:05',protocols="OpenFlow13")
		s6=self.addSwitch('s6',dpid='00:00:00:00:00:00:00:06',protocols="OpenFlow13")
		s7=self.addSwitch('s7',dpid='00:00:00:00:00:00:00:07',protocols="OpenFlow13")
		s8=self.addSwitch('s8',dpid='00:00:00:00:00:00:00:08',protocols="OpenFlow13")
		s9=self.addSwitch('s9',dpid='00:00:00:00:00:00:00:09',protocols="OpenFlow13")
		s10=self.addSwitch('s10',dpid='00:00:00:00:00:00:00:10',protocols="OpenFlow13")
		s15=self.addSwitch('s15',dpid='00:00:00:00:00:00:00:15',protocols="OpenFlow13")
		s11=self.addSwitch('s11',dpid='00:00:00:00:00:00:00:11',protocols="OpenFlow13")
		s12=self.addSwitch('s12',dpid='00:00:00:00:00:00:00:12',protocols="OpenFlow13")
		s13=self.addSwitch('s13',dpid='00:00:00:00:00:00:00:13',protocols="OpenFlow13")
		s14=self.addSwitch('s14',dpid='00:00:00:00:00:00:00:14',protocols="OpenFlow13")
		
		linkOptns1=dict(delay='25ms',bw=10, loss=0, max_queue_size=1000, use_htb=True)
		linkOptns2=dict(delay='25ms',bw=10, loss=0, max_queue_size=1000, use_htb=True)
	
		self.addLink(s1, s2, **linkOptns2)
		self.addLink(s1, s3, **linkOptns2)
		self.addLink(s1, s4, **linkOptns2)
		self.addLink(s2, s8, **linkOptns2)
		self.addLink(s2, s3, **linkOptns2)
		self.addLink(s3, s6, **linkOptns2)
		self.addLink(s4, s5, **linkOptns2)
		self.addLink(s4, s9, **linkOptns2)
		self.addLink(s5, s6, **linkOptns2)
		self.addLink(s5, s7, **linkOptns2)
		self.addLink(s6, s13, **linkOptns2)
		self.addLink(s6, s14, **linkOptns2)
		self.addLink(s7, s8, **linkOptns2)
		self.addLink(s8, s11, **linkOptns2)
		self.addLink(s9, s10, **linkOptns2)
		self.addLink(s9, s12, **linkOptns2)
		self.addLink(s10, s11, **linkOptns2)
		self.addLink(s10, s13, **linkOptns2)
		self.addLink(s10,s15, **linkOptns2)
		self.addLink(s11, s12, **linkOptns2)
		self.addLink(s11, s14, **linkOptns2)
		self.addLink(s12, s13, **linkOptns2)
	
		self.addLink(s1, h1, **linkOptns1)
		self.addLink(s2, h2, **linkOptns1)
		self.addLink(s3, h3, **linkOptns1)
		self.addLink(s4, h4, **linkOptns1)
		self.addLink(s5, h5, **linkOptns1)
		self.addLink(s6, h6, **linkOptns1)
		self.addLink(s7, h7, **linkOptns1)
		self.addLink(s8, h8, **linkOptns1)
		self.addLink(s9, h9, **linkOptns1)
		self.addLink(s15, h10, **linkOptns1)
		self.addLink(s11, h11, **linkOptns1)
		self.addLink(s12, h12, **linkOptns1)
		self.addLink(s13, h13, **linkOptns1)
		self.addLink(s14, h14, **linkOptns1)
def startNetwork():
	global net
	global activeThreadList
	global serverList
	serverList={"h1":"h14",
			 "h2":"h14",
			 "h3":"h14",
			 "h4":"h14",
			 "h5":"h10",}
	activeThreadList=[]
	net=None
	dataFrame=pd.read_csv('data.csv')
	dataRow={}
	cleanMininet()

	net=Mininet(topo=NsfnetTopo(),link=TCLink, build=False, switch=OVSKernelSwitch, autoSetMacs=True, waitConnected=True)
	remote_ip="127.0.0.1"
	
	net.addController('c1', controller=RemoteController,ip=remote_ip,port=6653,protocols="OpenFlow13")
	
	info(f'[INFO]********Topoloji Oluşturuluyor********\n')
	net.build()
	info(f'[INFO]*************Ağ Başlatıldı************\n')
	net.start()
	info(f'[INFO]*************2sn Bekleniyor************\n')
	sleep(2)
	floodlightRestApi.deleteAllFlows()
	info(f'[INFO]**********Tüm Akışlar Silindi**********\n')

	#net.pingAll()
	
	

	# wireThread=HostCommand(net.getNodeByName("s4"),"wireshark")
	# wireThread.daemon=True
	# wireThread.start()
	#serverName="h10"
	info(f'[INFO]*********Test Yayını Başlatıldı********\n')
	test(["h1","h2","h3","h4","h5"],serverList)
	print(json.dumps(serverList,indent=4))
	info(f'[INFO]********Aktif thread sayısı : {threading.active_count()}*******\n')
	info(f'[INFO]********Testin Bitmesi Bekleniyor*******\n')
	sleep(16)
	killFfmegPorts("h10")
	killFfmegPorts("h14")
	info(f'[INFO]********Test Bitti - Aktif thread sayısı : {threading.active_count()}*******\n')
	info(f'[INFO]********ASıl İşlem *******\n')
	LoadBalacing(["h1","h2","h3","h4","h5","h6"],serverList)
	sleep(10)
	# activeThreadList=threading.enumerate()
	# activeThreadList.pop(0)
	killFfmegPorts("h10")
	killFfmegPorts("h14")
	print(activeThreadList)
	#activeThreadList[len(activeThreadList)-1].join()
	info(f'[INFO]********Video bitti*******\n')
	info(f'[INFO]********PSNR & SSIM Değerleri Hesaplanıyor*******\n')
	for host in ["h1","h2","h3","h4","h5","h6"]:
		psnr, ssim_first, ssim_second=calcPsnrSsim(host)
		dataRow={"host":host,"psnr":psnr,"ssim_first":ssim_first,"ssim_second":ssim_second,"type":3,"server":serverList[host]}
		dataFrame=dataFrame.append(dataRow,ignore_index=True)
	
	dataFrame.to_csv("data.csv",sep=",",index=False,encoding="utf-8")
	
	try:
		deletefile()
	except Exception as e:
		print(f"Excaption {e}")
	
	cleanMininet()
	
	info(f'[INFO]********Aktif thread sayısı : {threading.active_count()}*******\n')
	# wireThread.join()

def test(receivers,serverList):
	port="1234"
	videoSource="test.ts"
	num_paths=3
	path_index=0
	senderCommand1=f"ffmpeg -re -i {videoSource}"
	senderCommand2=f"ffmpeg -re -i {videoSource}"
	for receiver in receivers:
		receiverNode=net.getNodeByName(receiver)
		dst_host_mac=receiverNode.MAC()
		dst_host_ipv4=receiverNode.IP()
		senderNode=net.getNodeByName(serverList[receiver])

		print(f"host : {receiver} - sender : {serverList[receiver]}")
		if(serverList[receiver]=="h10"):
			print(f"server : h10")
			src_host_mac=senderNode.MAC()
			src_host_ipv4=senderNode.IP()
			senderCommand1=senderCommand1+f" -c copy -f mpegts udp://{dst_host_ipv4}:{port}"
		if(serverList[receiver]=="h14"):
			print(f"server :h14")
			src_host_mac=senderNode.MAC()
			src_host_ipv4=senderNode.IP()
			senderCommand2=senderCommand2+f" -c copy -f mpegts udp://{dst_host_ipv4}:{port}"
		
		floodlightRestApi.pathPusher(src_host_mac, src_host_ipv4, dst_host_mac,dst_host_ipv4,num_paths,path_index)
		receiverURL=f"udp://{dst_host_ipv4}:{port}"
		receiverCommand=f"ffmpeg -i {receiverURL}"
		receiverThread=(HostCommand(receiverNode, receiverCommand))
		receiverThread.daemon=True
		receiverThread.start()
		sleep(2)
	senderNode1=net.getNodeByName("h10")
	senderNode2=net.getNodeByName("h14")
	
	senderThread1=(HostCommand(senderNode1, senderCommand1))
	senderThread1.daemon=True
	senderThread1.start()
	senderThread2=(HostCommand(senderNode2, senderCommand2))
	senderThread2.daemon=True
	senderThread2.start()
	print("2 sn bekleniyor")
	sleep(2)
	testH6()
	senderThread2.join()
	

def LoadBalacing(receivers,serverList):
	port="1234"
	videoSource="output.ts"
	senderNode1, senderNode2=net.getNodeByName("h10"), net.getNodeByName("h14")
	senderCommand1=f"ffmpeg -re -i {videoSource}"
	senderCommand2=f"ffmpeg -re -i {videoSource}"
	for receiver in receivers:
		receiverNode=net.getNodeByName(receiver)
		dst_host_ipv4=receiverNode.IP()
		if(serverList[receiver]=="h10"):
			senderCommand1=senderCommand1+f" -c copy -f mpegts udp://{dst_host_ipv4}:{port}"
		if(serverList[receiver]=="h14"):
			senderCommand2=senderCommand2+f" -c copy -f mpegts udp://{dst_host_ipv4}:{port}"
		receiverURL=f"udp://{dst_host_ipv4}:{port}"
		receiverNode.cmd(f"mkdir records/{receiver}")
		receiverCommand=f"ffmpeg -i {receiverURL} -c copy records/{receiver}/input.ts"
		receiverThread=(HostCommand(receiverNode, receiverCommand))
		receiverThread.daemon=True
		receiverThread.start()
	
	senderThread1=(HostCommand(senderNode1, senderCommand1))
	senderThread1.daemon=True
	senderThread1.start()
	senderThread2=(HostCommand(senderNode2, senderCommand2))
	senderThread2.daemon=True
	senderThread2.start()
	info(f'[INFO]********Video gönderim başladı*******\n')
	senderThread2.join()
	info(f'[INFO]********Video gönderim bitti*******\n')


def testH6():
	print("testH6 Başladı")
	streamThread1=(streamer("s15-eth2","10.0.0.10"))
	streamThread1.daemon=True
	streamThread1.start()
	streamThread2= streamer("s14-eth3","10.0.0.14")
	streamThread2.daemon=True
	streamThread2.start()
	streamThread2.join()
	streamThread1.join()
	print(f"toplam paket 1: {streamThread1.result[0]}, zaman 1: {streamThread1.result[1]}")
	print(f"toplam paket 2: {streamThread2.result[0]}, zaman 2: {streamThread2.result[1]}")
	if(streamThread1.result[1]==0 or streamThread2.result[1]==0):
		testH6()
	else:
		yuk1=streamThread1.result[0]/streamThread1.result[1]
		yuk2=streamThread2.result[0]/streamThread2.result[1]
	if (yuk1 < yuk2):
		serverList["h6"]="h10"
	else:
		serverList["h6"]="h14"

def killFfmegPorts(senderNode):
	node=net.getNodeByName(senderNode)
	commandCheckPort="pgrep -x ffmpeg"
	commandKillPort="pkill -x ffmpeg"
	result=node.cmd(commandCheckPort)
	while(result !=""):
		node.cmd(commandKillPort)
		print("port Killed: ",result)
		result=node.cmd(commandCheckPort)

def calcPsnrSsim(receiver):
	host=net.getNodeByName(receiver)
	print(f"***********{host} için PSNR ve SSİM değerleri hesaplanıyor******")
	videoSource="output.ts"
	outputSource=f"records/{host}/input.ts"
	command=f"ffmpeg -i {videoSource} -i {outputSource} -lavfi '[0:v][1:v]psnr' -f null -"
	hostThread=HostCommand(host, command)
	hostThread.daemon=True
	hostThread.start()
	hostThread.join()
	psnrResault=hostThread.result
	psnrResault=float(psnrResault.split("\n")[-2].split("average:")[1].split(" ")[0].strip())
	command=f"ffmpeg -i {videoSource} -i {outputSource} -lavfi '[0:v][1:v]ssim' -f null -"
	hostThread=HostCommand(host, command)
	hostThread.daemon=True
	hostThread.start()
	hostThread.join()
	ssimResault=hostThread.result.split("\n")[-2]
	first=float(ssimResault.split("All:")[1].split(" ")[0])
	second=float(ssimResault.split("All:")[1].split(" ")[1].replace("(","").replace(")",""))
	print(f"***********PSNR:{psnrResault}, SSIM F:{first}, SSIM S:{second}******")
	print("")
	return psnrResault, first, second

def cleanMininet():
	script_path="cleanMininet.sh"
	subprocess.run(['bash',script_path])

def deletefile():
	script_path="deleteFile.sh"
	subprocess.run(['bash',script_path])

class HostCommand(Thread):
	def __init__(self, host:Host, command:str):
		Thread.__init__(self)
		self._host=host
		self._command=command
		self.result=None
	def run(self):
		self.result=self._host.cmd(self._command)

class streamer(Thread):
    def __init__(self, sources:str,ip:str):
          Thread.__init__(self)
          self._sources=sources
          self._ip=ip
          self.result=None
    def run(self):
        flow_streamer=NFStreamer(source=self._sources,
                                statistical_analysis=True,
                                idle_timeout=10, active_timeout=5, max_nflows=5
                                #active_timeout 5 saniyelik süreyi ölçüyor
                                )
        totalPaket=0
        zaman=0
        
        for flow in flow_streamer:
            if((flow.src_ip==self._ip) or (flow.dst_ip==self._ip)): #and (flow.application_name=="Unknown" and flow.application_category_name=="Unspecified"):
                totalPaket=totalPaket+flow.bidirectional_packets
                zaman=zaman+flow.bidirectional_duration_ms
        self.result=[totalPaket,zaman]
    


if __name__ == '__main__':
	setLogLevel('info')
	startNetwork()

		
