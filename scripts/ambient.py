import os
import asyncio
import random
import time
from web3 import Web3
from colorama import init, Fore, Style

# Khởi tạo colorama
init(autoreset=True)

# Constants
RPC_URL = "https://testnet-rpc.monad.xyz/"
EXPLORER_URL = "https://testnet.monadexplorer.com/tx/"
ROUTER_ADDRESS = Web3.to_checksum_address("0x88B96aF200c8a9c35442C8AC6cd3D22695AaE4F0")

# Danh sách token với địa chỉ checksum
TOKENS = {
    "USDC": {
        "address": Web3.to_checksum_address("0xf817257fed379853cde0fa4f97ab987181b1e5ea"),
        "symbol": "USDC",
        "name": "USD Coin",
        "minAmount": 0.01,
        "maxAmount": 1,
        "decimals": 6,
    },
    "USDT": {
        "address": Web3.to_checksum_address("0x88b8E2161DEDC77EF4ab7585569D2415a1C1055D"),
        "symbol": "USDT",
        "name": "Tether USD",
        "minAmount": 0.01,
        "maxAmount": 1,
        "decimals": 6,
    },
    "WETH": {
        "address": Web3.to_checksum_address("0xB5a30b0FDc5EA94A52fDc42e3E9760Cb8449Fb37"),
        "symbol": "WETH",
        "name": "Wrapped ETH",
        "minAmount": 0.0000001,
        "maxAmount": 0.000001,
        "decimals": 18,
    },
}

# Khởi tạo web3 provider
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Kiểm tra kết nối
if not w3.is_connected():
    print(f"{Fore.RED}❌ Không kết nối được với RPC{Style.RESET_ALL}")
    exit(1)

