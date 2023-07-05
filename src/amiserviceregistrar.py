from src import amiservice
keyvsservice = {}



class AMIServiceRegistrar():
    
    @staticmethod
    def registerami(key,address,port,username,secret, callparams):
        service = amiservice.AMIService(address,port,username,secret, callparams)
        service.login(username,secret)
        keyvsservice[key] = service
        return service