from src import amiserviceregistrar
import configparser
from asterisk.ami import SimpleAction
def onAMIEvent(self,event,**kwargs):
    print(event)
    

config = configparser.ConfigParser()
config.read('./config.yml')
astconf = config['asterisk']
callparams = config['callparams']

amiservice = amiserviceregistrar.AMIServiceRegistrar.registerami("callserver", astconf['host'], int(astconf['port']),astconf['user'],astconf['secret'],callparams)


amiservice.add_event_listener(onAMIEvent)
        
action = SimpleAction('Originate',Channel=f'SIP/a@asap_1',Exten='callconfer',Priority=1,Context="from-manager-core",ActionId= "orginate-customer")
resp = amiservice.send_action(action)


action = SimpleAction('Originate',Channel=f'Local/a@vj',Exten='callconfer',Priority=1,Context="from-manager-core", ActionId= "originate-local")
resp = amiservice.send_action(action)
            