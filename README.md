# HANA NETWORK - Auto Deposit / Grows / Gardens

Hana, incubated by Binance Labs, has launched a campaign that allows you to earn points by depositing assets, collecting cards, and growing your garden.

[TELEGRAM CHANNEL](https://t.me/airdropbombnode)

# REGISTER
- Website: https://hanafuda.hana.network
- Access code: `OO514V`

To participate:
1. Sign up using a Google & use invite code
2. Deposit assets on Base, or Arbitrum
3. Collect cards by clicking on Draw Hanafuda
4. Collect points by clicking on Grow
5. Invite friends to grow your garden

NOTE: Make first deposit `MANUALY` on Base in a Small Amount like <= $0.5 - $1

# Feature
 - Auto `Grow` & `Garden` Actions [ Updated : 2024/10/31 ] with `tokens.txt`
 - Asynchronous execution for handling `multiple transactions` concurrently.
 - Customizable deposit amounts with `minimum` and `maximum` thresholds.
 - Automatic `nonce management` to prevent transaction failures.
 - Logs transaction `details` and `errors` for monitoring purposes.
 - MultiAccount support `BATCH PROCESS`

## Requirements

- Python 3.7 or higher
- Web3.py
- Colorama

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/airdropbomb/hanafuda.git
   cd hanafuda
   ```
   
Install the required packages:

You can use pip to install the required dependencies:

   ```bash
pip install web3 colorama
   ```
## Configuration:

Create a config.json file in the root directory with the following structure:

   ```json
{
    "rpc_url": "https://mainnet.base.org",
    "amount_min": 0.0000000001,
    "amount_max": 0.000000001,
    "delay": 2,
    "countdown_before_start": 10
}
   ```

Replace `rpc_url` with your actual Infura project ID or another Ethereum node provider URL.
Adjust `amount_min`, `amount_max`, and `delay` according to your requirements.

### Private Keys:
Create a `privkey.txt` file containing your Ethereum private keys, one per line:

   ```txt
your_private_key_1
your_private_key_2
   ```

#### Contract ABI:

Place your contract's ABI JSON file in the src/ directory and name it `contract_abi.json`.

## Usage
Run the bot using the following command:

   ```bash
python main.py
   ```

### Input Parameters
The bot will prompt you to enter the number of deposit transactions to be executed.
You can specify which accounts to use by entering their indices or type all to use all available accounts.

Example
   ```python
Enter the number of deposit to be executed: 2
Enter the account numbers to use (e.g., 0,2,4 for accounts 1,3,5 or 'all' for all accounts): all
   ```

## Grow / Garden (how to get tokens)

- Open https://hanafuda.hana.network/
- Press `F12` / `Inspect Element` to open the console
- Go to `Applications` & `Session Storage`
- Choose the link of hanafuda network then choose `Key` : firbase:authUser
- on Value of `stsTokenManager: {,...} 
- Take the Value of refreshToken: start with `AMf-`
- Paste it to `tokens.txt`

### Logging
All transaction details will be logged into a file named hash.log, including any errors encountered during execution.

### Error Handling
The bot includes error handling for common issues such as:

1. Insufficient funds for transactions.
2. Nonce issues due to concurrent transactions.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Disclaimer
Use this bot at your own risk. Always test with small amounts before executing larger transactions.

## Contact
For any questions or issues, please open an issue on GitHub or contact me at [ https://t.me/DeeplChain ]
