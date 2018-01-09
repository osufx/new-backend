import json
import random
import MySQLdb
import MySQLdb.cursors
from flask import Flask, make_response, redirect, request, render_template, url_for, flash, jsonify
from api import servers

import glob

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def main_index():
    return "This be osufx backend ;)"

with open("config.json", "r") as f:
    config = json.load(f)

with open("api_response.json", "r") as f:
    api_response = json.load(f)

glob.sql = MySQLdb.connect(**config["sql"], cursorclass = MySQLdb.cursors.DictCursor)

@app.route("/v10/servers")
def serve_servers():
    srv_list = servers.getServerList()
    return jsonify(srv_list)

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