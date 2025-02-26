import os
import sys
import importlib
import inquirer
import asyncio
from colorama import init, Fore, Style

# Khởi tạo colorama
init()

# Hàm hiển thị viền đẹp
def print_border(text, color=Fore.CYAN, width=60):
    print(f"{color}┌{'─' * (width - 2)}┐{Style.RESET_ALL}")
    print(f"{color}│ {text:^56} │{Style.RESET_ALL}")
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
    print(f"{Fore.GREEN}{banner}{Style.RESET_ALL}")
    print_border("MONAD TESTNET", Fore.GREEN)
    print(f"{Fore.YELLOW}│ Liên hệ: {Fore.CYAN}https://t.me/thog099{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}│ Replit: {Fore.CYAN}Thog{Style.RESET_ALL}")

# Hàm xóa màn hình
def _clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Lựa chọn ngôn ngữ
def select_language():
    while True:
        print_border("CHỌN NGÔN NGỮ / SELECT LANGUAGE", Fore.YELLOW)
        questions = [
            inquirer.List('language',
                          message="",
                          choices=[
                              ("1. Tiếng Việt", 'vi'),
                              ("2. English", 'en')
                          ],
                          carousel=True)
        ]
        answer = inquirer.prompt(questions)
        if answer and answer['language'] in ['vi', 'en']:
            return answer['language']
        print(f"{Fore.RED}❌ Lựa chọn không hợp lệ / Invalid choice{Style.RESET_ALL}")

# Danh sách script
def get_available_scripts(language):
    scripts = {
        'vi': [
            {"name": "1. Swap Rubic x Monad Tesnet", "value": "rubic"},
            {"name": "2. Staking Magma x Monad Tesnet", "value": "magma"},
            {"name": "3. Swap Izumi x Monad Tesnet", "value": "izumi"},
            {"name": "4. Staking aPriori x Monad Tesnet", "value": "apriori"},
            {"name": "5. Staking Kintsu x Monad Tesnet", "value": "kintsu"},  # Thêm Kitsu Staking
            {"name": "6. Bean Swap x Monad Tesnet", "value": "bean"},
            {"name": "7. Monorail Swap x Monad Tesnet", "value": "mono"},
            {"name": "8. Bebop Swap x Monad Tesnet", "value": "bebop"},
            {"name": "9. Ambient Finance Swap x Monad Tesnet ( Đang bảo trì )", "value": "ambient"},
            {"name": "10. Uniswap Swap x Monad Tesnet", "value": "uniswap"},
            {"name": "11. Deploy Contract x Monad Tesnet", "value": "deploy"},
            {"name": "12. Send TX ngẫu nhiên hoặc Send TX địa chỉ File (address.txt) x Monad Tesnet", "value": "sendtx"},
            {"name": "13. Bima Deposit bmBTC ( Coming soon )", "value": "exit"},
            {"name": "14. Nad domain ( Coming soon )", "value": "exit"},
            {"name": "15. shMONAD Staking ( Coming soon )", "value": "exit"},
            {"name": "16. Thoát", "value": "exit"},
            
        ],
        'en': [
            {"name": "1. Rubic Swap x Monad Tesnet", "value": "rubic"},
            {"name": "2. Magma Staking x Monad Tesnet", "value": "magma"},
            {"name": "3. Izumi Swap x Monad Tesnet", "value": "izumi"},
            {"name": "4. aPriori Staking x Monad Tesnet", "value": "apriori"},
            {"name": "5. Kintsu Staking x Monad Tesnet", "value": "kintsu"},  # Thêm Kitsu Staking
            {"name": "6. Bean Swap x Monad Tesnet", "value": "bean"},
            {"name": "7. Monorail Swap x Monad Tesnet", "value": "mono"},
            {"name": "8. Bebop Swap x Monad Tesnet", "value": "bebop"},
            {"name": "9. Ambient Finance Swap x Monad Tesnet ( Under maintenance )", "value": "ambient"},
            {"name": "10. Uniswap Swap x Monad Tesnet", "value": "uniswap"},
            {"name": "11. Deploy Contract x Monad Tesnet", "value": "deploy"},
            {"name": "12. Send Random TX or Send TX File Address (address.txt) x Monad Tesnet", "value": "sendtx"},
            {"name": "13. Bima Deposit bmBTC ( Coming soon )", "value": "exit"},
            {"name": "14. Nad domain ( Coming soon )", "value": "exit"},
            {"name": "15. shMONAD Staking ( Coming soon )", "value": "exit"},
            {"name": "16. Thoát", "value": "exit"},
        ]
    }
    return scripts[language]

def run_script(script_module, language):
    """Chạy script bất kể nó là async hay không"""
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
                          message="Chọn script để chạy / Select script to run",
                          choices=[script["name"] for script in available_scripts],
                          carousel=True)
        ]
        answers = inquirer.prompt(questions)
        if not answers:
            continue

        selected_script_name = answers['script']
        selected_script_value = next(script["value"] for script in available_scripts if script["name"] == selected_script_name)

        if selected_script_value == "exit":
            print_border("ĐANG THOÁT / EXITING", Fore.GREEN)
            print(f"{Fore.YELLOW}👋 {'Tạm biệt!' if language == 'vi' else 'Goodbye!'}{Style.RESET_ALL}")
            sys.exit(0)

        try:
            print_border(f"ĐANG CHẠY / RUNNING: {selected_script_name}", Fore.CYAN)
            script_module = importlib.import_module(f"scripts.{selected_script_value}")
            run_script(script_module, language)
            print(f"\n{Fore.GREEN}✔ {'Hoàn thành' if language == 'vi' else 'Completed'} {selected_script_name}{Style.RESET_ALL}")
            input(f"{Fore.YELLOW}⏎ Nhấn Enter để tiếp tục...{Style.RESET_ALL}")
        except ImportError:
            print(f"{Fore.RED}❌ {'Không tìm thấy script' if language == 'vi' else 'Script not found'}: {selected_script_value}{Style.RESET_ALL}")
            input(f"{Fore.YELLOW}⏎ Nhấn Enter để tiếp tục...{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}❌ {'Lỗi' if language == 'vi' else 'Error'}: {str(e)}{Style.RESET_ALL}")
            input(f"{Fore.YELLOW}⏎ Nhấn Enter để tiếp tục...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
