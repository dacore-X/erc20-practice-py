import configparser
import json

from web3 import Web3, HTTPProvider
from web3.eth import Contract
from web3.exceptions import ContractLogicError

from typing import Union
from types_eth import AddressLike, ChecksumAddress

config = configparser.ConfigParser()
config.read('.cfg')

PROVIDER = config["WEB3"]["PROVIDER"]
w3 = Web3(HTTPProvider(PROVIDER))


class ERC20Token:
    """
    Represents ERC20 Token with default functions
    """
    __contractAddress: ChecksumAddress
    __symbol: str = None
    __name: str = None
    __decimals: int = None
    __totalSupply: int = None

    # Instance of ETH Contract for Web3 calls
    contract: Contract

    # Token conctructor with Contract instance
    def __init__(self, contractAddress: Union[AddressLike, str]):
        if not Web3.isChecksumAddress(contractAddress):
            contractAddress = Web3.toChecksumAddress(contractAddress)

        # TODO: Is it good to read file with ABI in constructor
        # Read ERC20 ABI from file
        with open('abi/erc20.json') as f:
            ERC20_ABI = json.load(f)

        self.contract = w3.eth.contract(address=contractAddress, abi=ERC20_ABI)
        self.__contractAddress = contractAddress

    # Get contract of the token
    @property
    def contractAddress(self) -> ChecksumAddress:
        return self.__contractAddress

    # Get symbol of the token by interacting contract/reading value
    @property
    def symbol(self) -> str:
        if not self.__symbol:
            try:
                symbol = self.contract.functions.symbol().call()
            except ContractLogicError as e:
                raise e

            self.__symbol = symbol
            return symbol
        return self.__symbol

    # Get name of the token by interacting contract/reading value
    @property
    def name(self) -> str:
        if not self.__name:
            try:
                name = self.contract.functions.name().call()
            except ContractLogicError as e:
                raise e

            self.__name = name
            return name
        return self.__name

    # Get decimals of the token by interacting contract/reading value
    @property
    def decimals(self) -> int:
        if not self.__decimals:
            try:
                decimals = self.contract.functions.decimals().call()
            except ContractLogicError as e:
                raise e

            self.__decimals = decimals
            return decimals
        return self.__decimals

    # Get totalSupply of the token by interacting contract/reading value
    @property
    def totalSupply(self) -> int:
        if not self.__totalSupply:
            try:
                totalSupply = self.contract.functions.totalSupply().call()
            except ContractLogicError as e:
                raise e

            self.__totalSupply = totalSupply
            return totalSupply
        return self.__totalSupply


# Some tests
# Sensorium SENSO - 0xC19B6A4Ac7C7Cc24459F08984Bbd09664af17bD1 - doesn't return Decimals due contract specifics
# Uniswap Token - 0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984
Token_UNI = ERC20Token(contractAddress='0x1f9840a85d5af5bf1d1762f925bdaddc4201f984')

print(Token_UNI.contractAddress)
print(Token_UNI.name)
print(Token_UNI.symbol)
print(Token_UNI.decimals)
print(Token_UNI.totalSupply)
