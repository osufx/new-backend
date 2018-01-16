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
    cursor.execute("SELECT type,user,comment,date FROM update_log ORDER BY id DESC LIMIT 0,30")
    rows = cursor.fetchall()
    glob.changelog_list = rows

def changelog_format(logs):
    lines = [];
    for row in logs:
        if row["type"] == "comment":
            lines.append(row["comment"])
            continue

        c_type = {
            "add": "+",
            "fix": "*",
        }.get(row["type"], "+")

        line = "{}\t{}\t{}".format(c_type, row["user"], row["comment"])

        lines.append(line)
    return "\n".join(lines)