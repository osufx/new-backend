import json
from flask import Flask, make_response, redirect, request, render_template, url_for, flash

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def main_index():
    return "This be osufx backend ;)"

with open("config.json", "r") as f:
    config = json.load(f)

@app.errorhandler(404)
def not_found(error):
    return '404'

if __name__ == "__main__":
    app.run(**config)