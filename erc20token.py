import configparser
from web3 import Web3
from types_eth import AddressLike

config = configparser.ConfigParser()
config.read('.cfg')

PROVIDER = config["WEB3"]["PROVIDER"]
w3 = Web3.HTTPProvider(PROVIDER)


class ERC20Token:
    """
    Represents ERC20 Token with default functions
    """
    __contract: AddressLike
    __symbol: str = None
    __name: str = None
    __decimals: int = None
    __totalSupply: int = None

    # Token conctructor with contract
    def __init__(self, contract):
        self.__contract = contract

    # Get contract of the token
    @property
    def contract(self) -> AddressLike:
        return self.__contract

    # Get symbol of the token by interacting contract/reading value
    @property
    def symbol(self) -> str:
        if not self.__symbol:
            # Web3 get symbol from contract logic
            return 'ERC20'
        return self.__symbol

    # Get name of the token by interacting contract/reading value
    @property
    def name(self) -> str:
        if not self.__name:
            # Web3 get name from contract logic
            return 'ERC20'
        return self.__name

    # Get decimals of the token by interacting contract/reading value
    @property
    def decimals(self) -> int:
        if not self.__decimals:
            # Web3 get decimals from contract logic
            return 18
        return self.__decimals

    # Get totalSupply of the token by interacting contract/reading value
    @property
    def totalSupply(self) -> int:
        if not self.__totalSupply:
            # Web3 get Total Supply from contract logic
            return 10**18
        return self.__totalSupply


# Some tests
# Uniswap Token - 0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984
Token_UNI = ERC20Token(contract='0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984')
print(Token_UNI.contract)
print(Token_UNI.name)
print(Token_UNI.symbol)
print(Token_UNI.decimals)
print(Token_UNI.totalSupply)
