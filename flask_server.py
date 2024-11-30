from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def main_menu():
    return render_template("index.html")
