from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.topo import Topo
from mininet.link import TCLink
from time import sleep


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
		
		linkOptns1=dict(delay='5ms',bw=10, loss=0, max_queue_size=1000, use_htb=True)
		linkOptns2=dict(delay='5ms',bw=1000, loss=0, max_queue_size=1000, use_htb=True)
	
		self.addLink(s1,s2,**linkOptns2)
		self.addLink(s1,s3,**linkOptns2)
		self.addLink(s1,s4,**linkOptns2)
		self.addLink(s2,s8,**linkOptns2)
		self.addLink(s2,s3,**linkOptns2)
		self.addLink(s3,s6,**linkOptns2)
		self.addLink(s4,s5,**linkOptns2)
		self.addLink(s4,s9,**linkOptns2)
		self.addLink(s5,s6,**linkOptns2)
		self.addLink(s5,s7,**linkOptns2)
		self.addLink(s6,s13,**linkOptns2)
		self.addLink(s6,s14,**linkOptns2)
		self.addLink(s7,s8,**linkOptns2)
		self.addLink(s8,s11,**linkOptns2)
		self.addLink(s9,s10,**linkOptns2)
		self.addLink(s9,s12,**linkOptns2)
		self.addLink(s10,s11,**linkOptns2)
		self.addLink(s10,s13,**linkOptns2)
		self.addLink(s10,s15,**linkOptns2)
		self.addLink(s11,s12,**linkOptns2)
		self.addLink(s11,s14,**linkOptns2)
		self.addLink(s12,s13,**linkOptns2)
	
		self.addLink(s1,h1,cls=TCLink, **linkOptns1)
		self.addLink(s2,h2,**linkOptns1)
		self.addLink(s3,h3,**linkOptns1)
		self.addLink(s4,h4,**linkOptns1)
		self.addLink(s5,h5,**linkOptns1)
		self.addLink(s6,h6,**linkOptns1)
		self.addLink(s7,h7,**linkOptns1)
		self.addLink(s8,h8,**linkOptns1)
		self.addLink(s9,h9,**linkOptns1)
		self.addLink(s15,h10,**linkOptns1)
		self.addLink(s11,h11,**linkOptns1)
		self.addLink(s12,h12,**linkOptns1)
		self.addLink(s13,h13,**linkOptns1)
		self.addLink(s14,h14,**linkOptns1)
def startNetwork():
	global net
	net=Mininet(topo=NsfnetTopo(),link=TCLink, build=False, switch=OVSKernelSwitch, autoSetMacs=True, waitConnected=True)
	remote_ip="127.0.0.1"
	
	net.addController('c1', controller=RemoteController,ip=remote_ip,port=6653,protocols="OpenFlow13")
	
	net.build()
	net.start()
	print("100ms bağlantıların oluşması için bekleniyor")
	sleep(2)
	net.pingAll()
	CLI(net)
	net.stop()

net =Mininet()
if __name__ == '__main__':
	setLogLevel('info')
	startNetwork()

# #def getHosts():
# 	#global net
# 	print(net.host)
# 	return net.hosts
		
