import time
import socket

from typing import Dict

from config import arduino_ip, arduino_port


BUFFER_SENSORS: Dict[str, float] = {
    "temperature": 0,
    "pressure": 0,
    "depth": 0
}


def send_command(command: str) -> str:
    """
    Отправление команды на ардуино
    :param command: команда
    :return: ответ от ардуино
    """
    # Подключение к Arduino
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((arduino_ip, arduino_port))
        s.sendall(command.encode())  # Отправляем команду
        response = s.recv(1024).decode()  # Получаем ответ
        return response


def auto_get_vals_sensors() -> None:
    """
    Отдельный поток получения данных с датчиков
    """
    density: float = 1030  # плотность жидкости
    g: float = 9.81  # гравитационная постоянная
    while True:
        time.sleep(2)
        response: str = send_command("GETSENSDATA_0")
        # response: str = f"{random.randint(1, 100)}_{random.randint(1, 200000)}"
        temperature, pressure = response.split("_")
        temperature, pressure = float(temperature), float(pressure)
        depth: float = round(pressure / (density * g), 3)
        BUFFER_SENSORS["temperature"] = temperature
        BUFFER_SENSORS["pressure"] = pressure
        BUFFER_SENSORS["depth"] = depth


if __name__ == "__main__":
    request: str = send_command("SERVO_10\n")
    print(request)
