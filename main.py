import json
import random
import MySQLdb
import MySQLdb.cursors
from flask import Flask, make_response, redirect, request, render_template, url_for, flash, jsonify
from api import servers
from api import update

import glob

app = Flask(__name__)

with open("config.json", "r") as f:
    config = json.load(f)

with open("api_response.json", "r") as f:
    api_response = json.load(f)

glob.sql = MySQLdb.connect(**config["sql"], cursorclass = MySQLdb.cursors.DictCursor)

@app.route('/', methods=['GET', 'POST'])
def main_index():
    return "This be osufx backend ;)"

@app.route("/v10/servers")
def serve_servers():
    srv_list = servers.getServerList()
    return jsonify(srv_list)

@app.route("/v10/update", methods=['GET'])
def serve_update():
    res = {"code": 200, "message": "no action specified"}
    action = request.args.get('action')
    if action is not None:
        if action == "check":
            res = update.check()
        elif action == "path":
            target = request.args.get('target')
            res["message"] = "no target specified"
            if target is not None:
                try:
                    res = update.path(int(float(target)))
                except:
                    res["message"] = "invalid target file"
        elif action == "latest":
            res = update.latest()
        else:
            res["message"] = "invalid action"
    return jsonify(res)
    

@app.errorhandler(404)
def not_found(error):
    lookup = "common"

    if random.randint(0, 5) != 0 and str(error.code) in api_response.keys():
        lookup = str(error.code)

    msg = api_response[lookup]

    #Randomize
    msg = msg[random.randint(0, len(msg) - 1)]

    res = {
        "code": error.code,
        "message": msg
    }

    return jsonify(res)

if __name__ == "__main__":
    app.run(**config["web"])