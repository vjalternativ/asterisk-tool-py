import threading
class Thread(threading.Thread):
    def __init__(self,thread_name,thread_id,amiservice,maxcalls):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_id = thread_id
        self.amiservice = amiservice
        self.maxcalls = maxcalls

    def run(self) :
        ctx = f"{self.thread_name} : {self.thread_id}"
        str =  f"{ctx} executing thread"
        print(str)    
        self.amiservice.genereateload(ctx,self.maxcalls, "test","moh","test",'100')

            


    