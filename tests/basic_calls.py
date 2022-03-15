from erc20token import ERC20Token
from web3 import Web3, HTTPProvider
from util import _load_cfg
from types_eth import AddressLike, ChecksumAddress
from typing import Union


PROVIDER = _load_cfg()["WEB3"]["PROVIDER"]
w3 = Web3(HTTPProvider(PROVIDER))

TEST_TOKENS = [
    # KOVAN TOKENS
    '0x13512979ADE267AB5100878E2e0f485B568328a4',  # USDT
    '0xe22da380ee6B445bb8273C81944ADEB6E8450422',  # USDC
    # '0x4F96Fe3b7A6Cf9725f59d353F723c1bDb64CA6Aa',  # DAI
    '0xFf795577d9AC8bD7D90Ee22b6C1703490b6512FD',  # DAI AUGMENTED
    '0xa36085F69e2889c224210F603D836748e7dC0088',  # LINK
    # '0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984',  # UNI ERROR! METAMASK ASK TO SIGN
    '0xB347b9f5B56b431B2CF4e1d90a5995f7519ca792',  # POLYMATH
    '0xc011a73ee8576fb46f5e1c5751ca3b9fe0af2a6f',  # SNX

    # MAINNET TOKENS
    # '0xdAC17F958D2ee523a2206206994597C13D831ec7',  # USDT
    # '0x6B3595068778DD592e39A122f4f5a5cF09C90fE2',  # SUSHI
    # '0x514910771AF9Ca656af840dff83E8264EcF986CA',  # LINK
    # '0x75231F58b43240C9718Dd58B4967c5114342a86c',  # OKB
    # '0x4a220E6096B25EADb88358cb44068A3248254675',  # QNT
    # '0xc00e94Cb662C3520282E6f5717214004A7f26888'  # COMP
]


def test_basic_call(token: Union[AddressLike, str]):
    token = ERC20Token(token, w3)
    token.set_all_options()
    # print(token)


def test_approve_token(token: Union[AddressLike, str]):
    token = ERC20Token(token, w3)
    address = Web3.toChecksumAddress('0x8e014480A46d937d1BB851FbEbf26e78f35Ff3b3')
    spender = Web3.toChecksumAddress('0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D')
    response = token.approve(address, spender)
    # print(response)


def test_transfer_token(token: Union[AddressLike, str], to: Union[AddressLike, str], amount: float):
    token = ERC20Token(token, w3)
    to = Web3.toChecksumAddress(to)
    response = token.transfer(to, amount)
    # print(response)


for TOKEN in TEST_TOKENS:
    # test_basic_call(TOKEN)
    # test_approve_token(TOKEN)
    # test_transfer_token(TOKEN, '0x0b209139eaddbe99ffcd2a08cb45b92aca902833', 100)
    pass

