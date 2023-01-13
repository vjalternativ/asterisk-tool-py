from asterisk.ami import AMIClient
from asterisk.ami import SimpleAction
import time


client = AMIClient("localhost", "5038")
client.login("ameyodebug", "dacx")


i =1
while(i > 0):
    action = SimpleAction('Ping', ActionID="")
    client.send_action(action)
    time.sleep(1)
    