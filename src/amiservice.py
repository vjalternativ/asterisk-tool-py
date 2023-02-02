from asterisk.ami import AMIClient
from asterisk.ami import SimpleAction
class AMIService(AMIClient):
    
    def __init__(self, address, port,username,secret):
        super().__init__(address, port)
        self.login(username, secret)


    def generateload(self,ctx, num, channel,exten,context,numprefix,callerid):

        for x in range(num):
            number = f"{numprefix}{x}" 
            action = SimpleAction('Originate',Channel=f'SIP/{number}@{channel}',Exten=exten,Priority=1,Context=context,CallerID=callerid,Async='true')
            self.send_action(action)
            str = f"{ctx} originated leg for callerid {callerid}"
            print(str)