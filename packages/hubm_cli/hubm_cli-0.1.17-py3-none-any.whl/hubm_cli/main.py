import configparser
import logging
import sys, os
from pathlib import Path

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import click
from commands import config_cli, user_cli, usb_cli, group_cli, general_cli


# Настройка логгера для CLI
def setup_logging(log_level=logging.INFO, log_file=None):
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.setLevel(log_level)
    return logger


logger = setup_logging()


@click.group()
@click.option('--debug', is_flag=True, help="Включить режим отладки.")
@click.option('--log-file', type=click.Path(), help="Файл для сохранения логов.")
@click.pass_context
def cli(ctx, debug, log_file):
    """
    Основная точка входа CLI. Используйте --help для справки.
    """
    ctx.ensure_object(dict)
    ctx.obj['DEBUG'] = debug # Сохраняем значение параметра `name` в контексте
    if debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Режим отладки включен")

    if log_file:
        setup_logging(log_level=logging.DEBUG if debug else logging.INFO, log_file=log_file)



# Добавление команд
cli.add_command(group_cli)
cli.add_command(usb_cli)
cli.add_command(user_cli)
cli.add_command(config_cli)
cli.add_command(general_cli)

# Запуск CLI
def main():
    base_path = Path("/etc/hubm")
    base_path.mkdir(parents=True, exist_ok=True)
    config_path = base_path / "config.ini"
    config = configparser.ConfigParser()
    if not config_path.exists():
        config[ 'DEFAULT' ] = {
            'db_url': ""
        }
        with open(config_path, 'w') as file:
            config.write(file)

    cli(obj={})

if __name__ == '__main__':
    main()
