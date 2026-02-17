import socket
from colorama import init, Fore

# 컬러 초기화
init()

target_ip = input("스캔할 IP를 입력하세요 (예: 127.0.0.1): ")
print(f"{Fore.CYAN}--- [{target_ip}] 스캔 시작 ---{Fore.RESET}")

# 자주 쓰는 포트 몇 개만 스캔 (원래는 1~65535)
target_ports = [21, 22, 80, 443, 3306, 8080]

for port in target_ports:
    try:
        # 소켓 생성 (IPv4, TCP)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1) # 1초 안에 응답 없으면 패스
        
        # 접속 시도
        result = sock.connect_ex((target_ip, port))
        
        if result == 0:
            print(f"{Fore.GREEN}[+] Port {port}: OPEN{Fore.RESET}")
        else:
            print(f"{Fore.RED}[-] Port {port}: CLOSED{Fore.RESET}")
            
        sock.close()
    except Exception as e:
        print(f"Error: {e}")

print(f"{Fore.CYAN}--- 스캔 완료 ---{Fore.RESET}")