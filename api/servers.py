import glob

def getServerList():
    if glob.srv_list == None:
        cacheServerList()
    return glob.srv_list

def cacheServerList():
    cursor = glob.sql.cursor()
    cursor.execute("SELECT Host,Frontend,Bancho,Avatar,Direct,DirectAuth,protocol FROM server_list ORDER BY id ASC")
    rows = cursor.fetchall()
    glob.srv_list = rows
