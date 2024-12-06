import pyudev
import threading
import time

def monitor_usb_events():
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='usb')  # Отслеживать только события USB
    observer = pyudev.MonitorObserver(monitor, callback=usb_event_callback)
    observer.start()
    try:
        while True:
            time.sleep(1)  # Поддерживать поток активным
    except KeyboardInterrupt:
        observer.stop()

def usb_event_callback(device):
    if device.action == "bind":
        print(f"Устройство: {device.device_node}")
        print(f"  Шина (BUS): {device.get('DEVPATH').rsplit('/', 1)[-1]}")
        print(f"  Полный путь: {device.get('DEVPATH')}")
        print(f"  Производитель: {device.get('ID_VENDOR')} ({device.get('ID_VENDOR_FROM_DATABASE')})")
        print(f"  Модель: {device.get('ID_MODEL')} ({device.get('ID_MODEL_FROM_DATABASE')})")
        print(f"  Серийный номер: {device.get('ID_SERIAL')}")
        print("-" * 40)

if __name__ == "__main__":
    print("Запуск мониторинга USB-устройств...")
    usb_thread = threading.Thread(target=monitor_usb_events, daemon=True)
    usb_thread.start()

    try:
        while True:
            time.sleep(1)  # Основной поток остается активным
    except KeyboardInterrupt:
        print("Мониторинг остановлен.")
