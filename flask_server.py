from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route("/")
def main_menu():
    return render_template("index.html")


@app.route("/update_slider", methods=["POST"])
def update_slider():
    slider_servo = request.json.get("slider_servo")
    slider_engine1 = request.json.get("slider_engine1")

    # Здесь можно добавить логику для обработки значений слайдеров, например, проверку диапазона

    response_data = {}
    if slider_servo is not None:
        response_data['slider_value_servo'] = slider_servo
    if slider_engine1 is not None:
        response_data['slider_value_engine1'] = slider_engine1

    return jsonify(response_data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')