#!/usr/bin/env python3

import connexion
import orchestrator.orchestrator as orchestrator
import database.database as database
import logging

ONOS=1

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.add_api('swagger.yaml', arguments={'title': 'tapi-connectivity API generated from tapi-connectivity.yang'})
    app.app.config['JSON_SORT_KEYS']=False
    
    #Starting orchestrator    
    orch = orchestrator.Orchestrator(ONOS)
    database.orch_instance=orch
    if ONOS == 1:
      orch.network_manager.load_topology()
    
    #Run server
    app.run(port=8080, debug=False)
