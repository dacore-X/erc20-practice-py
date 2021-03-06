import json
import os
import configparser


def _load_abi(abi_file):
    path = f"{os.path.dirname(os.path.abspath(__file__))}/abi/"
    try:
        with open(os.path.abspath(path + f"{abi_file}.json")) as f:
            abi: str = json.load(f)
    except FileNotFoundError as e:
        raise e

    return abi


def _load_cfg():
    path = f"{os.path.dirname(os.path.abspath(__file__))}/.cfg"

    try:
        with open(os.path.abspath(path)) as f:
            config = configparser.ConfigParser()
            config.read(path)
    except FileNotFoundError as e:
        raise

    return config
