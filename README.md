# 1. Загрузите скетч ./sketchServer.ino в Arduino
С помощью Arduino IDE загрузить скетч в Arduino
# 2. Установите Python 3.12
Скачать Python: https://www.python.org/downloads/
# 3. Установите nodeJS v22.x.x
Скачать nodeJS: https://nodejs.org/en
# 4. Установка зависимостей
### 4.1 Установка зависимостей для python
cmd
```cmd
pip install Flask
```
### 4.2 Установка зависимостей для js
```cmd
npm install
```
# 5. Создание локальной сети
### 5.1 Отключите ПК от маршрутизатора (если подключены)
### 5.2 Подключите Arduino по Ethernet кабелю напрямую к ПК
### 5.3 Настройте сетевой интерфейс на ПК
- Установите статический IP-адрес для адаптера 192.168.1.1, с маской подсети 255.255.255.0
# 6. Запуск проекта через ./main.py
cmd
```cmd
python ./main.py
```

-----
### Заметки
- При изменении файла .js пересоберите проект
```cmd
npm run build
```
