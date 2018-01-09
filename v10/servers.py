import glob

srv_list = None

def getServerList():
    if srv_list == None:
        cacheServerList()
    return srv_list

def cacheServerList():
    srv_list = 0