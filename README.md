# HANA NETWORK - HANAFUDA BATCH DEPOSIT

Hana, incubated by Binance Labs, has launched a campaign that allows you to earn points by depositing assets, collecting cards, and growing your garden.

[TELEGRAM CHANNEL](https://t.me/Deeplchain) | [CONTACT](https://t.me/imspecials)

# REGISTER
- Website: https://hanafuda.hana.network
- Access code: `YOJQE9`

To participate:
1. Sign up using a Google & use invite code
2. Deposit assets on Base, or Arbitrum
3. Collect cards by clicking on Draw Hanafuda
4. Collect points by clicking on Grow
5. Invite friends to grow your garden

NOTE: Make first deposit `MANUALY` on Base in a Small Amount like <= $0.5 - $1

# Feature
 - Asynchronous execution for handling multiple transactions concurrently.
 - Customizable deposit amounts with minimum and maximum thresholds.
 - Automatic nonce management to prevent transaction failures.
 - Logs transaction details and errors for monitoring purposes.
 - MultiAccount support [BATCH PROCESS] 

## Requirements

- Python 3.7 or higher
- Web3.py
- Colorama

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/nadirasaid8/hanafuda.git
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
    "rpc_url": "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID",
    "amount_min": 0.0000000001,
    "amount_max": 0.000000001,
    "delay": 1
}
   ```

Replace `YOUR_INFURA_PROJECT_ID` with your actual Infura project ID or another Ethereum node provider URL.
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

## Auto Grow Tap a Card
The script below will help you to tap cards on Grow, you only need to enter the script below on the Grow pages console.

- Open https://hanafuda.hana.network/grow
- Press F12 to open the console
- Copy and paste the following script:

```yaml
let count = 0;
function clickElements() {
    if (count < 1000) {
        function clickElement(selector, buttonName) {
            const element = document.querySelector(selector);
            if (element) {
                element.click();
                console.log(`Clicked ${buttonName}`);
            } else {
                console.log(`${buttonName} not found`);
            }
        }

        const selector1 = 'body > div > div > div:nth-child(3) > div > div.relative.z-10.grid.size-full.flex-1.grid-cols-1.grid-rows-\\[20\\%_60\\%_20\\%\\].content-center.items-center.justify-center.justify-items-center.p-6 > div.relative.flex.size-full.flex-col.items-center.justify-center > div > div > canvas';
        const selector2 = 'body > div > div > div:nth-child(3) > div > div.relative.z-10.grid.size-full.flex-1.grid-cols-1.grid-rows-\\[20\\%_60\\%_20\\%\\].content-center.items-center.justify-center.justify-items-center.p-6 > div.relative.flex.w-full.items-center.justify-center.gap-1\\.5.lg\\:gap-3 > button.flex.cursor-pointer.items-center.justify-center.font-medium.tracking-\\[0\\.24px\\].disabled\\:cursor-default.shiny-button-color-red.shiny-button.h-\\[57px\\].w-\\[224px\\].rounded-\\[8px\\].text-\\[12px\\].max-w-\\[128px\\].gap-1\\.5.sm\\:gap-3.lg\\:w-\\[224px\\].lg\\:max-w-full';

        // Click the first element
        clickElement(selector1, 'button 1');

        setTimeout(() => {
            clickElement(selector2, 'button 2');
            count++; // Increment the counter variable after each round
            setTimeout(clickElements, 3000);
        }, 5000);
    }
}

clickElements();
```

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