# ABI cho Ambient DEX và Token
AMBIENT_ABI = [
    {
        "constant": False,
        "inputs": [
            {"name": "base", "type": "address"},
            {"name": "quote", "type": "address"},
            {"name": "poolIdx", "type": "uint256"},
            {"name": "isBuy", "type": "bool"},
            {"name": "inBaseQty", "type": "bool"},
            {"name": "qty", "type": "uint128"},
            {"name": "tip", "type": "uint16"},
            {"name": "limitPrice", "type": "uint128"},
            {"name": "minOut", "type": "uint128"},
            {"name": "reserveFlags", "type": "uint8"}
        ],
        "name": "swap",
        "outputs": [
            {"name": "baseFlow", "type": "int128"},
            {"name": "quoteFlow", "type": "int128"}
        ],
        "payable": True,
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {"name": "callpath", "type": "uint16"},
            {"name": "cmd", "type": "bytes"}
        ],
        "name": "userCmd",
        "outputs": [{"name": "", "type": "bytes"}],
        "payable": True,
        "stateMutability": "payable",
        "type": "function"
    }
]
TOKEN_ABI = [
    {
        "constant": False,
        "inputs": [
            {"name": "spender", "type": "address"},
            {"name": "amount", "type": "uint256"}
        ],
        "name": "approve",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {"name": "owner", "type": "address"},
            {"name": "spender", "type": "address"}
        ],
        "name": "allowance",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [{"name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    }
]

# Hàm đọc private key từ pvkey.txt
def load_private_keys(file_path='pvkey.txt'):
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

# Hàm hiển thị viền đẹp
def print_border(text, color=Fore.CYAN, width=60):
    print(f"{color}┌{'─' * (width - 2)}┐{Style.RESET_ALL}")
    print(f"{color}│ {text:^56} │{Style.RESET_ALL}")
    print(f"{color}└{'─' * (width - 2)}┘{Style.RESET_ALL}")

# Hàm hiển thị bước
def print_step(step, message, language):
    steps = {
        'vi': {'approve': 'Phê duyệt', 'swap': 'Swap'},
        'en': {'approve': 'Approve', 'swap': 'Swap'}
    }
    lang = steps[language]
    step_text = lang.get(step, step)
    print(f"{Fore.YELLOW}➤ {Fore.CYAN}{step_text:<15}{Style.RESET_ALL} | {message}")

# Tạo số lượng ngẫu nhiên giữa min và max
def get_random_amount(min_val, max_val):
    amount = random.uniform(min_val, max_val)
    return round(amount, 8)

# Phê duyệt token
async def approve_token(private_key, token_address, amount, decimals, language):
    account = w3.eth.account.from_key(private_key)
    wallet = account.address[:8] + "..."
    lang = {
        'vi': {
            'check': "Đang kiểm tra phê duyệt token...",
            'approve': "Đang phê duyệt",
            'success': "Phê duyệt thành công",
            'fail': "Phê duyệt thất bại"
        },
        'en': {
            'check': "Checking token approval...",
            'approve': "Approving",
            'success': "Approved successfully",
            'fail': "Approval failed"
        }
    }[language]

    token_contract = w3.eth.contract(address=token_address, abi=TOKEN_ABI)
    try:
        print_step('approve', lang['check'], language)
        allowance = await asyncio.get_event_loop().run_in_executor(None, lambda: token_contract.functions.allowance(account.address, ROUTER_ADDRESS).call())
        amount_in_decimals = w3.to_wei(amount, 'ether') if decimals == 18 else int(amount * 10**decimals)

        # Kiểm tra số dư trước khi phê duyệt
        balance = await asyncio.get_event_loop().run_in_executor(None, lambda: token_contract.functions.balanceOf(account.address).call())
        if balance < amount_in_decimals:
            raise Exception(f"Không đủ số dư {TOKENS[token_address]['symbol']} ({balance / 10**decimals} < {amount})")

        if allowance < amount_in_decimals:
            print_step('approve', f"{lang['approve']} {wallet}...", language)
            tx = token_contract.functions.approve(ROUTER_ADDRESS, 2**256 - 1).build_transaction({
                'from': account.address,
                'gas': 300000,
                'gasPrice': w3.eth.gas_price,
                'nonce': w3.eth.get_transaction_count(account.address),
            })
            signed_tx = w3.eth.account.sign_transaction(tx, private_key)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            await asyncio.sleep(1)
            receipt = await asyncio.get_event_loop().run_in_executor(None, lambda: w3.eth.wait_for_transaction_receipt(tx_hash, timeout=300))
            if receipt.status == 0:
                raise Exception("Phê duyệt thất bại trên blockchain")
            print_step('approve', f"{Fore.GREEN}{lang['success']}{Style.RESET_ALL}", language)
        else:
            print_step('approve', f"{Fore.GREEN}Đã phê duyệt trước đó / Already approved{Style.RESET_ALL}", language)
    except Exception as e:
        print_step('approve', f"{Fore.RED}{lang['fail']}: {str(e)}{Style.RESET_ALL}", language)
        raise

# Thử lại thao tác nếu thất bại
async def retry_operation(operation, max_retries=3, delay=5):
    for i in range(max_retries):
        try:
            return await operation()
        except Exception as e:
            if "SERVER_ERROR" in str(e) or "bad response" in str(e):
                if i < max_retries - 1:
                    print(f"{Fore.YELLOW}❌ Lỗi RPC, thử lại sau {delay} giây... (Lần {i + 1}/{max_retries}){Style.RESET_ALL}")
                    await asyncio.sleep(delay)
                    continue
            raise e
    raise Exception("Đã vượt quá số lần thử lại tối đa")

# Swap token
async def swap_tokens(private_key, from_token, to_token, amount, language):
    account = w3.eth.account.from_key(private_key)
    wallet = account.address[:8] + "..."
    lang = {
        'vi': {
            'start': f"Đang swap {amount} {from_token['symbol']} sang {to_token['symbol']}",
            'send': "Đang gửi giao dịch...",
            'success': "Swap thành công!",
            'transfer': "Chuyển token thành công!",
            'fail': "Swap thất bại"
        },
        'en': {
            'start': f"Swapping {amount} {from_token['symbol']} to {to_token['symbol']}",
            'send': "Sending transaction...",
            'success': "Swap successful!",
            'transfer': "Tokens transferred successfully!",
            'fail': "Swap failed"
        }
    }[language]

    try:
        print_border(f"{lang['start']} | {wallet}")
        amount_in = w3.to_wei(amount, 'ether') if from_token['decimals'] == 18 else int(amount * 10**from_token['decimals'])

        # Kiểm tra số dư trước khi swap
        if from_token['symbol'] == "MON":
            mon_balance = await asyncio.get_event_loop().run_in_executor(None, lambda: w3.eth.get_balance(account.address))
            if mon_balance < amount_in:
                raise Exception(f"Không đủ số dư MON ({w3.from_wei(mon_balance, 'ether')} < {amount})")
        else:
            token_contract = w3.eth.contract(address=from_token['address'], abi=TOKEN_ABI)
            balance = await asyncio.get_event_loop().run_in_executor(None, lambda: token_contract.functions.balanceOf(account.address).call())
            if balance < amount_in:
                raise Exception(f"Không đủ số dư {from_token['symbol']} ({balance / 10**from_token['decimals']} < {amount})")
            await retry_operation(lambda: approve_token(private_key, from_token['address'], amount, from_token['decimals'], language))

        ambient_contract = w3.eth.contract(address=ROUTER_ADDRESS, abi=AMBIENT_ABI)
        if from_token['symbol'] == "MON":
            # Swap từ MON sang token
            tx = ambient_contract.functions.swap(
                WMON_CONTRACT,  # base
                to_token['address'],  # quote
                36000,  # poolIdx
                True,  # isBuy (mua token bằng MON)
                True,  # inBaseQty (số lượng tính bằng base token)
                amount_in,  # qty
                0,  # tip
                0,  # limitPrice (không giới hạn)
                0,  # minOut (không yêu cầu tối thiểu, cần điều chỉnh nếu có slippage)
                0  # reserveFlags
            ).build_transaction({
                'from': account.address,
                'value': amount_in,
                'gas': 250000,
                'gasPrice': w3.eth.gas_price,
                'nonce': w3.eth.get_transaction_count(account.address),
            })
        elif to_token['symbol'] == "MON":
            # Swap từ token sang MON
            tx = ambient_contract.functions.swap(
                from_token['address'],  # base
                WMON_CONTRACT,  # quote
                36000,  # poolIdx
                False,  # isBuy (bán token lấy MON)
                True,  # inBaseQty (số lượng tính bằng base token)
                amount_in,  # qty
                0,  # tip
                0,  # limitPrice (không giới hạn)
                0,  # minOut (không yêu cầu tối thiểu, cần điều chỉnh nếu có slippage)
                0  # reserveFlags
            ).build_transaction({
                'from': account.address,
                'gas': 350000,
                'gasPrice': w3.eth.gas_price,
                'nonce': w3.eth.get_transaction_count(account.address),
            })
        else:
            # Swap giữa hai token
            cmd_data = w3.codec.encode(
                ["uint256", "address", "uint24", "bool", "bool", "uint128", "uint16", "uint128", "uint128", "uint8"],
                [0, from_token['address'], 36000, True, True, amount_in, 0, w3.to_wei(100000, 'ether'), 0, 0]
            )
            tx = ambient_contract.functions.userCmd(1, cmd_data).build_transaction({
                'from': account.address,
                'gas': 500000,
                'gasPrice': w3.eth.gas_price,
                'nonce': w3.eth.get_transaction_count(account.address),
            })

        print_step('swap', lang['send'], language)
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print_step('swap', f"{Fore.CYAN}Mã giao dịch / Tx: {EXPLORER_URL}{tx_hash.hex()}{Style.RESET_ALL}", language)
        await asyncio.sleep(1)
        receipt = await asyncio.get_event_loop().run_in_executor(None, lambda: w3.eth.wait_for_transaction_receipt(tx_hash, timeout=300))

        if receipt.status == 1:
            print_step('swap', f"{Fore.GREEN}{lang['success']}{Style.RESET_ALL}", language)
            transfer_events = [log for log in receipt.logs if log['topics'][0].hex() == '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef']
            if transfer_events:
                print_step('swap', f"{Fore.GREEN}{lang['transfer']}{Style.RESET_ALL}", language)
        else:
            # Giải mã lỗi revert nếu có
            try:
                tx_details = await asyncio.get_event_loop().run_in_executor(None, lambda: w3.eth.get_transaction(tx_hash))
                revert_reason = await asyncio.get_event_loop().run_in_executor(None, lambda: w3.eth.call(tx_details))
                error_msg = w3.to_text(revert_reason[4:]) if revert_reason.startswith('0x08c379a0') else revert_reason.hex()
                raise Exception(f"Giao dịch thất bại: {error_msg}")
            except Exception as revert_error:
                raise Exception(f"Giao dịch thất bại: {str(revert_error)}")
    except Exception as e:
        print_step('swap', f"{Fore.RED}{lang['fail']}: {str(e)}{Style.RESET_ALL}", language)
        raise

# Kiểm tra số dư
async def check_balance(wallet_address, language):
    lang = {
        'vi': {"title": "Số dư", "error": "Lỗi đọc số dư"},
        'en': {"title": "Balance", "error": "Error reading balance"}
    }[language]

    print(f"\n{Fore.CYAN}💰 {lang['title']}:{Style.RESET_ALL}")
    try:
        mon_balance = await asyncio.get_event_loop().run_in_executor(None, lambda: w3.eth.get_balance(wallet_address))
        print(f"{Fore.CYAN}MON: {w3.from_wei(mon_balance, 'ether')}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}MON: {lang['error']} - {str(e)}{Style.RESET_ALL}")

    for symbol, token in TOKENS.items():
        try:
            token_contract = w3.eth.contract(address=token['address'], abi=TOKEN_ABI)
            balance = await asyncio.get_event_loop().run_in_executor(None, lambda: token_contract.functions.balanceOf(wallet_address).call())
            print(f"{Fore.CYAN}{symbol}: {balance / 10**token['decimals']}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}{symbol}: {lang['error']} - {str(e)}{Style.RESET_ALL}")

# Thực hiện random swap
async def perform_random_swap(private_key, language):
    token_symbols = list(TOKENS.keys())
    from_symbol = "MON" if random.random() < 0.5 else random.choice(token_symbols)
    to_symbol = random.choice([s for s in token_symbols if s != from_symbol])
    from_token = TOKENS[from_symbol] if from_symbol != "MON" else {"symbol": "MON", "decimals": 18}
    to_token = TOKENS[to_symbol]
    amount = get_random_amount(from_token.get('minAmount', 0.001), from_token.get('maxAmount', 0.01))
    amount = max(amount, from_token.get('minAmount', 0.001))

    lang = {
        'vi': f"Random swap {from_symbol} sang {to_symbol}: {amount} {from_symbol}",
        'en': f"Random swap {from_symbol} to {to_symbol}: {amount} {from_symbol}"
    }[language]

    print(f"\n{Fore.YELLOW}🎲 {lang}{Style.RESET_ALL}")
    await swap_tokens(private_key, from_token, to_token, amount, language)

# Thực hiện manual swap
async def perform_manual_swap(private_key, from_symbol, to_symbol, amount, language):
    from_token = TOKENS[from_symbol] if from_symbol != "MON" else {"symbol": "MON", "decimals": 18}
    to_token = TOKENS[to_symbol]
    lang = {
        'vi': f"Manual swap {from_symbol} sang {to_symbol}: {amount} {from_symbol}",
        'en': f"Manual swap {from_symbol} to {to_symbol}: {amount} {from_symbol}"
    }[language]

    print(f"\n{Fore.YELLOW}🎲 {lang}{Style.RESET_ALL}")
    await swap_tokens(private_key, from_token, to_token, amount, language)

# Hàm chính
async def run(language):
    print(f"{Fore.GREEN}{'═' * 60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}│ {'AMBIENT SWAP BOT - MONAD TESTNET':^56} │{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'═' * 60}{Style.RESET_ALL}")

    private_keys = load_private_keys('pvkey.txt')
    if not private_keys:
        return

    print(f"{Fore.CYAN}👥 {'Tài khoản' if language == 'vi' else 'Accounts'}: {len(private_keys)}{Style.RESET_ALL}")

    choices = [
        {"title": "Swap Ngẫu Nhiên" if language == 'vi' else "Random Swap", "value": "random_swap"},
        {"title": "Swap Thủ Công" if language == 'vi' else "Manual Swap", "value": "manual_swap"},
        {"title": "Thoát" if language == 'vi' else "Exit", "value": "exit"}
    ]

    for idx, private_key in enumerate(private_keys, 1):
        wallet_short = w3.eth.account.from_key(private_key).address[:8] + "..."
        print_border(f"TÀI KHOẢN / ACCOUNT {idx}/{len(private_keys)} | {wallet_short}", Fore.CYAN)
        await check_balance(w3.eth.account.from_key(private_key).address, language)

        while True:
            print_border("LỰA CHỌN / OPTIONS", Fore.YELLOW)
            for i, choice in enumerate(choices, 1):
                print(f"{Fore.GREEN}{i}. {choice['title']}{Style.RESET_ALL}")
            action = input(f"{Fore.GREEN}➤ {'Chọn hành động (1-3): ' if language == 'vi' else 'Select action (1-3): '}{Style.RESET_ALL}")

            if action == "3" or action.lower() == "exit":
                break
            elif action == "1":
                number_of_swaps = 5
                start_msg = f"Chạy {number_of_swaps}x random swap" if language == 'vi' else f"Starting {number_of_swaps}x random swaps"
                print(f"{Fore.GREEN}🚀 {start_msg}{Style.RESET_ALL}")
                for i in range(number_of_swaps):
                    print(f"\n{Fore.YELLOW}📍 Random Swap {i + 1}/{number_of_swaps}:{Style.RESET_ALL}")
                    await perform_random_swap(private_key, language)
                    await check_balance(w3.eth.account.from_key(private_key).address, language)
                    if i < number_of_swaps - 1:
                        delay = 15
                        print(f"{Fore.YELLOW}⏳ {'Đợi' if language == 'vi' else 'Waiting'} {delay} {'giây trước swap tiếp theo...' if language == 'vi' else 'seconds before next swap...'}{Style.RESET_ALL}")
                        await asyncio.sleep(delay)
            elif action == "2":
                token_choices = ["MON"] + list(TOKENS.keys())
                print_border("CHỌN TOKEN NGUỒN / SELECT FROM TOKEN", Fore.YELLOW)
                for i, symbol in enumerate(token_choices, 1):
                    name = TOKENS[symbol]['name'] if symbol != "MON" else "Monad Coin"
                    print(f"{Fore.GREEN}{i}. {name} ({symbol}){Style.RESET_ALL}")
                from_idx = int(input(f"{Fore.GREEN}➤ {'Chọn token nguồn (1-{len(token_choices)}): ' if language == 'vi' else 'Select from token (1-{len(token_choices)}): '}{Style.RESET_ALL}")) - 1
                from_symbol = token_choices[from_idx]

                print_border("CHỌN TOKEN ĐÍCH / SELECT TO TOKEN", Fore.YELLOW)
                to_choices = [s for s in token_choices if s != from_symbol]
                for i, symbol in enumerate(to_choices, 1):
                    name = TOKENS[symbol]['name'] if symbol != "MON" else "Monad Coin"
                    print(f"{Fore.GREEN}{i}. {name} ({symbol}){Style.RESET_ALL}")
                to_idx = int(input(f"{Fore.GREEN}➤ {'Chọn token đích (1-{len(to_choices)}): ' if language == 'vi' else 'Select to token (1-{len(to_choices)}): '}{Style.RESET_ALL}")) - 1
                to_symbol = to_choices[to_idx]

                from_token = TOKENS[from_symbol] if from_symbol != "MON" else {"symbol": "MON", "decimals": 18}
                min_amount = from_token.get('minAmount', 0.001)
                max_amount = from_token.get('maxAmount', 0.01)
                while True:
                    try:
                        print_border(f"NHẬP SỐ LƯỢNG / ENTER AMOUNT ({from_symbol})", Fore.YELLOW)
                        amount_input = float(input(f"{Fore.GREEN}➤ {'Nhập số lượng (' + str(min_amount) + '-' + str(max_amount) + '): ' if language == 'vi' else 'Enter amount (' + str(min_amount) + '-' + str(max_amount) + '): '}{Style.RESET_ALL}"))
                        if min_amount <= amount_input <= max_amount:
                            break
                        print(f"{Fore.RED}❌ {'Số lượng phải từ ' + str(min_amount) + ' đến ' + str(max_amount) if language == 'vi' else 'Amount must be between ' + str(min_amount) + ' and ' + str(max_amount)}!{Style.RESET_ALL}")
                    except ValueError:
                        print(f"{Fore.RED}❌ {'Vui lòng nhập số hợp lệ!' if language == 'vi' else 'Please enter a valid number!'}{Style.RESET_ALL}")

                await perform_manual_swap(private_key, from_symbol, to_symbol, amount_input, language)
                await check_balance(w3.eth.account.from_key(private_key).address, language)
            else:
                print(f"{Fore.RED}❌ {'Lựa chọn không hợp lệ, chọn lại!' if language == 'vi' else 'Invalid choice, try again!'}{Style.RESET_ALL}")

        if idx < len(private_keys):
            delay = random.randint(60, 180)
            print(f"\n{Fore.YELLOW}⏳ {'Đợi' if language == 'vi' else 'Waiting'} {delay / 60:.1f} {'phút trước tài khoản tiếp theo...' if language == 'vi' else 'minutes before next account...'}{Style.RESET_ALL}")
            await asyncio.sleep(delay)

    print(f"{Fore.GREEN}{'═' * 60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}│ {'HOÀN TẤT' if language == 'vi' else 'ALL DONE'} - {len(private_keys)} {'TÀI KHOẢN' if language == 'vi' else 'ACCOUNTS'}{' ' * (40 - len(str(len(private_keys))))}│{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'═' * 60}{Style.RESET_ALL}")

if __name__ == "__main__":
    asyncio.run(run('vi'))
