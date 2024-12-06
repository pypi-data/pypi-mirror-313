import logging
import subprocess
import sys
import click
from pathlib import Path
from hubm_cli import hubm_path

from models import Servers, UsbPorts
from utils.utils import update_group_config, read_config
from . import handle_work, Group

logger = logging.getLogger(__name__)

#@handle_work
@click.group(name="group")
@click.argument("group_name")
@click.pass_context
def group_cli(ctx, group_name):
    """Группа команд для работы с группами."""
    ctx.obj['NAME'] = group_name  # Сохраняем значение параметра `name` в контексте




@handle_work
@group_cli.command()
@click.option('--name', help="Название группы.")
def start(name):
    """Приветствие пользователя с учетом возраста."""
    try:
        subprocess.run([ "HUB-CORE", "-b", "-c", "/usr/local/etc/virtualhere/groups/Test.ini"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info(f"Приветствие отправлено для пользователя: {name}, возраст: ")
        sys.exit()
    except Exception as e:
        logger.critical(e)
        sys.exit(1)


@group_cli.command()
@click.confirmation_option(prompt="Are you sure? Group will be reconfigured with selected params and restarted.")
@handle_work
@click.option('--usb', '-u', type=click.STRING, multiple=True, help="Virtual USB-порт. Может задаваться несколько раз.")
@click.option('--usb-action', type=click.Choice(['set','add','remove']), default='add', show_default=True, help="TCP-порт для подключения к базе данных.")
def conf(ctx, session, usb, usb_action):
    """Crонфигурировать сервер"""
    name = ctx.obj.get('NAME')  # Получаем значение `name` из контекста

    server = session.query(Servers).filter_by(name=name).first()
    if server is None:
        raise FileNotFoundError(f"Группа '{name}' не найдена.")


    if usb_action == "remove":
        for virtual_port in usb:
            port = session.query(UsbPorts).filter_by(virtual_port=virtual_port).first()
            if port is None:
                raise ValueError(f"USB with virtual port '{virtual_port}' doesnt exist ")
            if port.server_id == server.id:
                server.usb_ports.remove(port)
            else:
                raise ValueError(f"Server '{name}' doesnt have usb with virtual port {virtual_port}.'")
    elif usb_action == "add":
        for virtual_port in usb:
            port = session.query(UsbPorts).filter_by(virtual_port=virtual_port).first()
            if port is None:
                raise ValueError(f"USB with virtual port '{virtual_port}' doesnt exist ")
            if port.server_id is None or port.server_id == server.id:
                server.usb_ports.append(port)
            else:
                raise ValueError(f"USB with virtual port '{virtual_port}' already claimed.")
    elif usb_action == "set":
        new_ports = []
        for virtual_port in usb:
            port = session.query(UsbPorts).filter_by(virtual_port=virtual_port).first()
            if port is None:
                raise ValueError(f"USB with virtual port '{virtual_port}' doesnt exist ")
            if port.server_id is None or port.server_id == server.id:
                new_ports.append(port)
            else:
                raise ValueError(f"USB with virtual port '{virtual_port}' already claimed.")
        server.usb_ports = new_ports

    usb_ports_all_raw = session.query(UsbPorts.bus).all()
    usb_ports_all_buses = [ name[ 0 ] for name in usb_ports_all_raw ]


    usb_ports_not = list(set(usb_ports_all_buses) - set(usb.bus for usb in server.usb_ports))
    ignored_buses = ','.join(usb_ports_not)
    device_nicknames = read_config("DEFAULT", "usb_names")

    group = Group(server.name, server.tcp_port, server.usb_ports, ignored_buses, device_nicknames)

    create_group_conf(group)
    create_systemd_unit(group.name)
    click.secho(group)



@group_cli.command()
@handle_work
def show(ctx, session):
    """Текущая конфигурация сервера"""
    name = ctx.obj.get('NAME')  # Получаем значение `name` из контекста

    server = session.query(Servers).filter_by(name=name).first()
    if server is None:
        raise FileNotFoundError(f"Сервер '{name}' не найден.")

    group = Group(server.name, server.tcp_port, server.usb_ports
                  )
    click.secho(group)

def create_group_conf(group):
    conf = f"""
License=03d40274-0435-0549-2506-820700080009,0,MCACDhf5Fve1ROuGyx8tA5OlAg4ypJivw6hytRlYUz5arA==
ControlTimeout=3
ClaimPorts=0
AutoAttachToKernel=0
CompressionLimit=384
UseAVAHI=0
onServerRename=/usr/local/etc/virtualhere/2.sh
onChangeNickname=/usr/local/etc/virtualhere/2.sh
HostName={group.name}
ServerName={group.name}
TCPPort={group.tcp_port}
#clientAuthorization=/usr/local/etc/virtualhere/auth_test2.py "$VENDOR_ID$" "$PRODUCT_ID$" "$CLIENT_ID$" "$CLIENT_IP$" "$PRODUCT_SERIAL$" "$PASSWORD$" "$DEVPATH$" "$NICKNAME$"
#clientAuthorization=/usr/local/etc/virtualhere/auth.sh "$VENDOR_ID$" "$PRODUCT_ID$" "$CLIENT_ID$" "$CLIENT_IP$" "$PRODUCT_SERIAL$" "$PASSWORD$" "$DEVPATH$" "$NICKNAME$" {group.name}
onDeviceKick=/usr/local/etc/virtualhere/onDeviceKick.sh "$VENDOR_ID$" "$PRODUCT_ID$" "$KICKER_ID$" "$KICKER_IP$" "$CLIENT_ID$" "$CLIENT_IP$" "$PRODUCT_SERIAL$" "$DEVPATH$" {group.name}
DeviceNicknames={group.device_nicknames}
IgnoredBuses={group.ignored_buses}
"""
    path = Path(hubm_path) / f"groups/{group.name}.ini"

    try:
        # Создаем unit-файл
        path.write_text(conf, encoding="utf-8")
        print(f"Конфиг-файл {path} успешно создан.")

    except PermissionError:
        print("Ошибка: требуется выполнить скрипт с правами администратора для записи в /etc/systemd/system.")
    except Exception as e:
        print(f"Произошла неожиданная ошибка: {e}")

def create_systemd_unit(group):

    unit_content = f"""[Unit]
Description=hubM unit for group {group}
After=network.target

[Service]
ExecStart=HUB-CORE -c {hubm_path}/groups/{group}.ini
WorkingDirectory=/etc/hubm
Restart=on-failure
RestartSec=5s
StartLimitIntervalSec=500
StartLimitBurst=5
TimeoutStopSec=50
KillMode=mixed

[Install]
WantedBy=multi-user.target
"""
    unit_path = Path("/etc/systemd/system") / f"hubm-group-{group}.service"

    try:
        # Создаем unit-файл
        unit_path.write_text(unit_content, encoding="utf-8")
        print(f"Unit-файл {unit_path} успешно создан.")

        # Перезагружаем systemd
        subprocess.run([ "systemctl", "daemon-reload" ], check=True)
        print("Systemd daemon перезагружен.")

        # Включаем юнит для автозапуска
        #subprocess.run([ "systemctl", "enable", f"hubm-group-{group}.service" ], check=True)
        #print(f"Юнит {unit_path.name} включён для автозапуска.")

    except PermissionError:
        print("Ошибка: требуется выполнить скрипт с правами администратора для записи в /etc/systemd/system.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды: {e}")
    except Exception as e:
        print(f"Произошла неожиданная ошибка: {e}")