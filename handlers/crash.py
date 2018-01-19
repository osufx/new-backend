import os.path
import time
import glob

def handle_crash(request):
    filename = str(int(time.time()))

    if "u" in request.args:
        filename += "-{}".format(request.args.get("u"))
        
    full_filename = os.path.join(glob.config["handle"]["crash"], filename + ".txt")

    file = open(full_filename, "w")

    for arg in request.args:
        file.write("{}: {}\n".format(arg, request.args.get(arg)))
    
    file.close()