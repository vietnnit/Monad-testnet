import os
import random
import time
from colorama import init, Fore, Style
from web3 import Web3
from eth_abi import encode

# Initialize colorama
init(autoreset=True)

# Constants
RPC_URL = "https://testnet-rpc.monad.xyz/"
EXPLORER_URL = "https://testnet.monadexplorer.com/tx/"
WMON_CONTRACT = "0x760AfE86e5de5fa0Ee542fc7B7B713e1c5425701"
ROUTER_ADDRESS = "0xF6FFe4f3FdC8BBb7F70FFD48e61f17D1e343dDfD"
USDT_ADDRESS = "0x88b8E2161DEDC77EF4ab7585569D2415a1C1055D"
POOL_FEE = 10000  # 1% fee
CHAIN_ID = 10143  # Monad testnet chain ID

# Initialize web3 provider
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Token definitions
RUBIC_TOKENS = {
    "wmon": {"address": WMON_CONTRACT, "decimals": 18},
    "usdt": {"address": USDT_ADDRESS, "decimals": 6},
    "usdc": {"address": "0xf817257fed379853cDe0fa4F97AB987181B1E5Ea", "decimals": 6},
    "dak": {"address": "0x0F0BDEbF0F83cD1EE3974779Bcb7315f9808c714", "decimals": 18},
    "yaki": {"address": "0xfe140e1dCe99Be9F4F15d657CD9b7BF622270C50", "decimals": 18},
    "chodg": {"address": "0xE0590015A873bF326bd645c3E1266d4db41C4E6B", "decimals": 18}
}

