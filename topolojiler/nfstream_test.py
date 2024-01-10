from nfstream import NFStreamer
import sys
import threading
from threading import Thread


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
            if((flow.src_ip==self._ip) or (flow.dst_ip==self._ip)) and (flow.application_name=="Unknown" and flow.application_category_name=="Unspecified"):
                totalPaket=totalPaket+flow.bidirectional_packets
                zaman=zaman+flow.bidirectional_duration_ms
        self.result=[totalPaket,zaman]

if __name__=='__main__':
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
    