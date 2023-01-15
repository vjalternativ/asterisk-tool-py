from asterisk.ami import AMIClient
from asterisk.ami import SimpleAction
import time


client = AMIClient("localhost", 5038)

def event_listener(event,**kwargs):
    print(event)

client.add_event_listener(event_listener)
client.login("ameyodebug", "dacx")

def callback_response(response):
    print(response)


i =1
while(i > 0):
    action = SimpleAction('Ping', ActionID="")
    result = client.send_action(action,callback=callback_response)
    time.sleep(1)
    