
import os 
import sys 
import random
import asyncio
from web3 import Web3
from colorama import init, Fore, Style

# Khởi tạo colorama
init(autoreset=True)

# Constants
RPC_URL = "https://testnet-rpc.monad.xyz/"
EXPLORER_URL = "https://testnet.monadexplorer.com/tx/0x"
MAGMA_CONTRACT = "0x2c9C959516e9AAEdB2C748224a41249202ca8BE7"
GAS_LIMIT_STAKE = 500000
GAS_LIMIT_UNSTAKE = 800000

# Hàm đọc nhiều private key từ pvkey.txt
def load_private_keys(file_path):
    try:
        with open(file_path, 'r') as file:
            keys = [line.strip() for line in file.readlines() if line.strip()]
            if not keys:
                raise ValueError("File pvkey.txt rỗng")
            return keys
    except FileNotFoundError:
        print(f"{Fore.RED}❌ Không tìm thấy file pvkey.txt{Style.RESET_ALL}")
        return None
    except Exception as e:
        print(f"{Fore.RED}❌ Lỗi đọc file pvkey.txt: {str(e)}{Style.RESET_ALL}")
        return None

# Khởi tạo web3 provider
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Kiểm tra kết nối
if not w3.is_connected():
    print(f"{Fore.RED}❌ Không kết nối được với RPC{Style.RESET_ALL}")
    exit(1)

# Hàm hiển thị viền đẹp
def print_border(text, color=Fore.CYAN, width=60):
    print(f"{color}┌{'─' * (width - 2)}┐{Style.RESET_ALL}")
    print(f"{color}│ {text:^56} │{Style.RESET_ALL}")
    print(f"{color}└{'─' * (width - 2)}┘{Style.RESET_ALL}")

# Hàm hiển thị bước
def print_step(step, message, lang):
    steps = {
        'vi': {'stake': 'Stake MON', 'unstake': 'Unstake gMON'},
        'en': {'stake': 'Stake MON', 'unstake': 'Unstake gMON'}
    }
    step_text = steps[lang][step]
    print(f"{Fore.YELLOW}➤ {Fore.CYAN}{step_text:<15}{Style.RESET_ALL} | {message}")

# Tạo số lượng ngẫu nhiên (0.01 - 0.03 MON)
def get_random_amount():
    min_val = 0.01
    max_val = 0.03
    random_amount = random.uniform(min_val, max_val)
    return w3.to_wei(round(random_amount, 4), 'ether')

# Tạo delay ngẫu nhiên (1-3 phút)
def get_random_delay():
    return random.randint(60, 180)  # Trả về giây

# Stake MON
async def stake_mon(private_key, amount, language, cycle):
    try:
        account = w3.eth.account.from_key(private_key)
        wallet = account.address[:8] + "..."
        lang = {
            'vi': {
                'start': f"[Vòng {cycle}] Stake {w3.from_wei(amount, 'ether')} MON",
                'send': 'Đang gửi giao dịch...',
                'success': 'Stake thành công!'
            },
            'en': {
                'start': f"[Cycle {cycle}] Staking {w3.from_wei(amount, 'ether')} MON",
                'send': 'Sending transaction...',
                'success': 'Stake successful!'
            }
        }[language]

        print_border(f"{lang['start']} | {wallet}")
        
        tx = {
            'to': MAGMA_CONTRACT,
            'data': '0xd5575982',
            'from': account.address,
            'value': amount,
            'gas': GAS_LIMIT_STAKE,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(account.address),
        }

        print_step('stake', lang['send'], language)
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        print_step('stake', f"Tx: {Fore.YELLOW}{EXPLORER_URL}{tx_hash.hex()}{Style.RESET_ALL}", language)
        await asyncio.sleep(1)
        w3.eth.wait_for_transaction_receipt(tx_hash)
        print_step('stake', f"{Fore.GREEN}{lang['success']}{Style.RESET_ALL}", language)

        return amount

    except Exception as e:
        print_step('stake', f"{Fore.RED}Thất bại / Failed: {str(e)}{Style.RESET_ALL}", language)
        raise

# Unstake gMON
async def unstake_gmon(private_key, amount, language, cycle):
    try:
        account = w3.eth.account.from_key(private_key)
        wallet = account.address[:8] + "..."
        lang = {
            'vi': {
                'start': f"[Vòng {cycle}] Unstake {w3.from_wei(amount, 'ether')} gMON",
                'send': 'Đang gửi giao dịch...',
                'success': 'Unstake thành công!'
            },
            'en': {
                'start': f"[Cycle {cycle}] Unstaking {w3.from_wei(amount, 'ether')} gMON",
                'send': 'Sending transaction...',
                'success': 'Unstake successful!'
            }
        }[language]

        print_border(f"{lang['start']} | {wallet}")
        
        data = "0x6fed1ea7" + w3.to_hex(amount)[2:].zfill(64)
        tx = {
            'to': MAGMA_CONTRACT,
            'data': data,
            'from': account.address,
            'gas': GAS_LIMIT_UNSTAKE,
            'gasPrice': w3.eth.gas_price,
            'nonce': w3.eth.get_transaction_count(account.address),
        }

        print_step('unstake', lang['send'], language)
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        print_step('unstake', f"Tx: {Fore.YELLOW}{EXPLORER_URL}{tx_hash.hex()}{Style.RESET_ALL}", language)
        await asyncio.sleep(1)
        w3.eth.wait_for_transaction_receipt(tx_hash)
        print_step('unstake', f"{Fore.GREEN}{lang['success']}{Style.RESET_ALL}", language)

    except Exception as e:
        print_step('unstake', f"{Fore.RED}Thất bại / Failed: {str(e)}{Style.RESET_ALL}", language)
        raise

