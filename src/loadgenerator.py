import threading
import math
import time
import sys
class Thread(threading.Thread):
    def __init__(self,thread_name,thread_id,amiservice,maxcalls, cps):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_id = thread_id
        self.amiservice = amiservice
        self.maxcalls = maxcalls
        self.cps = cps
        self.channelsData =  {}
        self.summary = { 
            "total_channels" : 0, 
            "dialstatus_vs_count" : {} , 
            "hangup_cause_vs_count" : {}, 
            "total_hangup" : 0
            }
        amiservice.add_event_listener(self.onAMIEvent)
        #amiservice.add_event_listener(on_DialEnd=self.on_DialEnd)
        #amiservice.add_event_listener(on_Newchannel=self.on_NewChannelEvent)
        #amiservice.add_event_listener(on_VarSet=self.on_VarSetEvent)
        #amiservice.add_event_listener(on_Hangup = self.on_Hangup)

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
       
        self.channelsData[event.keys['DestChannel']]['DialStatus'] = event.keys['DialStatus']
        if(event.keys['DialStatus'] not in self.summary['dialstatus_vs_count']) :
            self.summary['dialstatus_vs_count'][event.keys['DialStatus']] =  1
        else :
            self.summary['dialstatus_vs_count'][event.keys['DialStatus']] = self.summary['dialstatus_vs_count'][event.keys['DialStatus']] + 1


    def on_Hangup(self, event):
        self.channelsData[event.keys['Channel']]['hangupCause'] = event.keys['Cause']
        self.channelsData[event.keys['Channel']]['hangupCauseText'] = event.keys['Cause-txt']
        
        if(event.keys['Cause'] not in self.summary['hangup_cause_vs_count']) :
            self.summary['hangup_cause_vs_count'][event.keys['Cause']] =  1
        else :
            self.summary['hangup_cause_vs_count'][event.keys['Cause']] = self.summary['hangup_cause_vs_count'][event.keys['Cause']] + 1
        
        self.summary['total_hangup'] = self.summary['total_hangup'] + 1
        self.checkreport()

    def on_VarSetEvent(self, event):
        if event.keys['Variable'] == "SIPCALLID":
              self.channelsData[event.keys['Channel']]["sipcallid"] = event.keys['Value']
        elif event.keys['Variable']  in( "RTPAUDIOQOSRTT","RTPAUDIOQOSJITTER","RTPAUDIOQOSLOSS"):
            args = event.keys['Value'].split(',')       
            for arg in args:
                keyval = arg.split('=')
                self.channelsData[event.keys['Channel']][keyval[0]] = keyval[1]
    
    def on_NewChannelEvent(self, event):
        self.channelsData[event.keys['Channel']] = {}
        self.summary['total_channels'] = self.summary['total_channels'] + 1
 

    def run(self) :
        ctx = f"{self.thread_name} : {self.thread_id}"
        str =  f"{ctx} executing thread"
        print(str)    
        n = math.ceil(self.maxcalls/self.cps)
        for i in range(n):
            j = i + 1
            endto = j * self.cps
            calls = self.cps if endto <= self.maxcalls else (self.maxcalls % self.cps)
            numberprefix = f'0100{i}' 
            self.amiservice.generateload(ctx,calls, "ip_plateform","moh","test",numberprefix,'01417119470')
            time.sleep(1)

    def printreport(self):
        ctx = f"{self.thread_name} : {self.thread_id}"
        print(f"report for context {ctx}")
        print(self.summary)
        print(self.channelsData)
        sys.exit()

    def checkreport(self):
        if(self.maxcalls == self.summary['total_channels'] and self.summary['total_channels'] == self.summary['total_hangup']):
            self.printreport()
            

            


    