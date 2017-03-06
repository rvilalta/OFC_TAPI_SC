import os.path, sys
sys.path.append(os.path.join('/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])))
import backend.backend as be


class Context_TopologyUuid_NodeImpl:

    @classmethod
    def get(cls, uuid):
        print 'handling get'
        if uuid in be.Context._topology:
            array_cs=[]
            for cs in be.Context._topology[uuid]._node:
                uri="restconf/config/Context/_topology/"+uuid+"/_node/"+be.Context._topology[uuid]._node[cs].uuid+"/"
                print uri
                array_cs.append(uri)
            json = { 'itemlist' : array_cs }
            return json
        else:
            raise KeyError('uuid')
