# Monad Testnet Automation Scripts

This repository contains a collection of Python scripts designed to automate various tasks on the Monad Testnet, including staking, swapping, deploying contracts, and sending transactions. The scripts are integrated with a central `main.py` file for easy navigation and execution, supporting multiple private keys and a user-friendly CLI interface.

## Features Overview

### General Features
- **Multi-Account Support**: Reads private keys from `pvkey.txt` to perform actions across multiple accounts.
- **Colorful CLI**: Uses `colorama` for visually appealing output with colored text and borders.
- **Asynchronous Execution**: Built with `asyncio` for efficient blockchain interactions (where applicable).
- **Error Handling**: Comprehensive error catching for blockchain transactions and RPC issues.

### 1. `main.py` - Main Menu
- **Description**: Acts as the central hub to select and run other scripts.
- **Features**:
  - Interactive menu with language selection (Vietnamese/English).
  - Supports running multiple scripts (`kitsu.py`, `bean.py`, `uniswap.py`, `deploy.py`, `sendtx.py`, `ambient.py`, `rubic.py`, `mono.py`, `apriori.py`, `bebop.py`, `izumi.py`, `magma.py`, `bima.py`, `lilchogstars.py`, `naddomains.py`).
  - Clean console interface with colorful banners and borders.
- **Usage**: Run `python main.py` and choose a script from the menu.

### 2. `kitsu.py` - Kitsu Staking
- **Description**: Automates staking and unstaking MON tokens on the Kitsu Staking contract.
- **Features**:
  - Supports multiple private keys from `pvkey.txt`.
  - Random staking amounts (0.01-0.05 MON).
  - Random delays (1-3 minutes) between actions.
  - Stake and unstake cycles with detailed transaction logging.
  - Bilingual output (Vietnamese/English).
- **Usage**: Select from `main.py` menu, input number of cycles.

### 3. `bean.py` - Bean Swap
- **Description**: Automates swapping between MON and tokens (USDC, USDT, BEAN, JAI) on Bean Swap.
- **Features**:
  - Supports multiple private keys from `pvkey.txt`.
  - Random swaps (MON → Token or Token → MON).
  - Configurable cycles and random delays (1-3 minutes).
  - Balance checking before and after swaps.
  - Detailed transaction logs with Tx Hash and explorer links.
- **Usage**: Select from `main.py` menu, input cycles.

### 4. `uniswap.py` - Uniswap Swap
- **Description**: Automates swapping between MON and tokens (DAC, USDT, WETH, MUK, USDC, CHOG) on Uniswap V2.
- **Features**:
  - Supports multiple private keys from `pvkey.txt`.
  - Random swaps (MON → Token or Token → MON).
  - Configurable cycles and random delays (1-3 minutes).
  - Balance checking before and after swaps.
  - Detailed transaction logs with Tx Hash and explorer links.
- **Usage**: Select from `main.py` menu, input cycles.

### 5. `deploy.py` - Contract Deployment
- **Description**: Deploys a simple Counter contract to Monad Testnet.
- **Features**:
  - Supports multiple private keys from `pvkey.txt`.
  - User input for contract name and symbol (e.g., "Thog Token", "THOG").
  - Configurable deployment cycles with random delays (4-6 seconds).
  - Displays contract address and Tx Hash after deployment.
  - Bilingual output (Vietnamese/English).
- **Usage**: Select from `main.py` menu, input cycles, then enter name and symbol for each deployment.

### 6. `sendtx.py` - Send Transactions
- **Description**: Sends MON transactions to random addresses or addresses from a file.
- **Features**:
  - Supports multiple private keys from `pvkey.txt`.
  - Two modes:
    - Send to random addresses (user-defined transaction count).
    - Send to addresses from `address.txt`.
  - Configurable MON amount (default 0.000001, max 999).
  - Random delays (1-3 seconds) between transactions.
  - Detailed logs including sender, receiver, amount, gas, block, and balance.
- **Usage**: Select from `main.py` menu, input transaction count, amount, and mode.

