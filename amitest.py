from src import amiserviceregistrar
import configparser
from asterisk.ami import SimpleAction 



class AMIClientListener(object):
    methods = ['on_action', 'on_response', 'on_event', 'on_connect', 'on_disconnect', 'on_unknown']

    def __init__(self, **kwargs):
        self.exitLoop = False
        self.customerActionId = "originate-customer-1"
        self.localActionId = "originate-local-1"
        self.customerChannel = ""
        self.localChannel = ""
        for k, v in kwargs.items():
            if k not in self.methods:
                raise TypeError('\'%s\' is an invalid keyword argument for this function' % k)
            setattr(self, k, v)

    def on_action(self, source, action):
        print(f"executng action {action}")

    def on_response(self, source, response):
        print(f"executng response {response}")

    def on_event(self, source, event):
        if(event.name =="Newchannel"):
            print(event.keys)
            print(f" newChannelevent keys {event.keys['ActionID']}")
            if(event.keys['ActionID'] == self.customerActionId):
                self.customerChannel = event.keys['Channel']
            elif(event.keys["ActionID"] == self.localActionId):
                self.localChannel = event.keys['Channel'].split(";")[0]
            print(f"customer channel {self.customerChannel} and local channel {self.localChannel}")
                

    def on_connect(self, source):
        print("onConnect")


    def on_disconnect(self, source, error=None):
        print(f"onDisconnect {source} and error {error}")
        self.exitLoop = True

    def on_unknown(self, source, pack):
        print("onUnknown")

    def run(self):
        while(True):
            if(self.exitLoop == True):
                break

config = configparser.ConfigParser()
config.read('./config.yml')
astconf = config['asterisk']
callparams = config['callparams']

amiservice = amiserviceregistrar.AMIServiceRegistrar.registerami("callserver", astconf['host'], int(astconf['port']),astconf['user'],astconf['secret'],callparams)

listener = AMIClientListener()
amiservice.add_listener(listener)
        
action = SimpleAction('Originate',Channel=f'SIP/a@asap_1',Exten='callconfer',Priority=1,Context="from-manager-core", ActionID=listener.customerActionId, Async='true')
resp = amiservice.send_action(action)


action = SimpleAction('Originate',Channel=f'Local/a@vj',Exten='callconfer',Priority=1,Context="from-manager-core", ActionID=listener.localActionId, Async='true')
resp = amiservice.send_action(action)


listener.run()


