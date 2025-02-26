import os
import random
import asyncio
from web3 import Web3
from eth_account import Account
from colorama import init, Fore, Style

# Khởi tạo colorama
init(autoreset=True)

# Constants
NETWORK_URL = "https://testnet-rpc.monad.xyz/"
CHAIN_ID = 10143
EXPLORER_URL = "https://testnet.monadexplorer.com/tx/0x"

# Khởi tạo web3 provider
w3 = Web3(Web3.HTTPProvider(NETWORK_URL))

# Kiểm tra kết nối
if not w3.is_connected():
    raise Exception("Không thể kết nối đến mạng")

# Hàm đọc private key từ pvkey.txt
def load_private_keys(file_path):
    try:
        with open(file_path, 'r') as file:
            keys = [line.strip() for line in file.readlines() if len(line.strip()) in [64, 66]]
            if not keys:
                raise ValueError("Không tìm thấy private key hợp lệ trong file")
            return keys
    except FileNotFoundError:
        print(f"{Fore.RED}❌ Không tìm thấy file pvkey.txt{Style.RESET_ALL}")
        return None
    except Exception as e:
        print(f"{Fore.RED}❌ Lỗi đọc file pvkey.txt: {str(e)}{Style.RESET_ALL}")
        return None

# Hàm đọc địa chỉ từ address.txt
def load_addresses(file_path):
    try:
        with open(file_path, 'r') as file:
            addresses = [line.strip() for line in file if line.strip()]
            if not addresses:
                raise ValueError("Không tìm thấy địa chỉ hợp lệ trong file")
            return addresses
    except FileNotFoundError:
        print(f"{Fore.RED}❌ Không tìm thấy file address.txt{Style.RESET_ALL}")
        return None
    except Exception as e:
        print(f"{Fore.RED}❌ Lỗi đọc file address.txt: {str(e)}{Style.RESET_ALL}")
        return None

# Hàm hiển thị viền đẹp mắt
def print_border(text, color=Fore.MAGENTA, width=60):
    print(f"{color}╔{'═' * (width - 2)}╗{Style.RESET_ALL}")
    print(f"{color}║ {text:^56} ║{Style.RESET_ALL}")
    print(f"{color}╚{'═' * (width - 2)}╝{Style.RESET_ALL}")

# Hàm hiển thị bước
def print_step(step, message, lang):
    steps = {
        'vi': {'send': 'Gửi Giao Dịch'},
        'en': {'send': 'Send Transaction'}
    }
    step_text = steps[lang][step]
    print(f"{Fore.YELLOW}🔸 {Fore.CYAN}{step_text:<15}{Style.RESET_ALL} | {message}")

# Địa chỉ ngẫu nhiên với checksum
def get_random_address():
    random_address = '0x' + ''.join(random.choices('0123456789abcdef', k=40))
    return w3.to_checksum_address(random_address)

# Hàm gửi giao dịch
async def send_transaction(private_key, to_address, amount, language):
    account = Account.from_key(private_key)
    sender_address = account.address
    lang = {
        'vi': {'send': 'Đang gửi giao dịch...', 'success': 'Giao dịch thành công!', 'failure': 'Giao dịch thất bại'},
        'en': {'send': 'Sending transaction...', 'success': 'Transaction successful!', 'failure': 'Transaction failed'}
    }[language]

    try:
        nonce = w3.eth.get_transaction_count(sender_address)
        latest_block = w3.eth.get_block('latest')
        base_fee_per_gas = latest_block['baseFeePerGas']
        max_priority_fee_per_gas = w3.to_wei(2, 'gwei')
        max_fee_per_gas = base_fee_per_gas + max_priority_fee_per_gas

        tx = {
            'nonce': nonce,
            'to': w3.to_checksum_address(to_address),
            'value': w3.to_wei(amount, 'ether'),
            'gas': 21000,
            'maxFeePerGas': max_fee_per_gas,
            'maxPriorityFeePerGas': max_priority_fee_per_gas,
            'chainId': CHAIN_ID,
        }

        print_step('send', lang['send'], language)
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_link = f"{EXPLORER_URL}{tx_hash.hex()}"
        
        await asyncio.sleep(2)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180)
        
        if receipt.status == 1:
            print_step('send', f"{Fore.GREEN}✔ {lang['success']} Tx: {tx_link}{Style.RESET_ALL}", language)
            print(f"{Fore.YELLOW}Người gửi / Sender: {sender_address}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Người nhận / Receiver: {to_address}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Số lượng / Amount: {amount:.6f} MONAD{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Gas: {receipt['gasUsed']}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Khối / Block: {receipt['blockNumber']}{Style.RESET_ALL}")
            balance = w3.from_wei(w3.eth.get_balance(sender_address), 'ether')
            print(f"{Fore.YELLOW}Số dư / Balance: {balance:.6f} MONAD{Style.RESET_ALL}")
            return True
        else:
            print_step('send', f"{Fore.RED}✘ {lang['failure']} Tx: {tx_link}{Style.RESET_ALL}", language)
            return False
    except Exception as e:
        print_step('send', f"{Fore.RED}✘ Thất bại / Failed: {str(e)}{Style.RESET_ALL}", language)
        return False

