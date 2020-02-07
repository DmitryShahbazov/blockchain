import sys
import os
import json
import logging as log
import hashlib
from blockchain import config
from datetime import datetime

log.basicConfig(stream=sys.stdout, level=log.DEBUG)


"""
Функция возвращающая имя нового блока
"""


def get_filename():
    files = os.listdir(config.Data.get('blocks_directory'))
    files = sorted([int(i) for i in files])
    filename = str(files[-1] + 1)
    return filename


"""
Функция возвращающая список всех файлов(блоков)
"""


def get_files():
    files = os.listdir(config.Data.get('blocks_directory'))
    files = sorted([int(i) for i in files])
    return files


"""
Проверям тип хэширования
! Сделать выбор хэша единственный раз за использование блокчейна !
"""


def check_hash_type(data):
    hash_type = config.Data.get('hash_type')
    if hash_type == 'md5':
        hash_result = hashlib.md5(data).hexdigest()
    elif hash_type == 'sha256':
        hash_result = hashlib.sha256(data).hexdigest()
    elif hash_type == 'sha512':
        hash_result = hashlib.sha512(data).hexdigest()
    else:
        hash_result = ''
        log.warning('Wrong hash type in config!')
    return hash_result


"""
Функция для хэширования новых блоков, принимает список файлов(блоков)
Берет из этого списка последний блок и хэширует его
Далее этот хэш добавляем в блок, который создаем
"""


def get_hash(files):
    last_file = str(files[-1])
    f = open(config.Data.get('blocks_directory') + last_file, 'rb')
    data = f.read()
    hash_result = check_hash_type(data)
    return hash_result


"""
Проверяем все блоки на изменения:
    Берем хэш блока (кроме генезис блока)
    Берем предыдущий блок, хэшируем его 
    Далее сравниваем хэши блоков, если было вмешательство в предыдущий блок, то хэши будут не совпадать
"""


def check_corruption(files):
    for i in range(len(files)):
        if i >= 1:
            try:
                with open(config.Data.get('blocks_directory') + str(files[i]), 'r') as file:
                    previous_hash = json.load(file)['previous_hash']
                print(previous_hash)
                prev_file = open(config.Data.get('blocks_directory') + str(files[i-1]), 'rb').read()
                prev_file = check_hash_type(prev_file)
                if prev_file != previous_hash:
                    log.critical(f'Data corrupted in {str(files[i-1])}')
            except IndexError:
                pass


"""
Основная функция для создания новых блоков, туда передаем данные из функции create_data и имя нового блока get_filename
"""


def create_block(data, filename):
    with open(config.Data.get('blocks_directory') + filename, 'w') as file:
        json.dump(data, file, indent=4)


def create_data():
    data = {
        "nickname": "Dmitry",
        "payment_id": "1",
        "amount": "100",
        "pay_to": "Mike",
        "payment_time": str(datetime.now()),
        "success": True,
        "previous_hash": str(get_hash(get_files()))
    }
    return data


"""
Вызываем функцию создания нового блока и одновременно проверяем на вмешательство
"""


create_block(create_data(), get_filename())
check_corruption(get_files())
