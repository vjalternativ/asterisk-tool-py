from src import loadgenerator
from src import amiserviceregistrar
client = amiserviceregistrar.AMIServiceRegistrar.registerami("callserver","localhost",5038,"ameyodebug","dacx")

thread1 = loadgenerator.Thread("amithread",1 ,client)


thread1.start()
thread2.start()



