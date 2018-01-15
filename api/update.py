import glob

def check():
    if glob.update_list == None:
        cacheUpdateList()
    return glob.update_list

def path(i):
    cursor = glob.sql.cursor()
    cursor.execute("SELECT file_version,filename,file_hash,filesize,filesize_zip,timestamp,patch_id,url_full,url_patch FROM check_table WHERE file_version = {} ORDER BY file_version DESC LIMIT 1".format(i))
    rows = cursor.fetchall()
    if len(rows) == 0:
        raise Exception("Unable to find entry from file_version!")
    
    return rows[0]
    
def latest():
    if glob.update_list == None:
        cacheUpdateList()
    l = [x for x in glob.update_list if x["filename"] == "osu!.exe"]

    if len(l) == 0:
        raise Exception("No osu file found!")
    
    return l[0]["url_full"]
    

def cacheUpdateList():
    glob.update_list = []

    cursor = glob.sql.cursor()
    cursor.execute("SELECT filename FROM check_table GROUP BY filename")
    rows = cursor.fetchall()
    for row in rows:
        glob.update_list.append(getLatestFile(row["filename"]))
   #glob.update_list = rows

def getLatestFile(filename):
    cursor = glob.sql.cursor()
    cursor.execute("SELECT file_version,filename,file_hash,filesize,filesize_zip,timestamp,patch_id,url_full,url_patch FROM check_table WHERE filename = '{}' ORDER BY file_version DESC LIMIT 1".format(filename))
    rows = cursor.fetchall()
    if len(rows) == 0:
        raise Exception("Unable to find entry from filename!")
    
    rows[0]["timestamp"] = str(rows[0]["timestamp"]) #Bootleg fix to make python return the right value instead of the timestamp as an object
    return rows[0]