# Contract ABIs
WMON_ABI = [
    {"constant": False, "inputs": [], "name": "deposit", "outputs": [], "payable": True, "stateMutability": "payable", "type": "function"},
    {"constant": False, "inputs": [{"name": "amount", "type": "uint256"}], "name": "withdraw", "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"},
    {"constant": False, "inputs": [{"name": "spender", "type": "address"}, {"name": "value", "type": "uint256"}], "name": "approve", "outputs": [{"name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
    {"constant": True, "inputs": [{"name": "account", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "", "type": "uint256"}], "payable": False, "stateMutability": "view", "type": "function"}
]

ERC20_ABI = [
    {"constant": True, "inputs": [{"name": "account", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"},
    {"constant": False, "inputs": [{"name": "spender", "type": "address"}, {"name": "value", "type": "uint256"}], "name": "approve", "outputs": [{"name": "", "type": "bool"}], "stateMutability": "nonpayable", "type": "function"}
]

RUBIC_ABI = [
    {"inputs": [{"internalType": "bytes[]", "name": "data", "type": "bytes[]"}], "name": "multicall", "outputs": [{"internalType": "bytes[]", "name": "results", "type": "bytes[]"}], "stateMutability": "payable", "type": "function"},
    {"inputs": [], "name": "refundETH", "outputs": [], "stateMutability": "payable", "type": "function"},
    {"inputs": [{"components": [{"internalType": "bytes", "name": "path", "type": "bytes"}, {"internalType": "address", "name": "recipient", "type": "address"}, {"internalType": "uint128", "name": "amount", "type": "uint128"}, {"internalType": "uint256", "name": "minAcquired", "type": "uint256"}, {"internalType": "uint256", "name": "deadline", "type": "uint256"}], "internalType": "struct IiZiSwapRouter.SwapAmountParams", "name": "params", "type": "tuple"}], "name": "swapAmount", "outputs": [{"internalType": "uint256", "name": "cost", "type": "uint256"}, {"internalType": "uint256", "name": "acquire", "type": "uint256"}], "stateMutability": "payable", "type": "function"},
    {"inputs": [{"internalType": "uint256", "name": "minAmount", "type": "uint256"}, {"internalType": "address", "name": "recipient", "type": "address"}], "name": "unwrapWETH9", "outputs": [], "stateMutability": "payable", "type": "function"}
]

# Initialize contracts
wmon_contract = w3.eth.contract(address=WMON_CONTRACT, abi=WMON_ABI)
router_contract = w3.eth.contract(address=ROUTER_ADDRESS, abi=RUBIC_ABI)

# Display functions
def print_border(text, color=Fore.CYAN, width=60):
    print(f"{color}┌{'─' * (width - 2)}┐{Style.RESET_ALL}")
    print(f"{color}│ {text:^56} │{Style.RESET_ALL}")
    print(f"{color}└{'─' * (width - 2)}┘{Style.RESET_ALL}")

def print_step(step, message, lang):
    steps = {
        'vi': {'wrap': 'Wrap MON', 'unwrap': 'Unwrap WMON', 'swap': 'Swap Tokens'},
        'en': {'wrap': 'Wrap MON', 'unwrap': 'Unwrap WMON', 'swap': 'Swap Tokens'}
    }
    step_text = steps[lang][step]
    print(f"{Fore.YELLOW}➤ {Fore.CYAN}{step_text:<15}{Style.RESET_ALL} | {message}")

# Utility functions
def load_private_keys(file_path='pvkey.txt'):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"{Fore.RED}❌ File pvkey.txt not found{Style.RESET_ALL}")
        return []
    except Exception as e:
        print(f"{Fore.RED}❌ Error reading pvkey.txt: {str(e)}{Style.RESET_ALL}")
        return []

def get_mon_amount_from_user(language):
    lang = {
        'vi': "Nhập số MON (0.01 - 999): ",
        'en': "Enter MON amount (0.01 - 999): "
    }
    error = {
        'vi': "Số phải từ 0.01 đến 999 / Nhập lại số hợp lệ!",
        'en': "Amount must be 0.01-999 / Enter a valid number!"
    }
    while True:
        try:
            print_border(lang[language], Fore.YELLOW)
            amount = float(input(f"{Fore.GREEN}➤ {Style.RESET_ALL}"))
            if 0.01 <= amount <= 999:
                return w3.to_wei(amount, 'ether')
            print(f"{Fore.RED}❌ {error[language]}{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}❌ {error[language]}{Style.RESET_ALL}")

def get_random_delay(min_delay=60, max_delay=180):
    return random.randint(min_delay, max_delay)

def get_balance(account, token):
    if token == "mon":  # Changed from "native" to "mon"
        return w3.eth.get_balance(account)
    token_contract = w3.eth.contract(address=RUBIC_TOKENS[token]["address"], abi=ERC20_ABI)
    return token_contract.functions.balanceOf(account).call()

def get_available_tokens(account, min_amount=10**14):
    available = []
    mon_balance = get_balance(account, "mon")
    if mon_balance >= min_amount:
        available.append(("mon", mon_balance))
    
    for token in RUBIC_TOKENS:
        balance = get_balance(account, token)
        if balance >= min_amount:
            available.append((token, balance))
    return available

# Core functions
def wrap_mon(private_key, amount, language):
    try:
        account = w3.eth.account.from_key(private_key)
        wallet = account.address[:8] + "..."
        lang = {
            'vi': {'start': f"Wrap {w3.from_wei(amount, 'ether')} MON → WMON | {wallet}", 'send': 'Đang gửi giao dịch...', 'success': 'Wrap thành công!'},
            'en': {'start': f"Wrap {w3.from_wei(amount, 'ether')} MON → WMON | {wallet}", 'send': 'Sending transaction...', 'success': 'Wrap successful!'}
        }[language]

        if get_balance(account.address, "mon") < amount:
            print_step('wrap', f"{Fore.RED}Insufficient MON balance{Style.RESET_ALL}", language)
            return False

        print_border(lang['start'])
        tx = wmon_contract.functions.deposit().build_transaction({
            'from': account.address,
            'value': amount,
            'gas': 500000,
            'gasPrice': w3.to_wei('100', 'gwei'),
            'nonce': w3.eth.get_transaction_count(account.address),
            'chainId': CHAIN_ID
        })

        print_step('wrap', lang['send'], language)
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        print_step('wrap', f"Tx: {Fore.YELLOW}{EXPLORER_URL}{tx_hash.hex()}{Style.RESET_ALL}", language)
        w3.eth.wait_for_transaction_receipt(tx_hash)
        print_step('wrap', f"{Fore.GREEN}{lang['success']}{Style.RESET_ALL}", language)
        return True
    except Exception as e:
        print_step('wrap', f"{Fore.RED}Failed: {str(e)}{Style.RESET_ALL}", language)
        return False

def swap_tokens(private_key, token_in, token_out, amount, language):
    try:
        account = w3.eth.account.from_key(private_key)
        wallet = account.address[:8] + "..."
        # Use "MON" instead of "NATIVE"
        token_in_display = "MON" if token_in == "mon" else token_in.upper()
        token_out_display = "MON" if token_out == "mon" else token_out.upper()
        amount_readable = w3.from_wei(amount, 'ether') if token_in == "mon" else (amount / (10 ** RUBIC_TOKENS[token_in]["decimals"]))
        lang = {
            'vi': {'start': f"Swap {amount_readable} {token_in_display} → {token_out_display} | {wallet}", 'send': 'Đang gửi giao dịch swap...', 'success': 'Swap thành công!'},
            'en': {'start': f"Swap {amount_readable} {token_in_display} → {token_out_display} | {wallet}", 'send': 'Sending swap transaction...', 'success': 'Swap successful!'}
        }[language]

        print_border(lang['start'])

        # Check balance
        balance = get_balance(account.address, token_in)
        if balance < amount:
            print_step('swap', f"{Fore.RED}Insufficient {token_in_display} balance: {balance / (10 ** (18 if token_in == 'mon' else RUBIC_TOKENS[token_in]['decimals']))} available{Style.RESET_ALL}", language)
            return False

        # Approve token if not MON
        if token_in != "mon":
            token_contract = w3.eth.contract(address=RUBIC_TOKENS[token_in]["address"], abi=ERC20_ABI)
            approve_tx = token_contract.functions.approve(ROUTER_ADDRESS, amount).build_transaction({
                'from': account.address,
                'gas': 100000,
                'gasPrice': w3.to_wei('50', 'gwei'),
                'nonce': w3.eth.get_transaction_count(account.address),
                'chainId': CHAIN_ID
            })
            signed_approve = w3.eth.account.sign_transaction(approve_tx, private_key)
            approve_hash = w3.eth.send_raw_transaction(signed_approve.raw_transaction)
            w3.eth.wait_for_transaction_receipt(approve_hash)
            print_step('swap', f"Approval Tx: {Fore.YELLOW}{EXPLORER_URL}{approve_hash.hex()}{Style.RESET_ALL}", language)

        # Prepare swap path
        token_in_addr = WMON_CONTRACT if token_in == "mon" else RUBIC_TOKENS[token_in]["address"]
        token_out_addr = WMON_CONTRACT if token_out == "mon" else RUBIC_TOKENS[token_out]["address"]
        path = bytes.fromhex(
            w3.to_checksum_address(token_in_addr)[2:] +
            format(POOL_FEE, "06x") +
            w3.to_checksum_address(token_out_addr)[2:]
        )
        deadline = int(time.time()) + 3600

        # Encode swap data
        recipient = ROUTER_ADDRESS if token_out == "mon" else account.address
        swap_data = router_contract.encode_abi("swapAmount", [(path, recipient, amount, 0, deadline)])
        multicall_data = [swap_data]
        
        if token_out == "mon":
            unwrap_data = router_contract.encode_abi("unwrapWETH9", [0, account.address])
            refund_data = router_contract.encode_abi("refundETH")
            multicall_data.extend([unwrap_data, refund_data])

        final_data = router_contract.encode_abi("multicall", [multicall_data])

        # Build transaction
        tx = {
            'from': account.address,
            'to': ROUTER_ADDRESS,
            'value': amount if token_in == "mon" else 0,
            'data': final_data,
            'gas': 500000,
            'gasPrice': w3.to_wei('100', 'gwei'),
            'nonce': w3.eth.get_transaction_count(account.address),
            'chainId': CHAIN_ID
        }

        print_step('swap', lang['send'], language)
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        print_step('swap', f"Tx: {Fore.YELLOW}{EXPLORER_URL}{tx_hash.hex()}{Style.RESET_ALL}", language)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        if receipt['status'] == 1:
            print_step('swap', f"{Fore.GREEN}{lang['success']}{Style.RESET_ALL}", language)
            return True
        else:
            print_step('swap', f"{Fore.RED}Swap failed{Style.RESET_ALL}", language)
            return False
    except Exception as e:
        print_step('swap', f"{Fore.RED}Failed: {str(e)}{Style.RESET_ALL}", language)
        return False

# Main execution
def run_swap_cycle(cycles, private_keys, language):
    all_tokens = list(RUBIC_TOKENS.keys())  # All possible output tokens
    for cycle in range(1, cycles + 1):
        for pk in private_keys:
            account = w3.eth.account.from_key(pk)
            wallet = account.address[:8] + "..."
            msg = f"CYCLE {cycle}/{cycles} | Tài khoản / Account: {wallet}"
            print(f"{Fore.CYAN}{'═' * 60}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}│ {msg:^56} │{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'═' * 60}{Style.RESET_ALL}")

            # Get available tokens
            available_tokens = get_available_tokens(account.address)
            if not available_tokens:
                print(f"{Fore.YELLOW}No tokens with sufficient balance available{Style.RESET_ALL}")
                continue

            # Wrap some MON if MON is available
            amount = get_mon_amount_from_user(language)
            has_mon = "mon" in [t[0] for t in available_tokens]
            if has_mon:
                if wrap_mon(pk, amount, language):
                    # Swap MON to all other tokens
                    mon_balance = get_balance(account.address, "mon")
                    if mon_balance >= amount:
                        for token_out in all_tokens:
                            if token_out != "wmon":  # Skip WMON since we wrap to it
                                swap_amount = amount // len([t for t in all_tokens if t != "wmon"])  # Divide amount among tokens
                                if swap_tokens(pk, "mon", token_out, swap_amount, language):
                                    time.sleep(5)  # Small delay between swaps
                                    # Swap back to MON
                                    token_balance = get_balance(account.address, token_out)
                                    if token_balance >= 10**14:
                                        swap_tokens(pk, token_out, "mon", token_balance // 2, language)
                                else:
                                    print(f"{Fore.YELLOW}Skipping swap to {token_out.upper()} due to failure{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.YELLOW}Insufficient MON balance after wrap{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}Wrap failed, skipping swaps{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}No MON available to wrap and swap{Style.RESET_ALL}")

            if cycle < cycles or pk != private_keys[-1]:
                delay = get_random_delay()
                wait_msg = f"Đợi {delay} giây..." if language == 'vi' else f"Waiting {delay} seconds..."
                print(f"\n{Fore.YELLOW}⏳ {wait_msg}{Style.RESET_ALL}")
                time.sleep(delay)

def run(language='vi'):
    print(f"{Fore.GREEN}{'═' * 60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}│ {'RUBIC SWAP - MONAD TESTNET':^56} │{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'═' * 60}{Style.RESET_ALL}")

    private_keys = load_private_keys()
    if not private_keys:
        print(f"{Fore.RED}No private keys loaded, exiting{Style.RESET_ALL}")
        return

    print(f"{Fore.CYAN}👥 {'Tài khoản' if language == 'vi' else 'Accounts'}: {len(private_keys)}{Style.RESET_ALL}")

    while True:
        try:
            print_border("SỐ VÒNG LẶP / NUMBER OF CYCLES", Fore.YELLOW)
            cycles = input(f"{Fore.GREEN}➤ {'Nhập số (mặc định 1): ' if language == 'vi' else 'Enter number (default 1): '}{Style.RESET_ALL}")
            cycles = int(cycles) if cycles else 1
            if cycles > 0:
                break
            print(f"{Fore.RED}❌ Số phải lớn hơn 0 / Number must be > 0{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}❌ Nhập số hợp lệ / Enter a valid number{Style.RESET_ALL}")

    start_msg = f"Chạy {cycles} vòng hoán đổi..." if language == 'vi' else f"Running {cycles} swap cycles..."
    print(f"{Fore.YELLOW}🚀 {start_msg}{Style.RESET_ALL}")
    run_swap_cycle(cycles, private_keys, language)

    print(f"{Fore.GREEN}{'═' * 60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}│ {'HOÀN TẤT / ALL DONE':^56} │{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'═' * 60}{Style.RESET_ALL}")

if __name__ == "__main__":
    asyncio.run(run('vi'))
