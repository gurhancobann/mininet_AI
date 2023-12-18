#from flask import Flask, jsonify
import topo_nsfnet
import json

if __name__ =="__main__":
   hosts=topo_nsfnet.getHosts()
   print((hosts))