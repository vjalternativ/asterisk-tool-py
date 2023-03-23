from asterisk.ami import AMIClient
from asterisk.ami import SimpleAction
import requests
import json
class AMIService(AMIClient):
    
    def __init__(self, address, port,username,secret):
        super().__init__(address, port)
        self.login(username, secret)


    def generateload(self,ctx, num, channel,exten,context,numprefix,callerid , webhook = None):

        for x in range(num):
            number = f"{numprefix}{x}"
            number ="trmum1e453bd91a2c9113cd416ct"
            if webhook is not None:
                url  = 'http://10.0.0.65:8081/v1/sip-trunk-webhook?CallSid=ascssdsac&CallFrom=ascsac&CallTo=ascsac'
                response = requests.get(url)
                if response.status_code == 200:
                    obj = json.loads(response.content)
                    number = obj['destination']['trunk']
                    print(f" get trunksid from routing service is {number}")
            action = SimpleAction('Originate',Channel=f'SIP/{number}@{channel}',Exten=exten,Priority=1,Context=context,CallerID=callerid,Async='true')
            self.send_action(action)
            str = f"{ctx} originated leg for callerid {callerid}"
            print(str)