from src import amiservice
keyvsclient = {}
class AMIServiceRegistrar():

    @staticmethod
    def registerami(key,address,port,username,secret):
        client = amiservice.AMIService(address,port,username,secret)
        client.login(username,secret)
        keyvsclient[key] = client
        return client