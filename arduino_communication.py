from config import arduino_ip, arduino_port
import socket


def send_command(command: str) -> str:
    # Подключение к Arduino
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((arduino_ip, arduino_port))
        s.sendall(command.encode())  # Отправляем команду
        response = s.recv(1024).decode()  # Получаем ответ
        return response


if __name__ == '__main__':
    request: str = send_command("LSERVO_10\n")
    print(request)