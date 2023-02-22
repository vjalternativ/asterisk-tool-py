import threading
import math
import time
class Thread(threading.Thread):
    def __init__(self,thread_name,thread_id,amiservice,maxcalls, cps):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_id = thread_id
        self.amiservice = amiservice
        self.maxcalls = maxcalls
        self.cps = cps
        self.channelsData =  {}
        amiservice.add_event_listener( 
            on_VarSet=self.on_VarSetEvent,
            on_Newchannel=self.on_NewChannelEvent)

    def on_VarSetEvent(self, event,**kwargs):
        self.channelsData[event.keys['Channel']][event.keys['Variable']] = event.keys['Value']
    
    def on_NewChannelEvent(self, event, **kwargs):
        self.channelsData[event.keys['Channel']] = {}


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
        self.printreport()

    def printreport(self):
        print(self.channelsData)
        

            


    