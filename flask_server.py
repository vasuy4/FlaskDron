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
BUFFER: Dict[str, List[Union[float, float, bool]]] = {
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

    anchor_value = request.json.get("anchor_value")

    response_data = {}

    if slider_servo is not None:
        response_data["slider_value_servo"] = slider_servo
        value_command: float = min(max(float(slider_servo) + 90, 10), 179)
        BUFFER["SERVO"][0] = value_command
        BUFFER["SERVO"][2] = False
    if slider_engine_left is not None:
        response_data["slider_value_engine_left"] = slider_engine_left
        if anchor_value != "slider_engine_left":
            response_data["slider_value_speed"] = (float(slider_engine_left) + float(slider_engine_right_secondary)) / 2
            response_data["slider_value_direction"] = (float(slider_engine_left) - float(slider_engine_right_secondary)) / 2

        value_command: float = min(max(float(slider_engine_left) + 90, 10), 179)
        BUFFER["LENGINE"][0] = value_command
        BUFFER["LENGINE"][2] = False
    if slider_engine_right is not None:
        response_data["slider_value_engine_right"] = slider_engine_right
        if anchor_value != "slider_engine_right":
            response_data["slider_value_speed"] = (float(slider_engine_right) + float(slider_engine_left_secondary)) / 2
            response_data["slider_value_direction"] = (float(slider_engine_left_secondary) - float(slider_engine_right)) / 2

        value_command: float = min(max(float(slider_engine_right) + 90, 10), 179)
        BUFFER["RENGINE"][0] = value_command
        BUFFER["RENGINE"][2] = False
    if slider_speed is not None:
        response_data["slider_value_speed"] = slider_speed
        if anchor_value != "slider_speed":
            val_eng_left: float = float(slider_speed) + float(slider_direction_secondary)
            val_eng_right: float = float(slider_speed) - float(slider_direction_secondary)
            val_eng_left = max(min(val_eng_left, 90), -90)
            val_eng_right = max(min(val_eng_right, 90), -90)

            response_data["slider_value_engine_left"] = val_eng_left
            response_data["slider_value_engine_right"] = val_eng_right
            response_data["slider_value_direction"] = slider_direction_secondary
    if slider_direction is not None:
        response_data["slider_value_direction"] = slider_direction
        if anchor_value != "slider_direction":
            val_eng_left: float = float(slider_speed_secondary) + float(slider_direction)
            val_eng_right: float = float(slider_speed_secondary) - float(slider_direction)
            val_eng_left = max(min(val_eng_left, 90), -90)
            val_eng_right = max(min(val_eng_right, 90), -90)

            val_speed = (val_eng_left + val_eng_right) / 2

            response_data["slider_value_engine_left"] = val_eng_left
            response_data["slider_value_engine_right"] = val_eng_right
            response_data["slider_value_speed"] = val_speed

    # Контрольный перерасчет значений
    recalculate_values(response_data, anchor_value)

    return jsonify(response_data)


def recalculate_values(response_data, anchor_value):
    """
    Контрольный перерасчет значений для исправления ошибок
    """
    speed = float(response_data.get("slider_value_speed", 0))
    direction = float(response_data.get("slider_value_direction", 0))
    engine_left = float(response_data.get("slider_value_engine_left", 0))
    engine_right = float(response_data.get("slider_value_engine_right", 0))

    # Пересчитываем значения двигателей на основе скорости и направления
    recalculated_engine_left = max(min(speed + direction, 90), -90)
    recalculated_engine_right = max(min(speed - direction, 90), -90)

    # Проверяем, выходят ли значения за пределы
    if engine_left != recalculated_engine_left or engine_right != recalculated_engine_right:
        if anchor_value != "slider_engine_left":
            response_data["slider_value_engine_left"] = recalculated_engine_left
        if anchor_value != "slider_engine_right":
            response_data["slider_value_engine_right"] = recalculated_engine_right
        if anchor_value != "slider_speed":
            response_data["slider_value_speed"] = (recalculated_engine_left + recalculated_engine_right) / 2
        if anchor_value != "slider_direction":
            response_data["slider_value_direction"] = (recalculated_engine_left - recalculated_engine_right) / 2