# Chạy vòng lặp staking cho từng private key
async def run_staking_cycle(cycles, private_keys, language):
    lang = {
        'vi': "VÒNG LẶP STAKING / STAKING CYCLE",
        'en': "STAKING CYCLE"
    }[language]

    for account_idx, private_key in enumerate(private_keys, 1):
        wallet = w3.eth.account.from_key(private_key).address[:8] + "..."
        print_border(f"TÀI KHOẢN / ACCOUNT {account_idx}/{len(private_keys)} | {wallet}", Fore.CYAN)

        for i in range(cycles):
            print_border(f"{lang} {i + 1}/{cycles} | {wallet}")
            amount = get_random_amount()
            stake_amount = await stake_mon(private_key, amount, language, i + 1)
            delay = get_random_delay()
            print(f"\n{Fore.YELLOW}⏳ {'Đợi' if language == 'vi' else 'Waiting'} {delay / 60:.1f} {'phút trước khi unstake...' if language == 'vi' else 'minutes before unstaking...'}{Style.RESET_ALL}")
            await asyncio.sleep(delay)
            await unstake_gmon(private_key, stake_amount, language, i + 1)
            
            if i < cycles - 1:
                delay = get_random_delay()
                print(f"\n{Fore.YELLOW}⏳ {'Đợi' if language == 'vi' else 'Waiting'} {delay / 60:.1f} {'phút trước vòng tiếp theo...' if language == 'vi' else 'minutes before next cycle...'}{Style.RESET_ALL}")
                await asyncio.sleep(delay)

        if account_idx < len(private_keys):
            delay = get_random_delay()
            print(f"\n{Fore.YELLOW}⏳ {'Đợi' if language == 'vi' else 'Waiting'} {delay / 60:.1f} {'phút trước tài khoản tiếp theo...' if language == 'vi' else 'minutes before next account...'}{Style.RESET_ALL}")
            await asyncio.sleep(delay)

    print(f"{Fore.GREEN}{'═' * 60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}│ {'HOÀN TẤT' if language == 'vi' else 'ALL DONE'}: {cycles} {'VÒNG LẶP CHO' if language == 'vi' else 'CYCLES FOR'} {len(private_keys)} {'TÀI KHOẢN' if language == 'vi' else 'ACCOUNTS'}{' ' * (32 - len(str(cycles)) - len(str(len(private_keys))))}│{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'═' * 60}{Style.RESET_ALL}")

# Hàm chính
async def run(language):
    print(f"{Fore.GREEN}{'═' * 60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}│ {'MAGMA STAKING - MONAD TESTNET':^56} │{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'═' * 60}{Style.RESET_ALL}")

    #private_keys = load_private_keys('pvkey.txt')
    current_directory = os.path.dirname(os.path.abspath(sys.argv[0])) 
    #print(script_directory)
    private_keys = load_private_keys(current_directory +'/pvkey.txt')

    if not private_keys:
        return

    print(f"{Fore.CYAN}👥 {'Tài khoản' if language == 'vi' else 'Accounts'}: {len(private_keys)}{Style.RESET_ALL}")

    while True:
        try:
            print_border("SỐ VÒNG LẶP / NUMBER OF CYCLES", Fore.YELLOW)
            # cycles_input = input(f"{Fore.GREEN}➤ {'Nhập số (mặc định 1): ' if language == 'vi' else 'Enter number (default 1): '}{Style.RESET_ALL}")
            # cycles = int(cycles_input) if cycles_input.strip() else 1
            # if cycles <= 0:
            #     raise ValueError
            cycles=3
            break
            
        except ValueError:
            print(f"{Fore.RED}❌ {'Vui lòng nhập số hợp lệ!' if language == 'vi' else 'Please enter a valid number!'}{Style.RESET_ALL}")

    start_msg = f"Chạy {cycles} vòng staking liền mạch cho {len(private_keys)} tài khoản..." if language == 'vi' else f"Running {cycles} staking cycles immediately for {len(private_keys)} accounts..."
    print(f"{Fore.YELLOW}🚀 {start_msg}{Style.RESET_ALL}")
    await run_staking_cycle(cycles, private_keys, language)

if __name__ == "__main__":
    asyncio.run(run('vi'))
