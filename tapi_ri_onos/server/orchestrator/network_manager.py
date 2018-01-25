import logging
import database.database as database
import requests
from requests.auth import HTTPBasicAuth
import json
import collections

class network_manager():
    def __init__(self):
        logging.debug("Init topo_manager")
        self.ctl_address = '127.0.0.1'
        self.ctl_port = '8181'
        self.ctl_user = 'onos'
        self.ctl_password = 'rocks'         
        
    def load_topology(self):

        topo=self.load_onos_topology( self.ctl_address, self.ctl_port, self.ctl_user, self.ctl_password)
        if topo != None:
          logging.info('Loaded topo:\n%s', topo)
          database.context['topology'].append(topo)

    def load_onos_topology(self, ctl_address, ctl_port, ctl_user, ctl_password):
        logging.info("load_onos_topology %s %s %s %s", ctl_address, ctl_port, ctl_user, ctl_password)

        node_array = []
        link_array = []

        #nodes
        http_json = 'http://' + ctl_address + ':' + ctl_port + '/onos/v1/devices'
        response = requests.get(http_json, auth=HTTPBasicAuth(ctl_user, ctl_password))
        onos_nodes = response.json()

        logging.info("Retrieved onos nodes:\n%s", json.dumps(onos_nodes, indent=4, sort_keys=True) )
        
        for node in onos_nodes["devices"]:
        
            node_edge_point = []
            http_json = 'http://' + ctl_address + ':' + ctl_port + '/onos/v1/devices/' + node['id'] + '/ports'
            response = requests.get(http_json, auth=HTTPBasicAuth(ctl_user, ctl_password))
            node_ports = response.json()
            logging.info("Retrieved node %s node_ports:\n%s", node['id'], json.dumps(node_ports, indent=4, sort_keys=True) )
            
            for port in node_ports["ports"]:
                if port["isEnabled"] == True :
                    
                    nep = collections.OrderedDict()
                    nep['uuid'] = "nep" + self.getNodeId(node['id']) + port["port"] 
                    node_edge_point.append( nep )
            
            node_json = collections.OrderedDict()
            node_json['uuid'] = "node" + self.getNodeId(node['id'])            
            node_json['owned-node-edge-point'] = node_edge_point
            
            node_array.append( node_json )
            
        #links
        http_json = 'http://' + ctl_address + ':' + ctl_port + '/onos/v1/links'
        response = requests.get(http_json, auth=HTTPBasicAuth(ctl_user, ctl_password))
        onos_links = response.json()
        logging.info("Retrieved onos links:\n%s", json.dumps(onos_links, indent=4, sort_keys=True) )

        for link in onos_links['links']:
            link_json = {}
            link_id= "link" + self.getNodeId(link['src']['device'])+ self.getNodeId(link['dst']['device'])
            link_json['uuid'] = link_id
            link_json['node-edge-point'] = []
            nep_src = "restconf/config/context/topology/top0/node/node" + self.getNodeId(link['src']['device']) + "/owned-node-edge-point/nep" + self.getNodeId(link['src']['device']) + link['src']['port'] + "/"
            nep_dst = "restconf/config/context/topology/top0/node/node" + self.getNodeId(link['dst']['device']) + "/owned-node-edge-point/nep" + self.getNodeId(link['dst']['device']) + link['dst']['port'] + "/"
            link_json['node-edge-point'].append(nep_src)
            link_json['node-edge-point'].append(nep_dst)    
            link_array.append( link_json )
        
        
        #topology    
        topo = collections.OrderedDict()  
        topo['uuid'] = "top0"
        topo['name'] = [{"value-name":"topo0","value":"0"}]
        topo['node'] = node_array     
        topo['link'] = link_array
        
        
        logging.debug("Topo: %s", topo)                  
        return topo


    def insertFlow( self, nodeId, priority, inport, outport ):

        flow='{ "priority": '+priority+', "timeout": 0, "isPermanent": true, "deviceId": "'+nodeId+'", "treatment": { "instructions": [ { "type": "OUTPUT", "port": "'+outport+'" } ] }, "selector": { "criteria": [ { "type": "IN_PORT", "port": "'+inport+'" } ] } }'

        url = 'http://' + self.ctl_address + ':' + self.ctl_port + '/onos/v1/flows/' + nodeId + '?appId=tuto' 
        headers = {'content-type': 'application/json'}
        response = requests.post(url, data=flow,
	                        headers=headers, auth=HTTPBasicAuth(self.ctl_user, self.ctl_password))
	                        
        return { 'status':response.status_code, 'content': response.content}

    def removeFlow(self, nodeId, flow_id):
        url = 'http://' + self.ctl_address + ':' + self.ctl_port + '/onos/v1/flows/application/tuto'
        response = requests.delete(url, auth=HTTPBasicAuth(self.ctl_user, self.ctl_password))
        return {'flow_id':flow_id, 'status':response.status_code, 'content': response.content}
    

    def getNodeId(self, ofdpi):
        nodeId=int(ofdpi.split('of:')[1])
        routerId=str(nodeId)
        return routerId
        



        