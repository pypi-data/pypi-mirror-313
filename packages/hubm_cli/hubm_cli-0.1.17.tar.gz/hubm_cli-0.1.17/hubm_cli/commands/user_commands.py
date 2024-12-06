import logging

import click

logger = logging.getLogger(__name__)


@click.group(name="user")
def user_cli():
    """Группа команд для работы с пользователями."""
    pass

#@handle_errors()
@user_cli.command()
@click.option('--name', prompt='Ваше имя', help="Имя пользователя.")
@click.option('--age', prompt='Ваш возраст', type=int, help="Возраст пользователя.")
def greet(name, age):
    """Приветствие пользователя с учетом возраста."""
    if age < 18:
        click.secho(f"Привет, {name}! Ты молод!", fg="cyan")
    else:
        click.secho(f"Привет, {name}! Добро пожаловать!", fg="yellow")

    logger.info(f"Приветствие отправлено для пользователя: {name}, возраст: {age}")
