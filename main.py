import os
import sys
import importlib
import inquirer
import asyncio
from colorama import init, Fore, Style

# Khởi tạo colorama
init(autoreset=True)

# Độ rộng viền cố định
BORDER_WIDTH = 80

# Hàm hiển thị viền đẹp mắt
def print_border(text: str, color=Fore.CYAN, width=BORDER_WIDTH):
    text = text.strip()
    if len(text) > width - 4:
        text = text[:width - 7] + "..."  # Cắt dài và thêm "..."
    padded_text = f" {text} ".center(width - 2)
    print(f"{color}┌{'─' * (width - 2)}┐{Style.RESET_ALL}")
    print(f"{color}│{padded_text}│{Style.RESET_ALL}")
    print(f"{color}└{'─' * (width - 2)}┘{Style.RESET_ALL}")

# Hàm hiển thị banner
def _banner():
    banner = r"""

    
    ███╗░░░███╗░█████╗░███╗░░██╗░█████╗░██████╗░  ████████╗███████╗░██████╗████████╗███╗░░██╗███████╗████████╗
    ████╗░████║██╔══██╗████╗░██║██╔══██╗██╔══██╗  ╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝████╗░██║██╔════╝╚══██╔══╝
    ██╔████╔██║██║░░██║██╔██╗██║███████║██║░░██║  ░░░██║░░░█████╗░░╚█████╗░░░░██║░░░██╔██╗██║█████╗░░░░░██║░░░
    ██║╚██╔╝██║██║░░██║██║╚████║██╔══██║██║░░██║  ░░░██║░░░██╔══╝░░░╚═══██╗░░░██║░░░██║╚████║██╔══╝░░░░░██║░░░
    ██║░╚═╝░██║╚█████╔╝██║░╚███║██║░░██║██████╔╝  ░░░██║░░░███████╗██████╔╝░░░██║░░░██║░╚███║███████╗░░░██║░░░
    ╚═╝░░░░░╚═╝░╚════╝░╚═╝░░╚══╝╚═╝░░╚═╝╚═════╝░  ░░░╚═╝░░░╚══════╝╚═════╝░░░░╚═╝░░░╚═╝░░╚══╝╚══════╝░░░╚═╝░░░
    
    
    """
    print(f"{Fore.GREEN}{banner:^80}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
    print_border("MONAD TESTNET", Fore.GREEN)
    print(f"{Fore.YELLOW}│ {'Liên hệ / Contact'}: {Fore.CYAN}https://t.me/thog099{Style.RESET_ALL:^76}│")
    print(f"{Fore.YELLOW}│ {'Replit'}: {Fore.CYAN}Thog{Style.RESET_ALL:^76}│")
    print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")

# Hàm xóa màn hình
def _clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Lựa chọn ngôn ngữ
def select_language():
    while True:
        print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
        print_border("CHỌN NGÔN NGỮ / SELECT LANGUAGE", Fore.YELLOW)
        questions = [
            inquirer.List('language',
                          message=f"{Fore.CYAN}Vui lòng chọn / Please select:{Style.RESET_ALL}",
                          choices=[
                              ("1. Tiếng Việt", 'vi'),
                              ("2. English", 'en')
                          ],
                          carousel=True)
        ]
        answer = inquirer.prompt(questions)
        if answer and answer['language'] in ['vi', 'en']:
            return answer['language']
        print(f"{Fore.RED}❌ {'Lựa chọn không hợp lệ / Invalid choice':^76}{Style.RESET_ALL}")

# Danh sách script
def get_available_scripts(language):
    scripts = {
        'vi': [
            {"name": "1. Swap Rubic x Monad Testnet", "value": "rubic"},
            {"name": "2. Staking Magma x Monad Testnet", "value": "magma"},
            {"name": "3. Swap Izumi x Monad Testnet", "value": "izumi"},
            {"name": "4. Staking aPriori x Monad Testnet", "value": "apriori"},
            {"name": "5. Staking Kintsu x Monad Testnet", "value": "kintsu"},
            {"name": "6. Bean Swap x Monad Testnet", "value": "bean"},
            {"name": "7. Monorail Swap x Monad Testnet", "value": "mono"},
            {"name": "8. Bebop Swap x Monad Testnet", "value": "bebop"},
            {"name": "9. Ambient Finance Swap x Monad Testnet", "value": "ambient"},
            {"name": "10. Uniswap Swap x Monad Testnet", "value": "uniswap"},
            {"name": "11. Deploy Contract x Monad Testnet", "value": "deploy"},
            {"name": "12. Send TX ngẫu nhiên hoặc File (address.txt) x Monad Testnet", "value": "sendtx"},
            {"name": "13. Bima Deposit bmBTC x Monad Testnet", "value": "bima"},
            {"name": "14. Mint NFT Lil Chogstars x Monad Testnet", "value": "lilchogstars"},
            {"name": "15. Nad domain (Coming soon)", "value": "exit"},
            {"name": "16. shMONAD Staking (Coming soon)", "value": "exit"},
            {"name": "17. Thoát", "value": "exit"},
        ],
        'en': [
            {"name": "1. Rubic Swap x Monad Testnet", "value": "rubic"},
            {"name": "2. Magma Staking x Monad Testnet", "value": "magma"},
            {"name": "3. Izumi Swap x Monad Testnet", "value": "izumi"},
            {"name": "4. aPriori Staking x Monad Testnet", "value": "apriori"},
            {"name": "5. Kintsu Staking x Monad Testnet", "value": "kintsu"},
            {"name": "6. Bean Swap x Monad Testnet", "value": "bean"},
            {"name": "7. Monorail Swap x Monad Testnet", "value": "mono"},
            {"name": "8. Bebop Swap x Monad Testnet", "value": "bebop"},
            {"name": "9. Ambient Finance Swap x Monad Testnet", "value": "ambient"},
            {"name": "10. Uniswap Swap x Monad Testnet", "value": "uniswap"},
            {"name": "11. Deploy Contract x Monad Testnet", "value": "deploy"},
            {"name": "12. Send Random TX or File (address.txt) x Monad Testnet", "value": "sendtx"},
            {"name": "13. Bima Deposit bmBTC x Monad Testnet", "value": "bima"},
            {"name": "14. Mint NFT Lil Chogstars x Monad Testnet", "value": "lilchogstars"},
            {"name": "15. Nad domain (Coming soon)", "value": "exit"},
            {"name": "16. shMONAD Staking (Coming soon)", "value": "exit"},
            {"name": "17. Exit", "value": "exit"},
        ]
    }
    return scripts[language]

def run_script(script_module, language):
    """Chạy script bất kể nó là async hay không."""
    run_func = script_module.run
    if asyncio.iscoroutinefunction(run_func):
        asyncio.run(run_func(language))
    else:
        run_func(language)

def main():
    _clear()
    _banner()
    language = select_language()

    while True:
        _clear()
        _banner()
        print_border("MENU CHÍNH / MAIN MENU", Fore.YELLOW)

        available_scripts = get_available_scripts(language)
        questions = [
            inquirer.List('script',
                          message=f"{Fore.CYAN}{'Chọn script để chạy / Select script to run'}{Style.RESET_ALL}",
                          choices=[script["name"] for script in available_scripts],
                          carousel=True)
        ]
        answers = inquirer.prompt(questions)
        if not answers:
            continue

        selected_script_name = answers['script']
        selected_script_value = next(script["value"] for script in available_scripts if script["name"] == selected_script_name)

        if selected_script_value == "exit":
            print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
            print_border("ĐANG THOÁT / EXITING", Fore.GREEN)
            print(f"{Fore.YELLOW}👋 {'Tạm biệt! / Goodbye!' if language == 'vi' else 'Goodbye! / Tạm biệt!':^76}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
            sys.exit(0)

        try:
            print(f"{Fore.CYAN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
            print_border(f"ĐANG CHẠY / RUNNING: {selected_script_name}", Fore.CYAN)
            script_module = importlib.import_module(f"scripts.{selected_script_value}")
            run_script(script_module, language)
            print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
            print_border(f"{'Hoàn thành / Completed'} {selected_script_name}", Fore.GREEN)
            input(f"{Fore.YELLOW}⏎ {'Nhấn Enter để tiếp tục... / Press Enter to continue...'}{Style.RESET_ALL:^76}")
        except ImportError:
            print(f"{Fore.RED}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
            print_border(f"{'Không tìm thấy script / Script not found'}: {selected_script_value}", Fore.RED)
            input(f"{Fore.YELLOW}⏎ {'Nhấn Enter để tiếp tục... / Press Enter to continue...'}{Style.RESET_ALL:^76}")
        except Exception as e:
            print(f"{Fore.RED}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
            print_border(f"{'Lỗi / Error'}: {str(e)}", Fore.RED)
            input(f"{Fore.YELLOW}⏎ {'Nhấn Enter để tiếp tục... / Press Enter to continue...'}{Style.RESET_ALL:^76}")

if __name__ == "__main__":
    main()
