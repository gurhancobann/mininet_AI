#!usr/bin/python

import sys
import pingparsing
sys.path.append("../controller")
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.net import Mininet
from mininet.node import RemoteController, OVSKernelSwitch, Host, CPULimitedHost, Node
from mininet.topo import Topo
from mininet.link import TCLink
from time import sleep, perf_counter
import datetime
import json
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor
import threading
from threading import Thread, Event
import floodlightRestApi
import subprocess
import pandas as pd
from nfstream import NFStreamer
import os

class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter,self).config(**params)
        self.cmd("sysctl net.ipv4.ip_forward=1")
    
    def terminate(self):
        self.cmd("sysctl net.ipv4.ip_forward=0")
        super(LinuxRouter,self).terminate()

class NetworkTopo(Topo):
    def build(self, **_opts):
        r1=self.addHost("r1",cls=LinuxRouter,ip="10.0.0.1/24")
        r2=self.addHost("r2",cls=LinuxRouter,ip="10.1.0.1/24")

        s1=self.addSwitch("s1")
        s2=self.addSwitch("s2")

        self.addLink(s1, r1,intfName2="r1-eth1", params2={"ip":"10.0.0.1/24"})
        self.addLink(s2, r2,intfName2="r2-eth1", params2={"ip":"10.1.0.1/24"})

        self.addLink(r1,r2,intfName1="r1-eth2",intfName2="r2-eth2",params1={"ip":"10.100.0.1/24"},params2={"ip":"10.100.0.2/24"})

        d1=self.addHost(name="d1",ip="10.0.0.251/24",defaultRoute="via 10.0.0.1")
        d2=self.addHost(name="d2",ip="10.1.0.252/24",defaultRoute="via 10.1.0.1")

        self.addLink(d1,s1)
        self.addLink(d2,s2)

def run():
    topo=NetworkTopo()
    net=Mininet(topo=topo,waitConnected=True,controller=RemoteController)
    

    info(net["r1"].cmd("ip route add 10.1.0.0/24 via 10.100.0.2 dev r1-eth2"))
    info(net["r2"].cmd("ip route add 10.0.0.0/24 via 10.100.0.1 dev r2-eth2"))

    #net.addController('c1', controller=RemoteController,ip="127.0.0.2",port=6653,protocols="OpenFlow13")
    net.start()
    CLI(net)
    net.stop()

if __name__ == "__main__":
    setLogLevel("info")
    run()