import os.path
import time
import glob
from pathlib import Path

def handle_crash(request):
    filename = str(int(time.time()))

    if "u" in request.args:
        filename += "-{}".format(request.args.get("u"))
    
    full_filename = None
    
    full_filename = os.path.join(glob.config["handle"]["crash"], filename + "-{}.txt")

    file_id = 0
    while Path(full_filename.format(file_id)).is_file():
        file_id += 1

    file = open(full_filename.format(file_id), "w")

    for arg in request.args:
        file.write("{}: {}\n".format(arg, request.args.get(arg)))
    
    file.close()