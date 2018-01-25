#!/usr/bin/python
# -*- coding: utf-8 -*-


import requests
from requests.auth import HTTPBasicAuth
import json
import matplotlib.pyplot as plt
import networkx as nx

IP='127.0.0.1'
PORT='8080'

def retrieveTopology(ip, port, user='', password=''):
    http_json = 'http://' + ip + ':' + port + '/restconf/config/context/topology/top0'
    response = requests.get(http_json, auth=HTTPBasicAuth(user, password))
    topology = response.json()
    return topology

def load_topology ( topology) :
    G=nx.Graph()
    for link in topology['link']:
      node_src = link['node-edge-point'][0].split('restconf/config/context/topology/top0/node/')[1].split('/')[0]
      node_dst = link['node-edge-point'][1].split('restconf/config/context/topology/top0/node/')[1].split('/')[0]
      G.add_edge( node_src, node_dst )
      print 'Link: ' + node_src + ' ' + node_dst
    nx.draw(G)
    plt.show()

if __name__ == "__main__":
    print "Reading network-topology"
    topo = retrieveTopology(IP, PORT)
    print json.dumps(topo, indent=4, sort_keys=True)
    load_topology(topo)
