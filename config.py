import configparser
import json

config = configparser.ConfigParser()
config.read('config.ini')


class Config:
    token = config['TgKeys']['token']
    create_engine = config['Database']['create_engine']
    database_path = config['Database']['path']

    coin_name = "XLX"
    ref_fee = 10
    task_fee = 50


class RegEx:
    token = "^([0-9]{10})(:)([A-Za-z0-9-_]){35}$"


sub_list = json.load(open('data/sub_list.json', 'r', encoding='utf-8'))
bot_commands = json.load(open('data/bot_commands.json', 'r', encoding='utf-8'))
