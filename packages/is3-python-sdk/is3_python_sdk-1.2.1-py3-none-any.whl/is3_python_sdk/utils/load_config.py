import configparser
import logging
import os
import sys

import yaml

from ..utils.logger import Logging

Logging()


def load_config(configPath):
    config_path = os.path.join(configPath)

    # 确认文件存在
    if os.path.exists(config_path):
        pass
    else:
        logging.error(f"Config file does not exist at: {config_path}")
        sys.exit("1")

    # 读取配置文件
    config = configparser.ConfigParser()
    config.read(config_path)

    return config


'''读取exe同级配置'''


def load_exe_config():
    # 获取当前执行的 EXE 文件的目录
    exe_dir = os.path.dirname(os.path.abspath(sys.executable))

    # 构造 config.yaml 的完整路径
    config_path = os.path.join(exe_dir, 'config.yaml')

    # 读取 YAML 文件，指定编码为 utf-8
    with open(config_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)

    return config


def load_local_config():
    # python代码测试时候
    exe_dir = os.path.dirname(os.path.abspath(__file__))

    # 构造 config.yaml 的完整路径
    config_path = os.path.join(exe_dir, 'config.yaml')

    # 读取 YAML 文件，指定编码为 utf-8
    with open(config_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)

    return config
