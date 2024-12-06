import logging
import re
import subprocess
from datetime import datetime, timedelta
import requests
import pyudev
from functools import partial
import threading
import time
import socketio


import click
from typing import TYPE_CHECKING, Literal

from models import UsbPorts, Servers
from utils.utils import generate_usb_name_string, update_config

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

from commands import handle_work

logger = logging.getLogger(__name__)

sio = socketio.Client()


@click.group(name="usb")
def usb_cli():
    """Группа команд для работы с USB-портами"""
    pass

@usb_cli.group(name="port")
@click.argument('virtual_port')
@click.pass_context
def port_cli(ctx, virtual_port):
    """Группа команд для работы с USB-портом"""
    ctx.obj['PORT'] = virtual_port

@port_cli.command()
@handle_work
def show(ctx, session):
    """Показать информацию о USB-порте"""
    virtual_port = ctx.obj.get('PORT')
    click.echo(virtual_port)

@port_cli.command()
@handle_work
@click.option('--name', '-n', type=click.STRING, help="Set USB-port name")
@click.option('--bus', '-b', type=click.STRING, help="Set USB-port bus")
@click.option('--server', '-s', type=click.STRING, help="Set USB-port server name")
def conf(ctx, session, name, bus, server):
    """Настроить USB-порт"""
    virtual_port = ctx.obj.get('PORT')
    usb_port = session.query(UsbPorts).filter_by(virtual_port=virtual_port).first()
    if name:
        usb_port.name = name
    if bus:
        usb_port.bus = bus
    if server is not None:
        if server == "":
            usb_port.server_id = None

        else:
            server_bd = session.query(Servers).filter_by(name=server).first()

            if not server_bd:
                raise ValueError(f"Server {server} not found")
            usb_port.server_id = server_bd.id

    usb_ports = session.query(UsbPorts).all()
    usb_names = generate_usb_name_string(usb_ports)

    update_config("DEFAULT", "usb_names", usb_names)

    click.echo(virtual_port)

@port_cli.command()
@handle_work
def delete(ctx, session):
    """Удалить USB-порт"""
    virtual_port = ctx.obj.get('PORT')
    click.echo(virtual_port)

@port_cli.command()
@handle_work
def add(ctx, session):
    """Добавить USB-порт"""
    virtual_port = ctx.obj.get('PORT')
    click.echo(virtual_port)

@port_cli.group(name='power')
def port_cli_power():
    """Управление питанием USB-порта"""
    pass

@port_cli_power.command(name='on')
@handle_work
def port_cli_power_on(ctx, session: 'Session'):
    virtual_port = ctx.obj.get('PORT')
    usb_port = session.query(UsbPorts).filter_by(virtual_port=virtual_port).first()
    if usb_port:
        change_usb_power("on", usb_port.bus)
        usb_port.active = True
        click.echo(f"Питание {virtual_port} включено")
    else:
        raise FileNotFoundError(f"USB-port {virtual_port} doesnt exist!")

