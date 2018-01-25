import logging
import database.database as database
import orchestrator.network_manager as network_manager


class Orchestrator:
    def __init__(self, onos):
        self.onos=onos
        self.network_manager=network_manager.network_manager()

    def create_tunnel(self, name, tunnel):
        #check if named-explicit-path
        
        nep = tunnel['p2p-primary-paths']['p2p-primary-path'][0]['config']['named-explicit-path']
        logging.debug("Looking nep %s", nep)
        rro_subobject = []
        found=False
        for nepid in database.te['te']['globals']['named-explicit-paths']['named-explicit-path']:
            logging.debug("looking nep %s %s", nep, nepid)
            if nep == nepid['name']:
                logging.debug("Found named-explicit-path: %s", nep )
                found=True
                #construct rro
                for ero_item in nepid['explicit-route-objects']['explicit-route-object']:
                  rro={}
                  logging.debug("Reading ero %s", ero_item)
                  rro['index']=ero_item['index']
                  rro['unnumbered']={}
                  rro['unnumbered']['node-id'] = ero_item['config']['unnumbered-hop']['router-id']
                  rro['unnumbered']['link-tp-id'] = ero_item['config']['unnumbered-hop']['interface-id']
                  rro_subobject.append (rro)  
        if not found:
          return found    
                
        #construct lsp
        lsp = {
                'tunnel-id' : name,
                'lsp-id' : name,
                'lsp-record-route-subobjects' : {
                  'record-route-subobject' : rro_subobject
                }
              }
        database.te['te']['lsps-state']['lsp'].append(lsp)
        database.te['te']['tunnels']['tunnel'].append(tunnel)
        return found

    def delete_tunnel(self, name):
        logging.info("delete_tunnel %s", name)
        for lsp in database.te['te']['lsps-state']['lsp']:
            if lsp['tunnel-id'] == name :
                logging.debug("removing lsp with tunnel-id %s", lsp['tunnel-id'] )
                database.te['te']['lsps-state']['lsp'].remove(lsp)