import threading
import time
from asterisk.ami import SimpleAction

class Thread(threading.Thread):
    def __init__(self,thread_name,thread_id,amiclient):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_id = thread_id
        self.amiclient = amiclient

    def run(self) :
        str =  f"{self.thread_name} : {self.thread_id} executing thread"
        action = SimpleAction('Originate',Channel='SIP/test',Exten='moh',Priority=1,Context='test',CallerID='test',Async='true')
        self.amiclient.send_action(action)


    