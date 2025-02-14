import threading
import math
import time
import os
import json
import csv
from datetime import datetime
class Service(threading.Thread):
    def __init__(self,thread_name,thread_id,amiservice,maxcalls, cps, callparams):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_id = thread_id
        self.amiservice = amiservice
        self.maxcalls = maxcalls
        self.cps = cps
        self.channelsData =  {}
        self.callparams = callparams

        
        #amiservice.add_event_listener(on_DialEnd=self.on_DialEnd)
        #amiservice.add_event_listener(on_Newchannel=self.on_NewChannelEvent)
        #amiservice.add_event_listener(on_VarSet=self.on_VarSetEvent)
        #amiservice.add_event_listener(on_Hangup = self.on_Hangup)

   


        

    def run(self) :
        self.start_time  = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
        ctx = f"{self.thread_name} : {self.thread_id}"
        str =  f"{ctx} executing thread"
        print(str)    
        n = math.ceil(self.maxcalls/self.cps)
        for i in range(n):
            j = i + 1
            endto = j * self.cps
            calls = self.cps if endto <= self.maxcalls else (self.maxcalls % self.cps)
            numberprefix = f"{self.callparams['to_prefix']}{i}"
            self.amiservice.generateload(ctx,calls, self.callparams['sipentity'],self.callparams['extension'],self.callparams['context'],numberprefix,self.callparams['callerid'], self.callparams['dynamic_to'], self.callparams['to_number'])
            time.sleep(1)
        while(True) :
            self.checkreport()
            if(self.maxcalls == self.summary['total_channels'] and self.summary['total_channels'] == self.summary['total_hangup']):
                break;
            time.sleep(5)

    def printreport(self):
        path = f"loadreport-{self.maxcalls}-{self.start_time}"
        if not os.path.exists(path):
            os.makedirs(path)
        ctx = f"{self.thread_name}_{self.thread_id}"
        
        filename = f'{path}/load-summary-{ctx}.json'
        with open(filename, 'w') as f:
            json.dump(self.summary, f)
        
        filename = f'{path}/load-channel-{ctx}.csv'
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = list(self.csvheaderlist.keys())
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for channel in self.channelsData.values():
                writer.writerow(channel)
           
    def checkreport(self):
        ctx = f"{self.thread_name} : {self.thread_id}"
        print(f"report {ctx} : {self.summary}")
        self.summary = self.amiservice.summary
        self.printreport()
        

            
class Thread(Service, threading.Thread):
    def __init__(self,thread_name,thread_id,amiservice,maxcalls, cps, callparams):
        threading.Thread.__init__(self)
        Service.__init__(self,thread_name,thread_id,amiservice,maxcalls, cps, callparams)
        
