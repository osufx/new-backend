import glob

#Its the default server (They help me to not end it all)
md5_ripple = "ee723a62345bb9869196e13e018f834b" #ripple.moe

def getData(hash_str):
    if hash_str is None:
        hash_str = md5_ripple

    if hash_str not in glob.data_dist:
        cacheData(hash_str)
    return glob.data_dist[hash_str]

def cacheData(hash_str):
    cursor = glob.sql.cursor()
    cursor.execute("SELECT type,data,server FROM data_client WHERE server = '{}' ORDER BY id ASC".format(hash_str))
    rows = cursor.fetchall()
    if len(rows) > 0:
        glob.data_dist[hash_str] = rows