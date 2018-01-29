import logging
import database.database as database
import orchestrator.network_manager as network_manager


class Orchestrator:
    def __init__(self, onos):
        self.onos=onos
        self.network_manager=network_manager.network_manager()

    def create_connectivity_service(self, uuid, connectivity_service):
      logging.info("create_connectivity_service %s %s", uuid, connectivity_service)

      connection = {
        "uuid" : uuid,
        "connection-end-point" : [] #We only include a reference to nep - This should be extended as a nep can contain several cep
      }
      
      src = connectivity_service['end-point'][0]['service-interface-point']
      dst = connectivity_service['end-point'][-1]['service-interface-point']
      
      #we assume sip encodes node and port info - and connectivity service is of a direct link between ports
      src_node=src.split("sip")[1].split("/")[0][1]
      src_port=src.split("sip")[1].split("/")[0][0]
      connection['connection-end-point'].append( "/restconf/config/topology/top0/node/node"+src_node + "/owned-node-edge-point/nep"+ src_node + src_port + "/" )
      dst_node=dst.split("sip")[1].split("/")[0][1]
      dst_port=dst.split("sip")[1].split("/")[0][0]
      connection['connection-end-point'].append( "/restconf/config/topology/top0/node/node"+dst_node + "/owned-node-edge-point/nep"+ dst_node + dst_port + "/" )
      logging.info("create_connectivity_service %s %s", src, dst)
      self.network_manager.insertFlow( uuid, "of:000000000000000" + src_node, "0", src_port)
      self.network_manager.insertFlow( uuid, "of:000000000000000" + dst_node, dst_port, "0")
      
      #storing db
      database.context['connection'].append(connection)
      connectivity_service['connection'] = [ "/restconf/config/connection/" + uuid + "/" ]
      database.context['connectivity-service'].append(connectivity_service)

        
      return connectivity_service

    def delete_connectivity_service(self, uuid):
      logging.info("delete_connectivity_service %s", uuid)  
      self.network_manager.removeFlows(uuid)  
      
      for connection in database.context['connection']:
          if connection['uuid'] == uuid :
              database.context['connection'].remove(connection)
              
      for cs in database.context['connectivity-service']:
          if cs['uuid'] == uuid :
              database.context['connectivity-service'].remove(cs)
              return "done"
              