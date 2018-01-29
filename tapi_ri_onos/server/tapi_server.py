#!/usr/bin/env python3

import connexion
import json
from flask import current_app
import orchestrator.orchestrator as orchestrator
import database.database as database
import logging

ONOS=1

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    app = connexion.App(__name__, specification_dir='swagger/')
    app.add_api('swagger.yaml', arguments={'title': 'tapi-connectivity API generated from tapi-connectivity.yang'})
    app.app.config['JSON_SORT_KEYS']=False
    
    #Starting orchestrator    
    database.ONOS=ONOS
    if ONOS == 1:
      orch = orchestrator.Orchestrator(ONOS)
      database.orch_instance=orch
      database.context = {
        "service-interface-point" : [ ],
        "topology" : [ ],
        "connection" : [ ],
        "connectivity-service" : [  ]
      }
      orch.network_manager.load_topology()
    else:
      with app.app.app_context():
        with current_app.open_resource("database/context.json", 'r') as f:
          database.context = json.load(f)
    
    #Run server
    app.run(port=8080, debug=False)
