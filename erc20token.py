import time

from web3 import Web3
from web3.contract import ContractFunction
from web3.eth import Contract
from web3.exceptions import ContractLogicError

from typing import Union, Optional
from types_eth import AddressLike, ChecksumAddress

from util import _load_abi, _load_cfg
from exceptions import Web3InstanceRequired


class ERC20Token:
    """
    Represents ERC20 Token with default functions
    """
    __contractAddress: ChecksumAddress
    __symbol: str = None
    __name: str = None
    __decimals: int = None
    __totalSupply: float = None

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
    def totalSupply(self) -> float:
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

    # Setting all Call values by interacting contract
    def set_all_options(self):
        if not self.__symbol:
            self.__symbol = self.symbol

        if not self.__name:
            self.__name = self.name

        if not self.__decimals:
            self.__decimals = self.decimals

        if not self.__totalSupply:
            self.__totalSupply = self.totalSupply

    # ****************** Approve function call ******************
    def _is_approved(self, account: AddressLike, spender: AddressLike) -> bool:
        isApproved: bool = False

        amountAllowed: int = self.contract.functions.allowance(account, spender).call()
        if amountAllowed > 0:
            isApproved = True

        return isApproved

    def approve(self, account: AddressLike, spender: AddressLike) -> bool:
        if self._is_approved(account, spender):
            print(f'{"-"*30}\n'
                  f'✔ [APPROVED] Token: {self.contractAddress}\n'
                  f'From: {account}\n'
                  f'For: {spender}\n'
                  f'{"-"*30}')

            return True

        max_approve_amount = Web3.toWei(2**64-1, 'ether')
        nonce = self.w3.eth.getTransactionCount(account)

        function: ContractFunction = self.contract.functions.approve(spender, max_approve_amount)

        tx = function.buildTransaction(
            {
                'chainId': 42,
                'from': account,
                'nonce': nonce
            }
        )

        pvkey = _load_cfg()['WEB3']['PVKEY']
        signed_tx = self.w3.eth.account.signTransaction(tx, pvkey)


        tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, 30000)

        if receipt['status'] == 1:

            # Maybe using in the future
            # resp = {
            #     'tx_hash': tx_hash.hex(),
            #     'to': receipt['to'],
            #     'gasUsed': receipt['gasUsed']
            # }

            # Console logs
            print(f"{'-'*30}\n"
                  f"✔ [APPROVED] Token: {self.contractAddress}\n"
                  f"tx_hash: {tx_hash.hex()}\n"
                  f"to: {receipt['to']}\n"
                  f"gasUsed: {receipt['gasUsed']}\n"
                  f"{'-'*30}")

            # Wait some time cause of
            # ValueError: {'code': -32010, 'message': 'Transaction nonce is too low. Try incrementing the nonce.'}
            # calling this method one after the other
            # TODO: How to fix it correctly
            time.sleep(1)
            return True

        else:
            print(f"{'-'*30}\n"
                  f"✖ [ERROR APPROVING] Token: {self.contractAddress}\n"
                  f"tx_hash: {tx_hash.hex()}\n"
                  f"{'-'*30}")
            return False
        
    # ****************** Tranfer function call ******************
    def transfer(self, to: ChecksumAddress, amount: float) -> bool:

        if not Web3.isChecksumAddress(to):
            to = Web3.toChecksumAddress(to)

        # Load pvkey from .cfg file
        pvkey = _load_cfg()['WEB3']['PVKEY']
        
        account = self.w3.eth.account.privateKeyToAccount(pvkey)
        account_address = account.address
        nonce = self.w3.eth.getTransactionCount(account_address)

        amount: int = int(amount * 10 ** self.decimals)

        function: ContractFunction = self.contract.functions.transfer(to, amount)

        # Estimate gas logic
        estimate_gas: int = function.estimateGas({'from': account_address}) + 3000  # extra 3k gas

        tx = function.buildTransaction(
            {
                'chainId': 42,
                'from': account_address,
                'nonce': nonce,
                'gas': estimate_gas
            }
        )

        signed_tx = self.w3.eth.account.signTransaction(tx, pvkey)

        tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, 30000)

        if receipt['status'] == 1:

            # Console logs
            print(f"{'-' * 30}\n"
                  f"✔ [SENT] Token: {self.contractAddress}\n"
                  f"tx_hash: {tx_hash.hex()}\n"
                  f"gasUsed: {receipt['gasUsed']}\n"
                  f"{'-' * 30}")

            return True

        else:
            print(f"{'-' * 30}\n"
                  f"✖ [ERROR TRANSFER] Token: {self.contractAddress}\n"
                  f"tx_hash: {tx_hash.hex()}\n"
                  f"{receipt}\n"
                  f"{'-' * 30}")
            return False