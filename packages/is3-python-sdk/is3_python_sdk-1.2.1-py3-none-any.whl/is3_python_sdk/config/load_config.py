import os

import yaml

'''加载local_config.yaml文件'''


def load_local_config():
    # python代码测试时候
    exe_dir = os.path.dirname(os.path.abspath(__file__))

    # 构造 local_config.yaml 的完整路径
    config_path = os.path.join(exe_dir, 'local_config.yaml')

    # 读取 YAML 文件，指定编码为 utf-8
    with open(config_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)

    return config
