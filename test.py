from src import loadgenerator
from src import amiserviceregistrar
amiservice = amiserviceregistrar.AMIServiceRegistrar.registerami("callserver","localhost",5038,"ameyodebug","dacx")

thread1 = loadgenerator.Thread("amithread",1 ,amiservice,5)


thread1.start()


