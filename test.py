from src import loadgenerator
from src import amiserviceregistrar
from src import amiping
import configparser
import argparse


config = configparser.ConfigParser()
config.read('./config.yml')
astconf = config['asterisk']
callparams = config['callparams']
parser = argparse.ArgumentParser()

parser.add_argument('--channels','-n', type=int, required=True)

parser.add_argument('--cps','-c', type=int, required=True)


args = parser.parse_args()




amiservice = amiserviceregistrar.AMIServiceRegistrar.registerami("callserver", astconf['host'], int(astconf['port']),astconf['user'],astconf['secret'],callparams)

service = loadgenerator.Service("amithread",2,amiservice,args.cps,args.cps,callparams)
service.run()

#thread0 = amiping.Thread("amipingpongthread",1, amiservice)
#thread1 = loadgenerator.Thread("amithread",2 ,amiservice,args.cps,args.cps,callparams)


#thread0.start()
#thread1.start()

#thread0.join()
#thread1.join()



