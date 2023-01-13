import threading

from asterisk.ami import SimpleAction

class Thread(threading.Thread):
    def __init__(self,thread_name,thread_id,amiclient,maxcalls):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_id = thread_id
        self.amiclient = amiclient
        self.maxcalls = maxcalls

    def run(self) :
        ctx = f"{self.thread_name} : {self.thread_id}"
        str =  f"{ctx} executing thread"
        print(str)    
        self.amiclient.genereateload(ctx,self.maxcalls, "test","moh","test",'100')

            


    