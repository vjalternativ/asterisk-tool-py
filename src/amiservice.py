from asterisk.ami import AMIClient
from asterisk.ami import SimpleAction
class AMIService(AMIClient):
    
    def __init__(self, address, port,username,secret):
        super().__init__(address, port)
        super().login(username, secret)


    def generateload(self,ctx, num, channel,exten,context,calleridprefix):

        for x in range(num):
            callerid = f"{calleridprefix}num" 
            action = SimpleAction('Originate',Channel=f'SIP/{channel}',Exten=exten,Priority=1,Context=context,CallerID=callerid,Async='true')
            self.amiclient.send_action(action)
            str = f"{ctx} originated leg for callerid {callerid}"
            print(str)