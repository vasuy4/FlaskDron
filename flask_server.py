from arduino_communication import send_command
from flask import Flask, render_template, request, jsonify
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
    "RENGINE": [90, time.time(), True]
}


def auto_update() -> None:
    """
    Поток автоматической отправки команд на ардуино каждые 0.5 секунды
    """
    while True:
        for command, value in BUFFER.items():
            if not value[2] and time.time() - value[1] > 0.5:
                send_command("{}_{}".format(command, value[0]))
        time.sleep(0.5)


@app.route("/")
def main_menu():
    return render_template("index.html")


@app.route("/update_slider", methods=["POST"])
def update_slider():
    slider_servo = request.json.get("slider_servo")
    slider_engine_left = request.json.get("slider_engine_left")
    slider_engine_right = request.json.get("slider_engine_right")

    # Здесь можно добавить логику для обработки значений слайдеров, например, проверку диапазона

    response_data = {}
    if slider_servo is not None:
        response_data['slider_value_servo'] = slider_servo
        value_angle: int = min(max(int(slider_servo) + 90, 10), 179)
        BUFFER["SERVO"][0] = value_angle
        BUFFER["SERVO"][2] = False
        # send_command("SERVO_{}".format(value_angle))
    if slider_engine_left is not None:
        response_data['slider_value_engine_left'] = slider_engine_left
    if slider_engine_right is not None:
        response_data['slider_value_engine_right'] = slider_engine_right

    return jsonify(response_data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')