### 7. `ambient.py` - Ambient Swap Bot
- **Description**: Automates token swapping on the Ambient DEX.
- **Features**:
  - Random Swap: Performs random swaps between USDC, USDT, and WETH with customizable amounts.
  - Manual Swap: Allows users to select source/destination tokens and input amounts.
  - Balance Checking: Displays MON and token balances (USDC, USDT, WETH).
  - Retry Mechanism: Retries failed transactions up to 3 times with a 5-second delay for RPC errors.
  - Extended Deadline: Swap transactions have a 1-hour deadline to avoid "Swap Deadline" errors.
  - Interactive Menu: Offers a CLI menu to choose between Random Swap, Manual Swap, or Exit.
- **Usage**: Select from `main.py` menu, choose Random/Manual mode, and follow prompts.

### 8. `rubic.py` - Rubic Swap Script
- **Description**: Automates swapping MON to USDT via the Rubic router.
- **Features**:
  - Supports multiple private keys from `pvkey.txt`.
  - Configurable swap cycles with a fixed amount (0.01 MON).
  - Wraps MON to WMON, swaps WMON to USDT, then unwraps remaining WMON to MON.
  - Random delays (1-3 minutes) between cycles and accounts.
  - Transaction tracking with Tx Hash and explorer links.
- **Usage**: Select from `main.py` menu, input number of cycles.

### 9. `mono.py` - Monorail Transaction Script
- **Description**: Sends predefined transactions to the Monorail contract.
- **Features**:
  - Supports multiple private keys from `pvkey.txt`.
  - Sends 0.1 MON transactions with custom data.
  - Gas Estimation: Falls back to 500,000 if estimation fails.
  - Explorer Links: Provides transaction links for tracking.
  - Random delays (1-3 minutes) between accounts.
- **Usage**: Select from `main.py` menu, runs automatically for all accounts.

### 10. `apriori.py` - Apriori Staking
- **Description**: Automates staking, unstaking, and claiming MON on the Apriori Staking contract.
- **Features**:
  - Supports multiple private keys from `pvkey.txt`.
  - Random staking amounts (0.01-0.05 MON).
  - Configurable cycles with random delays (1-3 minutes) between actions.
  - Stake → Unstake → Claim sequence with API check for claimable status.
  - Detailed transaction logging with Tx Hash and explorer links.
  - Bilingual output (Vietnamese/English).
- **Usage**: Select from `main.py` menu, input number of cycles.

### 11. `bebop.py` - Bebop Wrap/Unwrap Script (Synchronous)
- **Description**: Wraps MON to WMON and unwraps WMON back to MON via the Bebop contract (synchronous version).
- **Features**:
  - Supports multiple private keys from `pvkey.txt`.
  - User-defined MON amounts (0.01-0.05) for wrapping/unwrapping.
  - Configurable cycles with random delays (1-3 minutes).
  - Transaction tracking with Tx Hash and explorer links.
  - Bilingual output (Vietnamese/English).
- **Usage**: Select from `main.py` menu, input number of cycles and MON amount.

### 12. `izumi.py` - Izumi Wrap/Unwrap Script (Asynchronous)
- **Description**: Wraps MON to WMON and unwraps WMON back to MON via the Izumi contract (asynchronous version).
- **Features**:
  - Supports multiple private keys from `pvkey.txt`.
  - Random wrap/unwrap amounts (0.01-0.05 MON).
  - Configurable cycles with random delays (1-3 minutes).
  - Transaction tracking with Tx Hash and explorer links.
  - Bilingual output (Vietnamese/English).
- **Usage**: Select from `main.py` menu, input number of cycles.

### 13. `magma.py` - Magma Staking
- **Description**: Automates staking MON and unstaking gMON on the Magma contract.
- **Features**:
  - Supports multiple private keys from `pvkey.txt`.
  - Random staking amounts (0.01-0.05 MON).
  - Configurable cycles with random delays (1-3 minutes) between stake/unstake.
  - Transaction tracking with Tx Hash and explorer links.
  - Bilingual output (Vietnamese/English).
- **Usage**: Select from `main.py` menu, input number of cycles.

### 14. `bima.py` - Bima Deposit
- **Description**: Automates depositing bmBTC into the Bima contract on Monad Testnet.
- **Features**:
  - Supports multiple private keys from `pvkey.txt`.
  - Random deposit amounts (0.01-0.05 bmBTC).
  - Random delays (1-3 minutes) between actions.
  - Transaction tracking with Tx Hash and explorer links.
  - Bilingual output (Vietnamese/English).
