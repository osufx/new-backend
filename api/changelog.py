import glob

def getChangelog(is_json = False):
    if glob.changelog_list == None:
        cacheChangelogList()
    if is_json:
        return glob.changelog_list
    else:
        return changelog_format(glob.changelog_list)

def cacheChangelogList():
    cursor = glob.sql.cursor()
    cursor.execute()