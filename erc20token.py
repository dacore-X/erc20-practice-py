from web3 import Web3
from web3.eth import Contract
from web3.exceptions import ContractLogicError

from typing import Union
from web3.types import Wei
from types_eth import AddressLike, ChecksumAddress
from util import _load_abi
from exceptions import Web3InstanceRequired


class ERC20Token:
    """
    Represents ERC20 Token with default functions
    """
    __contractAddress: ChecksumAddress
    __symbol: str = None
    __name: str = None
    __decimals: int = None
    __totalSupply: Wei = None

    # Instance of Web3 to interact with contracts
    w3: Web3 = None

    # Instance of ETH Contract for Web3 calls
    contract: Contract = None

    # Token conctructor with Contract instance
    def __init__(self, contractAddress: Union[AddressLike, str], w3: Web3):
        if not Web3.isChecksumAddress(contractAddress):
            contractAddress = Web3.toChecksumAddress(contractAddress)

        if w3:
            self.w3 = w3
        else:
            raise Web3InstanceRequired

        # Read ERC20 ABI from file
        abi = _load_abi('erc20')

        # Setting an instance of w3.eth.contract
        self.contract: Contract = w3.eth.contract(address=contractAddress, abi=abi)

        # Setting contract address for Class attribute __contractAddress
        self.__contractAddress = contractAddress

    def __repr__(self) -> str:
        return f'ERC20 Object: {self.__contractAddress}, {self.__symbol}, {self.__name}, {self.__decimals}, {self.__totalSupply}'

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
    def totalSupply(self) -> Wei:
        if not self.__totalSupply:
            try:
                totalSupply = self.contract.functions.totalSupply().call()
            except ContractLogicError as e:
                raise e

            if not self.__decimals:
                self.__decimals = self.decimals

            totalSupply = totalSupply / (10 ** self.__decimals)
            self.__totalSupply = totalSupply

            return totalSupply
        return self.__totalSupply

    def setAllOptions(self):
        if not self.__symbol:
            self.__symbol = self.symbol

        if not self.__name:
            self.__name = self.name

        if not self.__decimals:
            self.__decimals = self.decimals

        if not self.__totalSupply:
            self.__totalSupply = self.totalSupply