- **Usage**: Select from `main.py` menu, runs automatically for all accounts.

### 15. `lilchogstars.py` - Mint Lil Chogstars NFT
- **Description**: Automates minting Lil Chogstars NFTs on Monad Testnet.
- **Features**:
  - Supports multiple private keys from `pvkey.txt`.
  - Free NFT minting or random amounts if fees apply.
  - Random delays (1-3 minutes) between actions.
  - Transaction tracking with Tx Hash and explorer links.
  - Bilingual output (Vietnamese/English).
- **Usage**: Select from `main.py` menu, runs automatically for all accounts.

### 16. `naddomains.py` - NAD Domain Registration
- **Description**: Automates NAD domain registration on Monad Testnet.
- **Features**:
  - Supports multiple private keys from `pvkey.txt`.
  - Registers random domains (6-12 characters) or user-defined names.
  - Registration fees: 1 MON (3 characters), 0.3 MON (4 characters), 0.1 MON (5+ characters).
  - Checks MON balance and domain availability via API.
  - Random delays (10-30 seconds) between accounts.
  - Transaction tracking with Tx Hash and explorer links.
  - Bilingual output (Vietnamese/English).
- **Usage**: Select from `main.py` menu, input domain name (or leave blank for random).

## Setup Instructions:

- **Python Version**: Python 3.7 or higher (recommended 3.9 or 3.10 due to `asyncio` usage).
- **Installer**: `pip` (Python package installer).

## Installation
1. **Clone this repository:**
- Open cmd or Shell, then run the command:
```sh
git clone https://github.com/thog9/Monad-testnet.git
```
```sh
cd Monad-testnet
```
2. **Install Dependencies:**
- Open cmd or Shell, then run the command:
```sh
pip install -r requirements.txt
```
3. **Prepare Input Files:**
- Open the `pvkey.txt`: Add your private keys (one per line) in the root directory.
```sh
nano pvkey.txt 
```
- Open the `address.txt`(optional): Add recipient addresses (one per line) for `sendtx.py`.
```sh
nano address.txt 
```
4. **Run:**
- Open cmd or Shell, then run command:
```sh
python main.py
```
- Choose a language (Vietnamese/English).

## Troubleshooting:

- **Connection Errors**: Ensure `pvkey.txt` exists and contains valid private keys. Check internet connectivity and RPC URL responsiveness (`https://testnet-rpc.monad.xyz/`).

- **Library Errors**: Verify all required libraries are installed (`pip list`).
  
- **Transaction Failures**: Check Tx Hash on Monad Testnet Explorer for detailed error messages (e.g., "Swap Deadline", insufficient balance).

- **API Errors in `apriori.py`**: Ensure the API endpoint `https://liquid-staking-backend-prod-b332fbe9ccfe.herokuapp.com/` is accessible.

## File Structure:
```
├── main.py           # Main menu script
├── scripts/          # Directory containing all automation scripts
│   ├── kitsu.py      # Kitsu Staking automation
│   ├── bean.py       # Bean Swap automation
│   ├── uniswap.py    # Uniswap Swap automation
│   ├── deploy.py     # Contract deployment automation
│   ├── sendtx.py     # Transaction sending automation
│   ├── ambient.py    # Ambient Swap automation
│   ├── rubic.py      # Rubic Swap automation
│   ├── mono.py       # Monorail Transaction automation
│   ├── apriori.py    # Apriori Staking automation
│   ├── bebop.py      # Bebop Wrap/Unwrap automation (synchronous)
│   ├── izumi.py      # Izumi Wrap/Unwrap automation (asynchronous)
│   ├── magma.py      # Magma Staking automation
│   ├── bima.py       # Bima Deposit automation
│   ├── lilchogstars.py # Lil Chogstars NFT minting automation
│   ├── naddomains.py  # NAD Domain registration automation
├── pvkey.txt         # Private keys file (create manually)
├── address.txt       # Recipient addresses file (optional for sendtx.py)
└── README.md         # +_-
```
