from asterisk.ami import AMIClient
from asterisk.ami import SimpleAction
import requests
import json
class AMIService(AMIClient):
    
    def __init__(self, address, port,username,secret, callparams):
        super().__init__(address, port)
        self.callparams = callparams
        self.login(username, secret)
        self.summary = { 
            "total_channels" : 0, 
            "dialstatus_vs_count" : {} , 
            "hangup_cause_vs_count" : {}, 
            "total_hangup" : 0
            }
        self.csvheaderlist = {}
        self.hangup_seq = 0
        self.startTime = ''
        
        
        self.add_event_listener(self.onAMIEvent)
        


    def generateload(self,ctx, num, channel,exten,context,numprefix,callerid, is_dynamic_to, to_number):

        for x in range(num):
            number = f"{numprefix}{x}"
            if self.callparams['webhook'] == "yes":
                url  = f"{self.callparams['webhook_url']}?CallSid=ascssdsac&CallFrom=ascsac&CallTo=ascsac"
                response = requests.get(url)
                if response.status_code == 200:
                    obj = json.loads(response.content)
                    number = obj['destination']['trunk']
                    print(f" orig {number}")
            if(is_dynamic_to == "no") :
                number = to_number
            action = SimpleAction('Originate',Channel=f'SIP/{number}@{channel}',Exten=exten,Priority=1,Context=context,CallerID=callerid,Async='true')
            resp = self.send_action(action)
            str = f"{ctx} originate SIP/{number}@{channel} extension {exten}@{context} for callerid {callerid} "
            print(str)
    

    def onAMIEvent(self,event,**kwargs):
        if event.name == "Newchannel" :
            self.on_NewChannelEvent(event)
        elif event.name == "VarSet" :
            self.on_VarSetEvent(event)
        elif event.name == "DialEnd" :
            self.on_DialEnd(event)
        elif event.name == "Hangup":
            self.on_Hangup(event)

    def on_DialEnd(self,event):
        self.csvheaderlist["DialStatus"] = 1
        self.channelsData[event.keys['DestChannel']]['DialStatus'] = event.keys['DialStatus']
        if(event.keys['DialStatus'] not in self.summary['dialstatus_vs_count']) :
            self.summary['dialstatus_vs_count'][event.keys['DialStatus']] =  1
        else :
            self.summary['dialstatus_vs_count'][event.keys['DialStatus']] = self.summary['dialstatus_vs_count'][event.keys['DialStatus']] + 1


    def on_Hangup(self, event):
       
        self.channelsData[event.keys['Channel']]['hangupCause'] = event.keys['Cause']
        self.channelsData[event.keys['Channel']]['hangupCauseText'] = event.keys['Cause-txt']
        self.csvheaderlist["hangupCause"] = 1
        self.csvheaderlist["hangupCauseText"] =1
        if(event.keys['Cause'] not in self.summary['hangup_cause_vs_count']) :
            self.summary['hangup_cause_vs_count'][event.keys['Cause']] =  1
        else :
            self.summary['hangup_cause_vs_count'][event.keys['Cause']] = self.summary['hangup_cause_vs_count'][event.keys['Cause']] + 1
        self.summary['total_hangup'] = self.summary['total_hangup'] + 1

    def on_VarSetEvent(self, event):
      
        if event.keys['Variable'] == "SIPCALLID":
              self.csvheaderlist["sipcallid"] = 1
              self.channelsData[event.keys['Channel']]["sipcallid"] = event.keys['Value']
        elif event.keys['Variable']  in( "RTPAUDIOQOS","RTPAUDIOQOSRTT","RTPAUDIOQOSJITTER","RTPAUDIOQOSLOSS"):
            args = event.keys['Value'].strip(";").split(';')       
            for arg in args:
                keyval = arg.split('=')
                self.channelsData[event.keys['Channel']][keyval[0]] = keyval[1]
                self.csvheaderlist[keyval[0]] =  1
    
    def on_NewChannelEvent(self, event):
        self.channelsData[event.keys['Channel']] = {}
        self.summary['total_channels'] = self.summary['total_channels'] + 1
   