from src import loadgenerator
from src import amiserviceregistrar
from src import amiping
amiservice = amiserviceregistrar.AMIServiceRegistrar.registerami("callserver","localhost",5038,"ameyodebug","dacx")


thread0 = amiping.Thread("amipingpongthread",1, amiservice)
thread1 = loadgenerator.Thread("amithread",2 ,amiservice,1,50,True)


thread0.start()
thread1.start()

thread0.join()
thread1.join()



