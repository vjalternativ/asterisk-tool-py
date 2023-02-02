from asterisk.ami import AMIClient
from asterisk.ami import SimpleAction
import time

import threading
class Thread(threading.Thread):
    def __init__(self,thread_name,thread_id,amiservice):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_id = thread_id
        self.amiservice = amiservice

    def callback_response(response):
        print(response)   

    def run(self) :
        i =1
        while(i > 0):
            action = SimpleAction('Ping', ActionID="")
            result = self.amiservice.send_action(action,callback=self.callback_response)
            time.sleep(1)
    