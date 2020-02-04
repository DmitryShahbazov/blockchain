import os
import json
import hashlib
from blockchain import config


def get_filename():
    files = os.listdir(config.Data.get('blocks_directory'))
    files = sorted([int(i) for i in files])
    print(files)
    filename = str(files[-1] + 1)
    print(filename)
    return filename


def create_block(data, filename):
    with open(config.Data.get('blocks_directory') + filename, 'w') as file:
        json.dump(data, file, indent=4)


def create_data():
    data = {
        "nickname": "",
        "payment_id": "",
        "amount": "",
        "pay_to": "",
        "payment_time": "",
        "success": "",
        "hash": ""
    }
    create_block(data, get_filename())


create_data()