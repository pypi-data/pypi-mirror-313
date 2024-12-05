"""Fundlock Module."""

import requests
from web3 import Web3
from logger import logger


class Fundlock:
    """Fundlock Class."""

    def __init__(self, parent):
        """Class constructor."""
        self.parent = parent

    def __get_web3(self):
        return Web3(Web3.HTTPProvider(self.parent.rpc_url))

    def __sign_and_send(self, account, web3, txn):
        """Sign and send transaction."""
        txn = txn.build_transaction(
            {
                "gas": 700000,
                "gasPrice": web3.eth.gas_price,
                "nonce": web3.eth.get_transaction_count(account.address),
            }
        )
        signed_txn = web3.eth.account.sign_transaction(txn, private_key=account.key)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt

    def faucet(self, symbol, amount=None):
        """Get Dummy tokens for Testnet."""
        web3 = self.__get_web3()
        if self.parent.account is None:
            logger.error("ERROR: private key not passed. Cannot sign transactions")
            return None

        account = self.parent.account
        tokens = self.parent.protocol.system_info().get("payload").get("tokenAddress")
        if symbol not in tokens:
            logger.error("Invalid token")
            return
        else:
            token_address = web3.to_checksum_address(tokens.get(symbol))
        contract = web3.eth.contract(address=token_address, abi=erc20_abi)
        if amount is None:
            amount = 5000 * 1e6 if symbol == "USDC" else Web3.to_wei(500, "ether")

        txn = contract.functions.mint(account.address, int(amount))
        return self.__sign_and_send(account, web3, txn)

    def token_balances(self):
        """Get token balances."""
        web3 = self.__get_web3()
        if self.parent.account is None:
            logger.error("ERROR: private key not passed. Cannot sign transactions")
            return None

        account = self.parent.account
        tokens = self.parent.protocol.system_info().get("payload").get("tokenAddress")
        for symbol, address in tokens.items():
            contract = web3.eth.contract(
                address=web3.to_checksum_address(address), abi=erc20_abi
            )
            balance = contract.functions.balanceOf(account.address).call()
            decimals = contract.functions.decimals().call()
            logger.debug(symbol, balance / 10 ** (decimals))

    def fundlock_balances(self):
        """Get fundlock balances."""
        web3 = self.__get_web3()
        if self.parent.account is None:
            logger.error("ERROR: private key not passed. Cannot sign transactions")
            return None

        account = self.parent.account
        system = self.parent.protocol.system_info().get("payload")
        tokens = system.get("tokenAddress")
        fundlock_address = web3.to_checksum_address(system.get("fundlockAddress"))
        fundlock = web3.eth.contract(address=fundlock_address, abi=fundlock_abi)
        for symbol, token in tokens.items():
            balance = fundlock.functions.balanceSheet(
                account.address, web3.to_checksum_address(token)
            ).call()
            logger.debug(symbol, balance)

    def deposit(self, symbol, amount):
        """Deposit funds."""
        web3 = self.__get_web3()
        if self.parent.account is None:
            logger.error("ERROR: private key not passed. Cannot sign transactions")
            return None

        account = self.parent.account
        system = self.parent.protocol.system_info().get("payload")
        tokens = system.get("tokenAddress")
        fundlock_address = Web3.to_checksum_address(system.get("fundlockAddress"))
        if symbol not in tokens:
            logger.error("Invalid token")
            return
        else:
            token_address = web3.to_checksum_address(tokens.get(symbol))
        contract = web3.eth.contract(address=token_address, abi=erc20_abi)
        wallet_balance = contract.functions.balanceOf(account.address).call()
        if wallet_balance < amount:
            logger.error("Not enough balance...")
            return
        allowance = contract.functions.allowance(
            account.address, fundlock_address
        ).call()
        if amount > allowance:
            logger.info("Setting allowance...")
            txn = contract.functions.approve(fundlock_address, amount)
            self.__sign_and_send(account, web3, txn)
        fundlock = web3.eth.contract(address=fundlock_address, abi=fundlock_abi)
        txn = fundlock.functions.deposit(account.address, token_address, amount)
        tx = self.__sign_and_send(account, web3, txn)
        logger.info(tx)

    def withdraw(self, symbol, amount):
        """Withdraw funds."""
        web3 = self.__get_web3()
        if self.parent.account is None:
            logger.error("ERROR: private key not passed. Cannot sign transactions")
            return None

        account = self.parent.account
        system = self.parent.protocol.system_info().get("payload")
        tokens = system.get("tokenAddress")
        if symbol not in tokens:
            logger.error("Invalid token")
            return
        else:
            token_address = tokens.get(symbol)
        fundlock_address = web3.to_checksum_address(system.get("fundlockAddress"))
        fundlock = web3.eth.contract(address=fundlock_address, abi=fundlock_abi)
        txn = fundlock.functions.withdraw(token_address, amount)
        tx = self.__sign_and_send(account, web3, txn)
        logger.info(tx)

    def release(self, symbol, withdrawal_slot):
        """Release funds."""
        web3 = self.__get_web3()
        if self.parent.account is None:
            logger.error("ERROR: private key not passed. Cannot sign transactions")
            return None

        account = self.parent.account
        system = self.parent.protocol.system_info().get("payload")
        tokens = system.get("tokenAddress")
        if symbol not in tokens:
            logger.error("Invalid token")
            return
        else:
            token_address = tokens.get(symbol)
        fundlock_address = web3.to_checksum_address(system.get("fundlockAddress"))
        fundlock = web3.eth.contract(address=fundlock_address, abi=fundlock_abi)
        txn = fundlock.functions.release(token_address, withdrawal_slot)
        tx = self.__sign_and_send(account, web3, txn)
        logger.info(tx)

    def cross_chain_deposit(self):
        """Cross chain deposit."""
        return False

    def get_cross_chain_tx_status(self):
        """Get cross chain tx status."""
        return False

    def history(self):
        """Get fundlock movements history."""
        query = """query ($account: ID!){
                account(id: $account) {
                    deposits {
                        amount
                        token
                        blockTimestamp
                        transactionHash
                    }
                    withdrawalRequests {
                        amount
                        token
                        withdrawalSlot
                        blockTimestamp
                        transactionHash
                        deductions {
                            amount
                            blockTimestamp
                            transactionHash
                        }
                    }
                    releases {
                        amount
                        token
                        blockTimestamp
                        transactionHash
                        withdrawalRequest {
                            amount
                            withdrawalSlot
                            blockTimestamp
                            transactionHash
                            deductions {
                                amount
                                blockTimestamp
                                transactionHash
                            }
                        }
                    }
                }
            }"""

        response = requests.post(
            self.parent.subgraph_url,
            json={
                "query": query,
                "variables": {"account": self.parent.address},
            },
        )
        return response.json()


