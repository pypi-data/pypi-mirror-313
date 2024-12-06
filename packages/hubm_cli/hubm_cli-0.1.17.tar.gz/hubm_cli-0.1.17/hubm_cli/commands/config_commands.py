import configparser
# from . import handle_work
import logging
import re
import subprocess
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import TYPE_CHECKING
import requests

import click

from commands import handle_work
from hubm_cli import hubm_path

from models import UsbPorts

from utils.utils import generate_usb_name_string

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


@click.group(name="config")
@click.pass_context
def config_cli(ctx):
    """Группа команд для настройки."""
    ctx.ensure_object(dict)  # Инициализация контекста как словаря


#@handle_work
@config_cli.command()
@click.option('--driver', default='postgresql', show_default=True, help="Драйвер для подключения к базе данных.", prompt = ("Введите driver"))
@click.option('--user', default='psql_user', show_default=True, help="Пользователь для подключения к базе данных.", prompt = ("Введите пользователя"))
@click.option('--password', default='irRaWUjZQ2bo9pwS7qA7', show_default=True, help="Пароль для подключения к базе данных.", prompt = ("Введите пароль"))
@click.option('--address', default='localhost', show_default=True, help="Адрес для подключения к базе данных.", prompt = ("Введите адрес"))
@click.option('--port', default='5432', type=click.IntRange(20,65535), show_default=True, help="TCP-порт для подключения к базе данных.", prompt = ("Введите порт"))
@click.option('--db-name', default='usbhub_db', show_default=True, help="Название базы данных для подключения к базе данных.", prompt = ("Введите название базы данных"))
@handle_work
def init(ctx, session: "Session", driver, user, password, address, port, db_name):
    """Первичная настройка"""
    base_path = Path("/etc/hubm")
    config = configparser.ConfigParser()
    dirs_to_create = ['groups', 'logs']
    for dir_name in dirs_to_create:
        dir_path = base_path / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        if ctx.obj['DEBUG']:
            click.secho(f'Папка {dir_path} успешно создана.', fg='green')

    usb_ports = session.query(UsbPorts).all()
    usb_names = generate_usb_name_string(usb_ports)

    config[ 'DEFAULT' ] = {
        'db_url': f'{driver}://{user}:{password}@{address}:{port}/{db_name}',
        'usb_names': usb_names,
    }

    if ctx.obj[ 'DEBUG' ]:
        click.secho(f"Сгенерирован файл конфигурации:", fg='green')
#        for section in config.sections():
#            click.secho(f"[{section}]", fg='green')
#            for key, value in config.items(section):
#                click.secho(f"{key}: {value}", fg='green')
#            # Если у вас нет других секций, выводите значения из DEFAULT
        click.secho("[DEFAULT]", fg="yellow")
        for key, value in config[ 'DEFAULT' ].items():
            click.secho(f"{key} = {value}", fg='yellow')

    config_path = base_path / "config.ini"
    with open(config_path, 'w') as configfile:
        config.write(configfile)
    if ctx.obj[ 'DEBUG' ]:
        click.secho(f"Конфигурационный файл '{config_path}' успешно создан!", fg='green')


    create_systemd_unit_usb_error()



def create_systemd_unit_usb_error():

    unit_content = f"""[Unit]
Description=hubM unit for monitoring USB errors
After=network.target

[Service]
ExecStart=hubm-cli usb monitoring-errors start
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
    unit_path = Path("/etc/systemd/system") / f"hubm-monitoring-usb-errors.service"

    try:
        # Создаем unit-файл
        unit_path.write_text(unit_content, encoding="utf-8")
        print(f"Unit-файл {unit_path} успешно создан.")

        # Перезагружаем systemd
        subprocess.run([ "systemctl", "daemon-reload" ], check=True)
        print("Systemd daemon перезагружен.")

        # Включаем юнит для автозапуска
        subprocess.run([ "systemctl", "enable", f"hubm-monitoring-usb-errors.service" ], check=True)
        print(f"Юнит {unit_path.name} включён для автозапуска.")

        subprocess.run([ "systemctl", "start", f"hubm-monitoring-usb-errors.service" ], check=True)
        print(f"Юнит {unit_path.name} запущен.")

    except PermissionError:
        print("Ошибка: требуется выполнить скрипт с правами администратора для записи в /etc/systemd/system.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды: {e}")
    except Exception as e:
        print(f"Произошла неожиданная ошибка: {e}")
