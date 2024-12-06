import logging
import sys
from functools import wraps

import click
import sqlalchemy.exc

from database import Session


class ExitCode:
    SUCCESS = 0              # Успешное завершение
    GENERAL_ERROR = 1        # Общая ошибка
    CONFIG_ERROR = 2         # Ошибка конфигурации
    DB_CONNECTION_ERROR = 3  # Ошибка подключения к базе данных
    NOT_FOUND_ERROR = 4      # Объект не найден
    VALIDATION_ERROR = 5     # Ошибка валидации данных
    PERMISSION_ERROR = 6     # Ошибка доступа
    UNKNOWN_ERROR = 99       # Неизвестная ошибка

logger = logging.getLogger(__name__)

class Group:
    def __init__(self, name, tcp_port, usb_ports: [], ignored_buses, device_nicknames):
        self.name = name
        self.tcp_port = tcp_port
        self.usb_ports = usb_ports
        self.ignored_buses = ignored_buses
        self.device_nicknames = device_nicknames

    def __repr__(self):
        usb_details = "\n".join(
            f"  - Name: {usb.name}, Virtual Port: {usb.virtual_port}, Bus: {usb.bus}"
            for usb in self.usb_ports
        ) or "  None"
        return (f"Server: {self.name}\n"
                f"TCP port: {self.tcp_port}\n"
                f"USB ports: \n{usb_details}")


def handle_work(func):
    """Декоратор для обработки ошибок и возврата кодов завершения, управлением сессии БД, логированием."""
    @wraps(func)
    @click.pass_context
    def wrapper(ctx, *args, **kwargs):
        session = Session()
        debug_mode = ctx.obj.get("DEBUG")
        if debug_mode:
            click.secho("Сессия БД открыта.", fg="yellow")
        try:
            func(ctx, *args, **kwargs, session=session)
            if debug_mode:
                click.secho("Операция успешно завершена.", fg="green")
            session.commit()
            sys.exit(ExitCode.SUCCESS)
        except sqlalchemy.exc.IntegrityError as e:
            click.secho(f"Ошибка валидации данных: {e}", fg="red")
            logger.log(logging.ERROR, f"Error in {func.__name__}: Validation error {str(e)}", exc_info=True)
            session.rollback()
            sys.exit(ExitCode.VALIDATION_ERROR)
        except ValueError as e:
            click.secho(f"Ошибка валидации данных: {e}", fg="red")
            logger.log(logging.ERROR, f"Error in {func.__name__}: Validation error {str(e)}", exc_info=True)
            session.rollback()
            sys.exit(ExitCode.VALIDATION_ERROR)
        except ConnectionError as e:
            click.secho(f"Ошибка подключения к базе данных: {e}", fg="red")
            logger.log(logging.ERROR, f"Error in {func.__name__}: Database connection error {str(e)}", exc_info=True)
            session.rollback()
            sys.exit(ExitCode.DB_CONNECTION_ERROR)
        except FileNotFoundError as e:
            click.secho(f"Объект не найден: {e}", fg="red")
            logger.log(logging.WARNING, f"Error in {func.__name__}: Object not found {str(e)}", exc_info=True)
            session.rollback()
            sys.exit(ExitCode.NOT_FOUND_ERROR)
        except PermissionError as e:
            click.secho(f"Ошибка доступа: {e}", fg="red")
            logger.log(logging.ERROR, f"Error in {func.__name__}: Permission error {str(e)}", exc_info=True)
            session.rollback()
            sys.exit(ExitCode.PERMISSION_ERROR)
        except Exception as e:
            click.secho(f"Неизвестная ошибка: {e}", fg="red")
            logger.log(logging.CRITICAL, f"Error in {func.__name__}: Unknown error {str(e)}", exc_info=True)
            session.rollback()
            sys.exit(ExitCode.UNKNOWN_ERROR)
        finally:
            session.close()
            if debug_mode:
                click.secho("Сессия БД закрыта.", fg="yellow")

    return wrapper


from .group_commands import group_cli
from .user_commands import user_cli
from .usb_commands import usb_cli
from .config_commands import config_cli
from .general_commands import general_cli

__all__ = ['group_cli', 'user_cli', 'config_cli', 'usb_cli', 'general_cli']
