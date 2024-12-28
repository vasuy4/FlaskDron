#include <SPI.h>
#include <Ethernet.h>
#include <Servo.h>

// сигнал АЦП, (R резистора / R термистора), B термистора, t термистора, разрешение АЦП
float NTC_compute(float analog, float baseDiv, uint16_t B, uint8_t t = 25, uint8_t res = 10)
{
    if (analog <= 0 || isnan(analog)) return INFINITY;
    analog = baseDiv / ((float)((1 << res) - 1) / analog - 1.0f);
    analog = (log(analog) / B) + 1.0f / (t + 273.15f);
    return (1.0f / analog - 273.15f);
}

// сигнал АЦП, R резистора, B термистора, t термистора, R термистора, разрешение АЦП
float NTC_compute(float analog, uint32_t R, uint16_t B, uint8_t t = 25, uint32_t Rt = 10000, uint8_t res = 10)
{
    return NTC_compute(analog, (float)R / Rt, B, t, res);
}

class NTC 
{
   public:
    NTC() {}

    // пин, R резистора, B термистора, t термистора, R термистора, разрешение АЦП
    NTC(uint8_t pin, uint32_t R, uint16_t B, uint8_t t = 25, uint32_t Rt = 10000, uint8_t res = 10) 
    {
        config(R, B, t, Rt);
        setPin(pin, res);
    }

    // настроить термистор: R резистора, B термистора, t термистора, R термистора
    void config(uint32_t R, uint16_t B, uint8_t t = 25, uint32_t Rt = 10000) 
    {
        _beta = B;
        _tempBase = t;
        _baseDivRes = (float)R / Rt;
    }

    // настроить пин и разрешение АЦП
    void setPin(uint8_t pin, uint8_t res = 10) 
    {
        _pin = pin;
        _res = res;
    }

    // прочитать температуру с пина
    float getTemp() 
    {
        //Serial.println(analogRead(_pin));
        return computeTemp(analogRead(_pin), _res);
    }

    // прочитать усреднённую температуру с пина, можно указать к-во усреднений
    float getTempAverage(uint8_t samples = 20) 
    {
        uint16_t aver = 0;
        for (uint8_t i = 0; i < samples; i++) aver += analogRead(_pin);
        return computeTemp((float)aver / samples, _res);
    }

    // получить температуру из сигнала АЦП, можно указать разрешение АЦП
    float computeTemp(float analog, uint8_t res = 10) 
    {
        return NTC_compute(analog, _baseDivRes, _beta, _tempBase, res);
    }

   private:
    uint8_t _res = 10;
    uint8_t _pin = 0;
    uint16_t _beta = 3435;
    uint8_t _tempBase = 25;
    float _baseDivRes = 1.0;
};

NTC ntc(A0, 10000, 3950);

// MAC-адрес вашего Ethernet Shield (можно использовать любой)
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };

// Создаем объект для работы с сервоприводом
Servo myServoL;
Servo myServoR;

// Создаем переменные для моторов
Servo myESC_L, myESC_R;
int myESC_CurSpeedL = 89, 
    myESC_CurSpeedR = 89,
    myESC_TargetSpeedL = 180, 
    myESC_TargetSpeedR = 0;

// Создаем объект для работы с Ethernet
EthernetServer server(80);

void setup() {
  // Инициализируем сервопривод и подключаем его к пину 9
  myServoL.attach(8);
  myServoR.attach(9);

  // ESC моторы / пины 2 и 3
  myESC_L.attach(2);
  myESC_R.attach(3);

  // Устанавливаем в полную остановку
  myESC_L.write(89);
  myESC_R.write(89);
  
  Ethernet.begin(mac, IPAddress(192, 168, 1, 100));
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
          Serial.println(prefix);

          if (prefix == "SERVO") {
            myServoL.write(value);
            myServoR.write(value);
            client.print(command);
          } else if (prefix == "LSERVO") {
            myServoL.write(value);
            client.print(command);
          } else if (prefix == "RSERVO") {
            myServoR.write(value);
            client.print(command);
          } else if (prefix == "LENGINE") {
            myESC_TargetSpeedL = value;
            client.print(command);
          } else if (prefix == "RENGINE") {
            myESC_TargetSpeedR = value;
            client.print(command);
          } else if (prefix == "GETSENSDATA") {
            Serial.print("Temperature ");
            float tempAvg = ntc.getTempAverage();
            Serial.print(tempAvg);

            float valPress = analogRead(A1);
            float newton = 0.00005 * valPress * valPress * - valPress *  + 0.2162;
            float pascal = newton / 0.003848; // 0,003848 - площадь датчика
            String data = String(tempAvg)  + "_" + String(pascal);
            client.print(data);  // Data-temp_Data-depth
          } else {
            client.print("Unknown command");
          }
          while ((abs(myESC_TargetSpeedL - myESC_CurSpeedL) > 1) || 
                 (abs(myESC_TargetSpeedR - myESC_CurSpeedR) > 1)){
            delay(20);
            // ENGINE L Меняем скорость постепенно
            int buffDirection = myESC_TargetSpeedL - myESC_CurSpeedL;
            if(buffDirection < 0){
              myESC_CurSpeedL-=1;
            }else if(buffDirection > 0){
              myESC_CurSpeedL+=1;
            }
            // ENGINE R Меняем скорость постепенно
            buffDirection = myESC_TargetSpeedR - myESC_CurSpeedR;
            if(buffDirection < 0){
              myESC_CurSpeedR-=1;
            }else if(buffDirection > 0){
              myESC_CurSpeedR+=1;
            }
            Serial.println("Engines Cur Speed - L:" + String(myESC_CurSpeedL) + " | R:" + String(myESC_CurSpeedR));
            myESC_L.write(myESC_CurSpeedL);
            myESC_R.write(myESC_CurSpeedR);
          }
          
        } else {
          client.print("-1");
        }
      }
    }

    
    // Закрываем соединение
    delay(1);
    client.stop();
    Serial.println("Client disconnected");
  }
}