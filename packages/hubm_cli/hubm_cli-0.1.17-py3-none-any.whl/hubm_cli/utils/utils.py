from pathlib import Path
from typing import Literal
import configparser
from typing import Any, Optional

base_path = Path("/etc/hubm")
config_path = base_path / "config.ini"

def read_config(section: str, option: str) -> Optional[ str ]:
    """
    Читает значение параметра из конфигурационного файла.

    :param file_path: Путь к файлу конфигурации.
    :param section: Название секции.
    :param option: Название параметра.
    :return: Значение параметра или None, если секция или параметр не найдены.
    """
    config = configparser.ConfigParser()
    config.read(config_path)

    try:
        if section == "DEFAULT":
            # Чтение из секции DEFAULT
            return config[ "DEFAULT" ].get(option, None)
        else:
            # Проверяем наличие секции
            if config.has_section(section):
                return config.get(section, option, fallback=None)
            else:
                print(f"Секция '{section}' не найдена в файле '{config_path}'.")
                return None
    except configparser.NoOptionError:
        print(f"Параметр '{option}' не найден в секции '{section}'.")
        return None


def update_config(section: str, option: str, value: str) -> None:
    """
    Обновляет (или добавляет) значение параметра в конфигурационном файле.

    :param file_path: Путь к файлу конфигурации.
    :param section: Название секции.
    :param option: Название параметра.
    :param value: Новое значение параметра.
    """
    config = configparser.ConfigParser()
    config.read(config_path)

    if section == "DEFAULT":
        config[ "DEFAULT" ][ option ] = value
    else:
        if not config.has_section(section):
            config.add_section(section)
        config.set(section, option, value)

    with open(config_path, 'w') as config_file:
        config.write(config_file)


def read_group_config(filepath):
    """Чтение конфигурационного файла и сохранение его содержимого в словарь"""
    config = {}
    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()
            if '=' in line:
                key, value = line.split('=', 1)
                config[ key.strip() ] = value.strip()
    return config


def write_group_config(filepath, config):
    """Запись изменений обратно в конфигурационный файл"""
    with open(filepath, 'w') as file:
        for key, value in config.items():
            file.write(f"{key}={value}\n")


def update_group_config(filepath, key, value):
    """Обновление значения ключа в конфигурационном файле"""
    config = read_group_config(filepath)

    if key in config:
        config[ key ] = value
    else:
        print(f"Ключ '{key}' не найден. Добавляем новый ключ.")
        config[ key ] = value

    write_group_config(filepath, config)
    print(f"Ключ '{key}' обновлен на значение: {value}")


def get_config_value(filepath, key):
    """Получение значения для заданного ключа"""
    config = read_group_config(filepath)
    return config.get(key, None)


def add_to_list_group_config(filepath, key, value):
    """Добавление значения в список, если ключ уже существует (например, в IgnoredBuses)"""
    config = read_group_config(filepath)

    if key in config:
        existing_value = config[ key ]
        # Разделяем по запятой и добавляем новое значение
        values = existing_value.split(',')
        if value not in values:
            values.append(value)
            config[ key ] = ','.join(values)
        else:
            print(f"Значение '{value}' уже существует для ключа '{key}'.")
    else:
        print(f"Ключ '{key}' не найден. Добавляем новый ключ.")
        config[ key ] = value

    write_group_config(filepath, config)
    print(f"Значение '{value}' добавлено в ключ '{key}'.")


def generate_usb_name_string(usb_ports):
    usb_strings = [ ]
    for usb in usb_ports:
        name = usb.name
        bus = usb.bus.replace('.', '').replace('-', '')  # Убираем точки и тире
        usb_strings.append(f'{name},ffff,ffff,{bus}')

    return ','.join(usb_strings)