@port_cli_power.command(name='off')
@handle_work
def port_cli_power_off(ctx, session: 'Session'):
    virtual_port = ctx.obj.get('PORT')
    usb_port = session.query(UsbPorts).filter_by(virtual_port=virtual_port).first()
    if usb_port:
        change_usb_power("off", usb_port.bus)
        try:
            subprocess.run(
                [ "udevadm", "trigger", "--action=remove", f"/sys/bus/usb/devices/{usb_port.bus}/" ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
        except:
            click.secho(f"Ошибка при очистке старой информации модулем udevadm. Вероятнее всего порт уже выключен.", fg="red")
        usb_port.active = False
        click.echo(f"Питание {virtual_port} включено")
    else:
        raise FileNotFoundError(f"USB-port {virtual_port} doesnt exist!")

@port_cli_power.command(name='restart')
@handle_work
def port_cli_power_restart(ctx, session: 'Session'):
    virtual_port = ctx.obj.get('PORT')
    usb_port = session.query(UsbPorts).filter_by(virtual_port=virtual_port).first()
    if usb_port:
        change_usb_power("off", usb_port.bus)
        try:
            subprocess.run(
                [ "udevadm", "trigger", "--action=remove", f"/sys/bus/usb/devices/{usb_port.bus}/" ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
        except:
            click.secho(f"Ошибка при очистке старой информации модулем udevadm. Вероятнее всего порт уже выключен.",
                        fg="red")

        time.sleep(2)
        change_usb_power("on", usb_port.bus)
        usb_port.active = True
        click.echo(f"Питание {virtual_port} включено")
    else:
        raise FileNotFoundError(f"USB-port {virtual_port} doesnt exist!")


def change_usb_power(state: Literal["on", "off", "cycle"], bus):
    location, port = bus.rsplit('.', 1)[ 0 ], bus.rsplit('.', 1)[ 1 ]


    try:
        result = subprocess.run(
            [ "uhubctl", "-f", "-l", location, "-p", port, "-a", str(state) ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        click.echo(f"Результат для {location}, порт {port}:\n{result.stdout}")

    except subprocess.CalledProcessError as e:
        print(f"Ошибка выполнения команды, код возврата: {e.returncode}")
        print("Ошибка:", e.stderr)

    except Exception as e:
        print(f"Произошла ошибка: {e}")

@usb_cli.group(name="show")
@handle_work
def global_show(ctx, session):
    """Show all USB-ports"""
    pass

@usb_cli.group(name="conf")
@click.pass_context
def global_conf(ctx):
    """Global configuration"""
    pass

@usb_cli.group(name='monitoring-new')
def monitoring_new():
    """Управление мониторингом ошибок USB-портов"""
    pass


@monitoring_new.command(name='start')
@handle_work
def monitoring_new_start(ctx, session: "Session"):
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='usb')  # Отслеживать только события USB
    callback_with_session = partial(usb_event_callback, session=session)
    observer = pyudev.MonitorObserver(monitor, callback=callback_with_session)
    observer.start()

    try:
        sio.connect('http://localhost:5001', namespaces=[ '/USB_NEW' ])  # Замените URL на адрес вашего сервера
        print(f"Клиент подключен к пространству {sio.connection_namespaces}")
        while True:
            time.sleep(1)  # Поддерживать поток активным
    except:
        sio.disconnect()
        observer.stop()

# Обработчик подключения
@sio.event
def connect():
    print("Подключен к серверу")

# Обработчик отключения
@sio.event
def disconnect():
    print("Отключен от сервера")

def send_message(message):
    sio.emit('message', message, namespace='/USB_NEW')

def usb_event_callback(device, session: "Session"):
    if device.action == "bind":
        if device.device_node:
            usb_db = session.query(UsbPorts).filter_by(bus=device.get('DEVPATH').rsplit('/', 1)[-1]).first()
            if usb_db:
                usb_data = {
                    'virtual_port': usb_db.virtual_port,
                    'bus': usb_db.bus,
                    'device': f"{device.get('ID_VENDOR_FROM_DATABASE', device.get('ID_VENDOR'))}, {device.get('ID_MODEL_FROM_DATABASE', device.get('ID_MODEL'))}",
                }
            else:
                usb_data = {
                    'virtual_port': '',
                    'bus': usb_db.bus,
                    'device': {
                        'vendor': device.get('ID_VENDOR_FROM_DATABASE', device.get('ID_VENDOR')),
                        'model': device.get('ID_MODEL_FROM_DATABASE', device.get('ID_MODEL')),
                    }
                }

            send_message(usb_data)
            print(f"Устройство: {device.device_node}")
            print(f"  Data: {usb_data}")
            print(f"  Шина (BUS): {device.get('DEVPATH').rsplit('/', 1)[-1]}")
            print(f"  Полный путь: {device.get('DEVPATH')}")
            print(f"  Производитель: {device.get('ID_VENDOR_FROM_DATABASE', device.get('ID_VENDOR'))}")
            print(f"  Модель: {device.get('ID_MODEL_FROM_DATABASE', device.get('ID_MODEL'))}")
            print(f"  Серийный номер: {device.get('ID_SERIAL')}")
            print("-" * 40)



@usb_cli.group(name='monitoring-errors')
def monitoring_errors():
    """Управление мониторингом ошибок USB-портов"""
    pass

@monitoring_errors.command(name='start')
@handle_work
def monitoring_error_start(ctx, session: "Session"):
    last_check_time = datetime.now()  # Начальная метка времени
    while True:
        # Форматируем метку времени для dmesg (через минуту от времени последней проверки)
        start_time = (last_check_time - timedelta(seconds=11)).strftime("%Y-%m-%d %H:%M:%S")

        # Запуск мониторинга с параметром --since для получения логов
        monitor_dmesg_since(start_time)

        # Обновляем время последней проверки
        last_check_time = datetime.now()

        time.sleep(10)

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
            for usb in usb_ports:
                print(f"Detected error with usb: {usb}")

            # URL для PUT запроса
            url = "http://localhost:5000/api/v2/errors"

            # Данные для отправки
            data = {
                "usb-ports": [ {"bus": bus} for bus in usb_ports ]  # Используем правильное имя поля с дефисом
            }

            # Заголовки
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }

            # Выполняем PUT запрос
            response = requests.put(url, json=data, headers=headers)
            print("An attempt to send information to the server")
            if response.status_code == 200:
                print(f"Actual errors from server: {response.json()}")
            else:
                print(f"Error: {response.status_code}, {response.text}")


    except Exception as e:
        print(f"Ошибка при попытке отслеживания dmesg: {e}")
