from asterisk.ami import AMIClient
from asterisk.ami import SimpleAction
import requests
import json
class AMIService(AMIClient):
    
    def __init__(self, address, port,username,secret, callparams):
        super().__init__(address, port)
        self.callparams = callparams
        self.login(username, secret)


    def generateload(self,ctx, num, channel,exten,context,numprefix,callerid):

        for x in range(num):
            number = f"{numprefix}{x}"
            if self.callparams['webhook'] == "yes":
                url  = f"{self.callparams['webhook_url']}?CallSid=ascssdsac&CallFrom=ascsac&CallTo=ascsac"
                response = requests.get(url)
                if response.status_code == 200:
                    obj = json.loads(response.content)
                    number = obj['destination']['trunk']
                    print(f" orig {number}")
            action = SimpleAction('Originate',Channel=f'SIP/{number}@{channel}',Exten=exten,Priority=1,Context=context,CallerID=callerid,Async='true')
            resp = self.send_action(action)
            str = f"{ctx} originate SIP/{number}@{channel} extension {exten}@{context} for callerid {callerid} "
            print(str)
            