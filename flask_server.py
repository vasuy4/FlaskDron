from flask import Flask

app = Flask(__name__)


@app.route("/")
def main_menu():
    # response = send_command(command)
    # print("Response:", response)
    return "Hello bebra"
