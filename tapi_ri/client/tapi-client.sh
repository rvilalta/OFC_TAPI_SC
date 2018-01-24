#Set Context
curl -X POST -H "Content-Type: application/json" http://127.0.0.1:8080/restconf/config/context/ -d @context.json

#Get Context
curl -X GET -H "Content-Type: application/json" http://127.0.0.1:8080/restconf/config/context/ 

#Get topologies
curl -X GET -H "Content-Type: application/json" http://127.0.0.1:8080/restconf/config/context/topology/

#Get topology Top0
curl -X GET -H "Content-Type: application/json" http://127.0.0.1:8080/restconf/config/context/topology/top0/

#Get nodes
curl -X GET -H "Content-Type: application/json" http://127.0.0.1:8080/restconf/config/context/topology/top0/node/

#Get node 1
curl -X GET -H "Content-Type: application/json" http://127.0.0.1:8080/restconf/config/context/topology/top0/node/node0/

#Get links
curl -X GET -H "Content-Type: application/json" http://127.0.0.1:8080/restconf/config/context/topology/top0/link/

#Get link 1-3
curl -X GET -H "Content-Type: application/json" http://127.0.0.1:8080/restconf/config/context/topology/top0/link/link0/

#Get Service End Points
curl -X GET -H "Content-Type: application/json" http://127.0.0.1:8080/restconf/config/context/service-interface-point/sip1/
curl -X GET -H "Content-Type: application/json" http://127.0.0.1:8080/restconf/config/context/service-interface-point/sip2/

#Create Connectivity Service #connected with ONOS
curl -X POST -H "Content-Type: application/json" http://127.0.0.1:8080/restconf/config/context/connectivity-service/ -d'{ "_connConstraint":{"serviceType":"POINT_TO_POINT_CONNECTIVITY", "serviceLayer":["OCH"] }, "_servicePort":[ { "localId":"sp1", "serviceLayer":"OCH" , "direction":"BIDIRECTIONAL", "role":"SYMMETRIC", "_serviceEndPoint":"http://127.0.0.1:8080/restconf/config/Context/_serviceEndPoint/of:0000000000000001"}, { "localId":"sp2", "serviceLayer":"OCH" , "direction":"BIDIRECTIONAL", "role":"SYMMETRIC", "_serviceEndPoint":"http://127.0.0.1:8080/restconf/config/Context/_serviceEndPoint/of:0000000000000003"} ] }'

#Get Connectivity Services
curl -X GET -H "Content-Type: application/json" http://127.0.0.1:8080/restconf/config/context/connectivity-service/

curl -X GET -H "Content-Type: application/json" http://127.0.0.1:8080/restconf/config/context/connectivity-service/cs1/

curl -X DELETE -H "Content-Type: application/json" http://127.0.0.1:8080/restconf/config/context/connectivity-service/186/

curl -X DELETE -H "Content-Type: application/json" http://127.0.0.1:8080/restconf/config/context/connectivity-service/cs1/



