import threading
import math
import time
import sys
import json
import csv

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
        self.csvheaderlist = {}
        self.hangup_seq = 0
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
        print("increasing hangup count")
        self.summary['total_hangup'] = self.summary['total_hangup'] + 1

    def on_VarSetEvent(self, event):
      
        if event.keys['Variable'] == "SIPCALLID":
              self.csvheaderlist["sipcallid"] = 1
              self.channelsData[event.keys['Channel']]["sipcallid"] = event.keys['Value']
        elif event.keys['Variable']  in( "RTPAUDIOQOS"):
            # "RTPAUDIOQOSRTT","RTPAUDIOQOSJITTER","RTPAUDIOQOSLOSS"
            args = event.keys['Value'].strip(";").split(';')       
            for arg in args:
                keyval = arg.split('=')
                self.channelsData[event.keys['Channel']][keyval[0]] = keyval[1]
                self.csvheaderlist[keyval[0]] =  1
    
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
            numberprefix = "trmum1e453bd91a2c9113cd416ct" 
            self.amiservice.generateload(ctx,calls, "ip_plateform","moh","test",numberprefix,'01417119470')
            time.sleep(1)
        while(True) :
            self.checkreport()
            if(self.maxcalls == self.summary['total_channels'] and self.summary['total_channels'] == self.summary['total_hangup']):
                break;
            time.sleep(5)

    def printreport(self):
        ctx = f"{self.thread_name}_{self.thread_id}"
        
        filename = f'load-summary-{ctx}.json'
        with open(filename, 'w') as f:
            json.dump(self.summary, f)
        
        filename = f'load-channel-{ctx}.csv'
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = list(self.csvheaderlist.keys())
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for channel in self.channelsData.values():
                writer.writerow(channel)

    def checkreport(self):
        ctx = f"{self.thread_name} : {self.thread_id}"
        print(f"report for context {ctx}")
        print(self.summary)
        self.printreport()
        

            

            


    