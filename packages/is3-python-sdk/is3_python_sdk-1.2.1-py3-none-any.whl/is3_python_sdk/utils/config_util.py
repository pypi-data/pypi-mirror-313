import configparser
import logging
import os
import sys

from ..utils.logger import Logging

Logging()


# def get_header(filePath, key):
#     # 上传的文件路径
#     key_config = load_config(filePath)[key]
#     headers = {
#         'Content-Type': 'application/json',
#         'X-Access-Key': key_config.get('X-Access-Key', ''),
#         'X-Secret-Key': key_config.get('X-Secret-Key', '')
#     }
#     return headers


# def get_server_name(filePath, key):
#     key_config = load_config(filePath)[key]
#     serverName = key_config.get('plugin-code', '')
#     return serverName


# def get_property(filePath, key, pro):
#     key_config = load_config(filePath)[key]
#     value = key_config.get(pro)
#     return value


def load_config(configPath):
    config_path = os.path.join(configPath)

    # 确认文件存在
    if os.path.exists(config_path):
        # 读取配置文件
        config = configparser.ConfigParser()
        with open(config_path, 'r', encoding='utf-8') as f:  # 指定编码为 UTF-8
            config.read_file(f)
        return config
    else:
        logging.error(f"Config file does not exist at: {config_path}")
        sys.exit("1")
