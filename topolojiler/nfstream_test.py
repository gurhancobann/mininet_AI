from nfstream import NFStreamer
import sys
if __name__=='__main__':
    flow_streamer=NFStreamer(source="s15-eth2",
                             statistical_analysis=True,
                             idle_timeout=15, active_timeout=5#active_timeout 5 saniyelik süreyi ölçüyor
                             )
    
    for flow in flow_streamer:
        if(flow.src_ip=="10.0.0.10") or (flow.dst_ip=="10.0.0.10"):
            print(flow)