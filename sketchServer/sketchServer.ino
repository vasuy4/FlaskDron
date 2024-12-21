#include <SPI.h>
#include <Ethernet.h>
#include <Servo.h>

// MAC-адрес вашего Ethernet Shield (можно использовать любой)
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };

// Создаем объект для работы с сервоприводом
Servo myServo;
Servo myServo2;

// Создаем объект для работы с Ethernet
EthernetServer server(80);

const int neutralPosition = 90;
const int minInputAngle = -45;
const int maxInputAngle = 45;

void setup() {
  // Инициализируем сервопривод и подключаем его к пину 9
  myServo.attach(9);
  myServo2.attach(6);

  // Инициализируем Ethernet Shield с использованием DHCP
  if (Ethernet.begin(mac) == 0) {
    Serial.println("Failed to configure Ethernet using DHCP");
    // Если DHCP не удалось, можно использовать статический IP-адрес
    // Ethernet.begin(mac, IPAddress(192, 168, 1, 177));
  } else {
    Serial.print("DHCP assigned IP: ");
    Serial.println(Ethernet.localIP());
  }

  // Запускаем сервер
  server.begin();

  // Выводим IP-адрес сервера в монитор порта
  Serial.begin(9600);
  Serial.print("Server is at ");
  Serial.println(Ethernet.localIP());
}

void loop() {
  // Ожидаем подключения клиента
  EthernetClient client = server.available();
  if (client) {
    Serial.println("New client");

    while (client.connected()) {
      if (client.available()) {
        String command = client.readStringUntil('\n'); // Чтение команды до конца строки
        Serial.print("Получена команда: ");
        Serial.println(command);

        // Находим позицию символа подчеркивания
        size_t underscorePos = command.indexOf('_');
        if (underscorePos != -1) {
          // Извлекаем подстроку до символа подчеркивания
          String prefix = command.substring(0, underscorePos);
          // Извлекаем подстроку после символа подчеркивания и преобразуем в целое число
          int value = atoi(command.substring(underscorePos + 1).c_str());

          if (prefix == "SERVO") {
            setBothServos(value);
            Serial.print("Set angle to: ");
            Serial.println(value);
            client.print(command);
          } else if (prefix == "LENGINE") {
            // Код для левого двигателя
            client.print(command);
          } else if (prefix == "RENGINE") {
            // Код для правого сервопривода
            client.print(command);
          } else if (prefix == "GETSENSDATA") {
            // Код для получения данных с датчиков
            client.print("Data-temp_Data-depth");
          } else {
            client.print("Unknown command");
          }
        }
      }
    }

    // Закрываем соединение
    delay(1);
    client.stop();
    Serial.println("Client disconnected");
  }
}

void setBothServos(int inputAngle) {
  if (inputAngle < minInputAngle) {
    inputAngle = minInputAngle;
  } else if (inputAngle > maxInputAngle) {
    inputAngle = maxInputAngle;
  }

  int servoAngle = neutralPosition + inputAngle;
  servoAngle = constrain(servoAngle, 0, 180);

  myServo.write(servoAngle);
  myServo2.write(servoAngle);
}