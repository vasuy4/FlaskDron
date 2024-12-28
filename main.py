from flask_server import app, auto_update
from arduino_communication import auto_get_vals_sensors
from threading import Thread

if __name__ == "__main__":
    thread_auto_update = Thread(target=auto_update)  # создание потока отправки буфера
    thread_auto_update.start()

    thread_get_vals_sensors = Thread(target=auto_get_vals_sensors)  # создание потока автообновления значений датчиков
    thread_get_vals_sensors.start()

    app.run(debug=True)
    thread_auto_update.join()
    thread_get_vals_sensors.join()