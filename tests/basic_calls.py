import configparser

from erc20token import ERC20Token
from web3 import Web3, HTTPProvider
from util import _load_cfg
from types_eth import AddressLike
from typing import Union

config = configparser.ConfigParser()
config.read(_load_cfg())

PROVIDER = config["WEB3"]["PROVIDER"]
w3 = Web3(HTTPProvider(PROVIDER))

TEST_TOKENS = [
    '0x6B3595068778DD592e39A122f4f5a5cF09C90fE2',  # SUSHI
    '0x514910771AF9Ca656af840dff83E8264EcF986CA',  # LINK
    '0x75231F58b43240C9718Dd58B4967c5114342a86c',  # OKB
    '0x4a220E6096B25EADb88358cb44068A3248254675',  # QNT
    '0xc00e94Cb662C3520282E6f5717214004A7f26888'  # COMP
]


def test_basic_call(token: Union[AddressLike, str]):
    token = ERC20Token(token, w3)
    token.setAllOptions()
    print(token)


for TOKEN in TEST_TOKENS:
    test_basic_call(TOKEN)