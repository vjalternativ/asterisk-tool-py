from asterisk.ami import AMIClient
keyvsclient = {}
class AMIServiceRegistrar():

    @staticmethod
    def registerami(key,address,port,username,secret):
        client = AMIClient(address,port)
        client.login(username,secret)
        keyvsclient[key] = client
        return client