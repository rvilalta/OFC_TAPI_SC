from flask import Flask
import thread
from notification_factory import NotificationServerFactory
## EXAMPLE IMPORT SERVER MODELS
import Tapi
import TapiTopology
import TapiConnectivity
import TapiPathComputation
import TapiVirtualNetwork
import TapiNotification
import backend_api
import backend.backend as be

def launch_notification_server():
    return thread.start_new_thread(NotificationServerFactory,())

IP="127.0.0.1"
PORT="8181"
CTL_TYPE="ONOS"
USER="onos"
PASSWORD="rocks"

app = Flask(__name__)
app.register_blueprint(getattr(Tapi, "Tapi"))
app.register_blueprint(getattr(TapiTopology, "TapiTopology"))
app.register_blueprint(getattr(TapiConnectivity, "TapiConnectivity"))
app.register_blueprint(getattr(TapiPathComputation, "TapiPathComputation"))
app.register_blueprint(getattr(TapiVirtualNetwork, "TapiVirtualNetwork"))
app.register_blueprint(getattr(TapiNotification, "TapiNotification"))
app.register_blueprint(getattr(backend_api, 'backend_api'))

if __name__ == "__main__":
    nf = launch_notification_server()
    be.connect_sdn_controller(ip=IP, port=PORT, ctl_type=CTL_TYPE, user=USER, password=PASSWORD)
    app.run(host='0.0.0.0', port = 8080, debug=False)
    
