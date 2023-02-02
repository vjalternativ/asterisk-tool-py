from src import amiservice
keyvsservice = {}

def event_listener(event,**kwargs):
    print(event)
    
    


class AMIServiceRegistrar():
    
    @staticmethod
    def registerami(key,address,port,username,secret):
        service = amiservice.AMIService(address,port,username,secret)
        service.login(username,secret)
        service.add_event_listener(event_listener)
        keyvsservice[key] = service
        return service