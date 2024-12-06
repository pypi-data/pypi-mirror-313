import re
import subprocess
import time
from datetime import datetime, timedelta
import requests
import json

# Регулярное выражение для извлечения USB порта
usb_pattern = re.compile(r'usb (\S+):')

def monitor_dmesg_since(start_time):
    """Функция для мониторинга новых записей dmesg начиная с последнего времени."""
    try:
        # Запуск dmesg с параметром --since для фильтрации по времени
        process = subprocess.Popen(['sudo', 'dmesg', '-T', '--since', start_time], stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, text=True)

        # Чтение вывода dmesg
        line = process.stdout.readline()
        usb_ports = set()
        while line:
            # Проверяем наличие сообщения "device not accepting address"
            if "device not accepting address" in line.lower():
                # Ищем USB порт с помощью регулярного выражения
                match = usb_pattern.search(line)
                if match:
                    usb_port = match.group(1)
                    usb_ports.add(usb_port)
            line = process.stdout.readline()

        if usb_ports:

            # URL для PUT запроса
            url = "http://localhost:5000/api/v2/errors"

            # Данные для отправки
            data = {
                "usb-ports": list(usb_ports)  # Используем правильное имя поля с дефисом
            }
            print(data)

            # Заголовки
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }

            # Выполняем PUT запрос
            response = requests.put(url, json=data, headers=headers)

            if response.status_code == 200:
                print(f"Ответ от сервера: {response.json()}")
            else:
                print(f"Ошибка запроса: {response.status_code}, {response.text}")


    except Exception as e:
        print(f"Ошибка при попытке отслеживания dmesg: {e}")

def start_monitoring():
    """Запуск мониторинга каждую минуту."""
    last_check_time = datetime.now()  # Начальная метка времени
    while True:
        # Форматируем метку времени для dmesg (через минуту от времени последней проверки)
        start_time = (last_check_time - timedelta(seconds=11)).strftime("%Y-%m-%d %H:%M:%S")

        # Запуск мониторинга с параметром --since для получения логов
        monitor_dmesg_since(start_time)

        # Обновляем время последней проверки
        last_check_time = datetime.now()

        time.sleep(10)

if __name__ == "__main__":
    start_monitoring()
