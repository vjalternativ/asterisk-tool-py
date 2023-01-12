from src import loadgenerator
from asterisk.ami import AMIClient

client = AMIClient(address='localhost',port=5038)
client.login(username='ameyodebug',secret='dacx')

thread1 = loadgenerator.Thread("amithread",1 ,client)
thread2 = loadgenerator.Thread("amithread",2 , client)

thread1.start()
thread2.start()