# Gửi giao dịch đến địa chỉ ngẫu nhiên
async def send_to_random_addresses(amount, tx_count, private_keys, language):
    lang = {
        'vi': {'start': f'Bắt đầu gửi {tx_count} giao dịch ngẫu nhiên'},
        'en': {'start': f'Starting {tx_count} random transactions'}
    }[language]
    print_border(lang['start'], Fore.CYAN)
    
    count = 0
    for _ in range(tx_count):
        for private_key in private_keys:
            to_address = get_random_address()
            if await send_transaction(private_key, to_address, amount, language):
                count += 1
            await asyncio.sleep(random.uniform(1, 3))  # Delay ngẫu nhiên 1-3 giây
    
    print(f"{Fore.YELLOW}Tổng giao dịch thành công / Total successful: {count}{Style.RESET_ALL}")
    return count

# Gửi giao dịch đến địa chỉ từ file
async def send_to_file_addresses(amount, addresses, private_keys, language):
    lang = {
        'vi': {'start': f'Bắt đầu gửi giao dịch đến {len(addresses)} địa chỉ từ file'},
        'en': {'start': f'Starting transactions to {len(addresses)} addresses from file'}
    }[language]
    print_border(lang['start'], Fore.CYAN)
    
    count = 0
    for private_key in private_keys:
        for to_address in addresses:
            if await send_transaction(private_key, to_address, amount, language):
                count += 1
            await asyncio.sleep(random.uniform(1, 3))  # Delay ngẫu nhiên 1-3 giây
    
    print(f"{Fore.YELLOW}Tổng giao dịch thành công / Total successful: {count}{Style.RESET_ALL}")
    return count

# Hàm chính
async def run(language):
    print(f"{Fore.GREEN}{'═' * 60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}│ {'SEND TX - MONAD TESTNET':^56} │{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'═' * 60}{Style.RESET_ALL}")

    private_keys = load_private_keys('pvkey.txt')
    if not private_keys:
        return

    print(f"{Fore.CYAN}👥 {'Tài khoản' if language == 'vi' else 'Accounts'}: {len(private_keys)}{Style.RESET_ALL}")

    while True:
        try:
            print_border("🔢 SỐ LƯỢNG GIAO DỊCH / NUMBER OF TRANSACTIONS", Fore.YELLOW)
            tx_count_input = input(f"{Fore.GREEN}➤ {'Nhập số (mặc định 5): ' if language == 'vi' else 'Enter number (default 5): '}{Style.RESET_ALL}")
            tx_count = int(tx_count_input) if tx_count_input.strip() else 5
            if tx_count <= 0:
                raise ValueError
            break
        except ValueError:
            print(f"{Fore.RED}❌ {'Vui lòng nhập số hợp lệ!' if language == 'vi' else 'Please enter a valid number!'}{Style.RESET_ALL}")

    while True:
        try:
            print_border("💰 SỐ LƯỢNG MONAD / AMOUNT OF MONAD", Fore.YELLOW)
            amount_input = input(f"{Fore.GREEN}➤ {'Nhập số (mặc định 0.000001, tối đa 999): ' if language == 'vi' else 'Enter amount (default 0.000001, max 999): '}{Style.RESET_ALL}")
            amount = float(amount_input) if amount_input.strip() else 0.000001
            if 0 < amount <= 999:
                break
            raise ValueError
        except ValueError:
            print(f"{Fore.RED}❌ {'Số lượng phải lớn hơn 0 và không quá 999!' if language == 'vi' else 'Amount must be greater than 0 and not exceed 999!'}{Style.RESET_ALL}")

    while True:
        print_border("🔧 CHỌN LOẠI GIAO DỊCH / TRANSACTION TYPE", Fore.YELLOW)
        print(f"{Fore.CYAN}1. {'Gửi đến địa chỉ ngẫu nhiên' if language == 'vi' else 'Send to random address'}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}2. {'Gửi đến địa chỉ từ file (address.txt)' if language == 'vi' else 'Send to addresses from file (address.txt)'}{Style.RESET_ALL}")
        choice = input(f"{Fore.GREEN}➤ {'Nhập lựa chọn (1/2): ' if language == 'vi' else 'Enter choice (1/2): '}{Style.RESET_ALL}")

        if choice == '1':
            await send_to_random_addresses(amount, tx_count, private_keys, language)
            break
        elif choice == '2':
            addresses = load_addresses('address.txt')
            if addresses:
                await send_to_file_addresses(amount, addresses, private_keys, language)
            break
        else:
            print(f"{Fore.RED}❌ {'Lựa chọn không hợp lệ!' if language == 'vi' else 'Invalid choice!'}{Style.RESET_ALL}")

    print(f"{Fore.GREEN}{'═' * 60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}│ {'HOÀN TẤT' if language == 'vi' else 'ALL DONE'}: {tx_count} {'GIAO DỊCH CHO' if language == 'vi' else 'TRANSACTIONS FOR'} {len(private_keys)} {'TÀI KHOẢN' if language == 'vi' else 'ACCOUNTS'}{' ' * (32 - len(str(tx_count)) - len(str(len(private_keys))))}│{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'═' * 60}{Style.RESET_ALL}")

# Chạy chương trình nếu là file chính
if __name__ == "__main__":
    asyncio.run(run('vi'))
