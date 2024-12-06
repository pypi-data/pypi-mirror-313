import logging
import subprocess
import sys
import click
import socketio
from pathlib import Path
from hubm_cli import hubm_path

from models import Servers, UsbPorts
from utils.utils import update_group_config, read_config
from . import handle_work, Group

logger = logging.getLogger(__name__)

sio = socketio.Server()

#@handle_work
@click.group(name="general")
def general_cli():
    """Группа команд для работы с глобальным функционалом."""


@general_cli.group(name='socketio')
def socketio():
    """Управление сервисом SocketIO"""
    pass

@socketio.command(name='start')
def socketio_start():
    from flask import Flask
    app = Flask(__name__)

    # Инициализация SocketIO с Flask
    socketio = SocketIO(app)

    # Обработчики событий для SocketIO
    @sio.event
    def connect(sid, environ):
        print(f"Client {sid} connected")

    @sio.event
    def disconnect(sid):
        print(f"Client {sid} disconnected")

    @sio.event
    def message(sid, data):
        print(f"Message from {sid}: {data}")
        sio.send(sid, "Hello from server!")

    app.run(port=5001)


