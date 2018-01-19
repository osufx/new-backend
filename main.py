import json
import random
import MySQLdb
import MySQLdb.cursors
from flask import Flask, make_response, redirect, request, render_template, url_for, flash, jsonify, Response
from api import servers
from api import update
from api import changelog
from api import data
from handlers import crash

import glob

app = Flask(__name__)

with open("config.json", "r") as f:
    config = json.load(f)

glob.config = config

with open("api_response.json", "r") as f:
    api_response = json.load(f)

glob.sql = MySQLdb.connect(**config["sql"], cursorclass = MySQLdb.cursors.DictCursor)

@app.route("/", methods=["GET", "POST"])
def main_index():
    return "This be osufx backend ;)"

@app.route("/v10/servers/")
@app.route("/v10/servers")
def serve_servers():
    srv_list = servers.getServerList()
    return jsonify(srv_list)

@app.route("/v10/update/", methods=["GET"])
@app.route("/v10/update", methods=["GET"])
def serve_update():
    action = request.args.get("action")
    target = request.args.get("target")
    res = update.getUpdateList(action, target)
    return res

@app.route("/v10/changelog/", methods=["GET"])
@app.route("/v10/changelog", methods=["GET"])
def serve_changelog():
    if request.args.get("json") is not None:
        res = changelog.getChangelog(True)
        return jsonify(res)
    else:
        res = changelog.getChangelog(False)
        return Response(res, mimetype="text/raw")

@app.route("/v10/data/", methods=["GET"])
@app.route("/v10/data", methods=["GET"])
def serve_data():
    s = request.args.get("s")
    res = data.getData(s)
    return jsonify(res)

@app.route("/v10/crash/", methods=["GET", "POST"])
@app.route("/v10/crash", methods=["GET", "POST"])
def handle_crash():
    crash.handle_crash(request)
    return jsonify({"code": 200, "message": "OK"})

@app.errorhandler(500)
@app.errorhandler(410)
@app.errorhandler(404)
@app.errorhandler(403)
@app.errorhandler(401)
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