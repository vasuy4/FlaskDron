from arduino_communication import send_command
from flask import Flask, render_template, request, jsonify, Response
import time
from typing import Dict, List, Union

app = Flask(__name__)

"""
ключ - наименование команды
значение - кортеж из:
1) Значение команды
2) Последняя отправка на ардуино
3) Было ли отправлено это значение
"""
BUFFER: Dict[str, List[Union[int, float, bool]]] = {
    "SERVO": [90, time.time(), True],
    "LENGINE": [90, time.time(), True],
    "RENGINE": [90, time.time(), True],
}


def auto_update() -> None:
    """
    Поток автоматической отправки команд на ардуино каждые 0.5 секунды
    """
    while True:
        for command, value in BUFFER.items():
            if not value[2] and time.time() - value[1] > 0.5:
                send_command("{}_{}\n".format(command, value[0]))
        time.sleep(0.5)


@app.route("/")
def main_menu():
    return render_template("index.html")


@app.route("/update_slider", methods=["POST"])
def update_slider() -> Response:
    """
    Обновляет значение слайдера и буфера отправки команды на ардуино
    """
    slider_servo = request.json.get("slider_servo")
    slider_engine_left = request.json.get("slider_engine_left")
    slider_engine_right = request.json.get("slider_engine_right")
    slider_now_speed = request.json.get("slider_engine_now_speed")
    slider_direction = request.json.get("slider_direction")

    print('speed', slider_now_speed)
    response_data = {}

    if slider_servo is not None:
        response_data["slider_value_servo"] = slider_servo
        value_command: int = min(max(int(slider_servo) + 90, 10), 179)
        BUFFER["SERVO"][0] = value_command
        BUFFER["SERVO"][2] = False
    if slider_engine_left is not None:
        response_data["slider_value_engine_left"] = slider_engine_left
        response_data["slider_value_speed"] = int(slider_engine_left) / 2 + int(slider_now_speed or 0)

        value_command: int = min(max(int(slider_engine_left) + 90, 10), 179)
        BUFFER["LENGINE"][0] = value_command
        BUFFER["LENGINE"][2] = False
    if slider_engine_right is not None:
        response_data["slider_value_engine_right"] = slider_engine_right
        response_data["slider_value_speed"] = int(slider_engine_right) / 2 + int(slider_now_speed or 0)

        value_command: int = min(max(int(slider_engine_right) + 90, 10), 179)
        BUFFER["RENGINE"][0] = value_command
        BUFFER["RENGINE"][2] = False
    return jsonify(response_data)