erc20_abi = [
    {
        "inputs": [
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
        ],
        "name": "mint",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "decimals",
        "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "spender", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
        ],
        "name": "approve",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "owner", "type": "address"},
            {"internalType": "address", "name": "spender", "type": "address"},
        ],
        "name": "allowance",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
]

fundlock_abi = [
    {
        "inputs": [
            {"internalType": "address", "name": "client", "type": "address"},
            {"internalType": "address", "name": "token", "type": "address"},
        ],
        "name": "balanceSheet",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "client", "type": "address"},
            {"internalType": "address", "name": "token", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
        ],
        "name": "deposit",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "client", "type": "address"},
            {"internalType": "address", "name": "token", "type": "address"},
            {"internalType": "uint8", "name": "index", "type": "uint8"},
        ],
        "name": "fundsToWithdraw",
        "outputs": [
            {"internalType": "uint256", "name": "value", "type": "uint256"},
            {"internalType": "uint32", "name": "timestamp", "type": "uint32"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "client", "type": "address"},
            {"internalType": "address", "name": "token", "type": "address"},
        ],
        "name": "fundsToWithdrawTotal",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "token", "type": "address"},
            {"internalType": "uint8", "name": "index", "type": "uint8"},
        ],
        "name": "release",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "releaseLock",
        "outputs": [{"internalType": "uint32", "name": "", "type": "uint32"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "tradeLock",
        "outputs": [{"internalType": "uint32", "name": "", "type": "uint32"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "token", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
        ],
        "name": "withdraw",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
]
