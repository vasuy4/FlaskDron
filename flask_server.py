from arduino_communication import send_command
from flask import Flask, render_template, request, jsonify, Response, send_from_directory
import time
from typing import Dict, List, Union, Tuple

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


@app.route("/js/<path:filename>")
def serve_js(filename):
    return send_from_directory("templates/js", filename)



@app.route("/update_slider", methods=["POST"])
def update_slider() -> Response:
    """
    Обновляет значение слайдера и буфера отправки команды на ардуино
    """
    slider_servo = request.json.get("slider_servo")

    slider_engine_left = request.json.get("slider_engine_left")
    slider_engine_right = request.json.get("slider_engine_right")

    slider_speed = request.json.get("slider_speed")
    slider_direction = request.json.get("slider_direction")

    slider_engine_left_secondary = request.json.get("slider_engine_left_secondary")
    slider_engine_right_secondary = request.json.get("slider_engine_right_secondary")

    slider_speed_secondary = request.json.get("slider_speed_secondary")
    slider_direction_secondary = request.json.get("slider_direction_secondary")

    response_data = {}

    if slider_servo is not None:
        response_data["slider_value_servo"] = slider_servo
        value_command: int = min(max(int(slider_servo) + 90, 10), 179)
        BUFFER["SERVO"][0] = value_command
        BUFFER["SERVO"][2] = False
    if slider_engine_left is not None:
        response_data["slider_value_engine_left"] = slider_engine_left
        response_data["slider_value_speed"] = (int(slider_engine_left) + int(slider_engine_right_secondary)) / 2
        response_data["slider_value_direction"] = (int(slider_engine_left) - int(slider_engine_right_secondary)) / 2

        value_command: int = min(max(int(slider_engine_left) + 90, 10), 179)
        BUFFER["LENGINE"][0] = value_command
        BUFFER["LENGINE"][2] = False
    if slider_engine_right is not None:
        response_data["slider_value_engine_right"] = slider_engine_right
        response_data["slider_value_speed"] = (int(slider_engine_right) + int(slider_engine_left_secondary)) / 2
        response_data["slider_value_direction"] = (int(slider_engine_left_secondary) - int(slider_engine_right)) / 2

        value_command: int = min(max(int(slider_engine_right) + 90, 10), 179)
        BUFFER["RENGINE"][0] = value_command
        BUFFER["RENGINE"][2] = False
    if slider_speed is not None:
        val_eng_left: int = int(slider_speed) + int(slider_direction_secondary)
        val_eng_right: int = int(slider_speed) - int(slider_direction_secondary)
        remainsL: int = 0
        remainsR: int = 0
        if abs(val_eng_left) > 90:
            if val_eng_left < 0:
                remainsL = val_eng_left + 90
            else:
                remainsL = val_eng_left - 90
        elif abs(val_eng_right) > 90:
            if val_eng_right < 0:
                remainsR = val_eng_right + 90
            else:
                remainsR = val_eng_right - 90

        response_data["slider_value_speed"] = slider_speed
        response_data["slider_value_engine_left"] = max(min(val_eng_left, 90), -90)
        response_data["slider_value_engine_right"] = max(min(val_eng_right, 90), -90)
        response_data["slider_value_direction"] = int(slider_direction_secondary) + remainsR - remainsL
    if slider_direction is not None:
        val_eng_left: int = int(slider_speed_secondary) + int(slider_direction)
        val_eng_right: int = int(slider_speed_secondary) - int(slider_direction)
        remainsL: int = 0
        remainsR: int = 0
        if abs(val_eng_left) > 90:
            if val_eng_left < 0:
                remainsL = val_eng_left + 90
            else:
                remainsL = val_eng_left - 90
        elif abs(val_eng_right) > 90:
            if val_eng_right < 0:
                remainsR = val_eng_right + 90
            else:
                remainsR = val_eng_right - 90

        response_data["slider_value_direction"] = slider_direction
        response_data["slider_value_engine_left"] = max(min(val_eng_left, 90), -90)
        response_data["slider_value_engine_right"] = max(min(val_eng_right, 90), -90)
        response_data["slider_value_speed"] = int(slider_speed_secondary) - (remainsL + remainsR) / 2
    return jsonify(response_data)
