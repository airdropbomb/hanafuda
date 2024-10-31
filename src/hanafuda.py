import sys
import json
import asyncio
import random
from colorama import *
from web3 import Web3
from datetime import datetime
from deeplchain import log, countdown_timer, _banner, _clear, htm, mrh, kng, hju, bru, pth

init(autoreset=True)

class Hanafuda:
    def __init__(self, config, private_keys):
        self.web3 = Web3(Web3.HTTPProvider(config['rpc_url']))
        self.contract_address = "0xC5bf05cD32a14BFfb705Fb37a9d218895187376c"
        self.private_keys = private_keys
        self.amount_min = config['amount_min']
        self.amount_max = config['amount_max']
        self.delay = config['delay']
        
        with open("src/contract_abi.json", "r") as abi_file:
            self.contract_abi = json.load(abi_file)

        self.contract = self.web3.eth.contract(address=self.contract_address, abi=self.contract_abi)
        self.nonces = {key: self.web3.eth.get_transaction_count(self.web3.eth.account.from_key(key).address) for key in self.private_keys}
        self.tx_count = {key: 0 for key in self.private_keys}

    def get_random_amount(self):
        return random.uniform(self.amount_min, self.amount_max)

    async def send_transaction(self, private_key, transaction_number):
        from_address = self.web3.eth.account.from_key(private_key).address
        short_from_address = from_address[:4] + "..." + from_address[-4:]
        amount = self.get_random_amount()
        amount_wei = self.web3.to_wei(amount, 'ether')

        try:
            balance = self.web3.eth.get_balance(from_address)
            tx_cost = amount_wei + (self.web3.eth.gas_price * 100000)

            if balance < tx_cost:
                log(mrh + f"Insufficient funds for {short_from_address}: balance {self.web3.from_wei(balance, 'ether'):.10f} ETH, tx cost {self.web3.from_wei(tx_cost, 'ether'):.10f} ETH")
                return

            transaction = self.contract.functions.depositETH().build_transaction({
                'from': from_address,
                'value': amount_wei,
                'gas': 100000,
                'gasPrice': self.web3.eth.gas_price,
                'nonce': self.nonces[private_key],
            })

            signed_txn = self.web3.eth.account.sign_transaction(transaction, private_key=private_key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_txn.raw_transaction)

            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open("hash.log", "a") as log_file:
                log_file.write(f"{timestamp} - SEND - ({short_from_address}) - https://basescan.org/tx/0x{tx_hash.hex()}\n")

            log(hju + f"Deposit {pth}{transaction_number} {hju}sent from {pth}{short_from_address} {hju}for {pth}{amount:.10f} {hju}ETH")

            self.nonces[private_key] += 1
            self.tx_count[private_key] += 1

            if self.tx_count[private_key] >= 50:
                self.tx_count[private_key] = 0

            await asyncio.sleep(self.delay)

        except Exception as e:
            if 'nonce too low' in str(e):
                log(mrh + f"Nonce too low for {short_from_address}. Fetching the latest nonce...")
                self.nonces[private_key] = self.web3.eth.get_transaction_count(from_address)
            elif 'insufficient funds' in str(e):
                log(mrh + f"Insufficient funds error for {short_from_address}: {str(e)}")
            else:
                log(mrh + f"Error sending transaction from {short_from_address}: {str(e)}")

        finally:
            await asyncio.sleep(1)


    async def main(self, num_deposit):
        tasks = []
        account_indices = input(Fore.YELLOW + "Enter the account numbers to use (e.g., 0,2,4 for accounts 1,3,5 or 'all' for all accounts): " + Style.RESET_ALL)
        selected_keys = []
        
        if account_indices.lower() == 'all':
            selected_keys = self.private_keys
        else:
            try:
                indices = [int(i.strip()) for i in account_indices.split(',')]
                selected_keys = [self.private_keys[i] for i in indices if i < len(self.private_keys)]
            except (ValueError, IndexError):
                log(mrh + "Invalid account selection. Please enter valid indices.")
                return

        if not selected_keys:
            log(mrh + "No valid accounts selected.")
            return

        for i in range(num_deposit):
            for private_key in selected_keys:
                tasks.append(self.send_transaction(private_key, i + 1))
        
        countdown_timer(5)
        log(htm + "~" * 38)
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    try:
        _clear()
        _banner()

        num_deposit = int(input(kng + "Enter the number of deposit to be executed: " + Style.RESET_ALL))

        with open("privkey.txt", "r") as file:
            private_keys = [line.strip() for line in file if line.strip()]

        eth_transaction = Hanafuda(config, private_keys)
        asyncio.run(eth_transaction.main(num_deposit))

        log(bru + f"Finished sending {num_deposit} deposit transactions for each account.")
    except KeyboardInterrupt as e:
        log(mrh + "Deposit transaction execution cancelled.")
        sys.exit()
