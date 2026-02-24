import socket
from colorama import init, Fore

init(autoreset=True)

target_ip = input("스캔할 IP를 입력하세요 (예: 127.0.0.1): ")
print(f"{Fore.CYAN}--- [{target_ip}] 배너 그래빙 스캔 시작 ---{Fore.RESET}")

target_ports = [21, 22, 80, 135, 443, 445, 3306, 8080, 11434]

for port in target_ports:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2) # 타임아웃을 조금 넉넉히 2초로

        result = sock.connect_ex((target_ip, port))

        if result == 0:
            try:
                service = socket.getservbyport(port, 'tcp')
            except:
                service = "Unknown"

            # 출력할 때 서비스 이름도 같이 보여줌
            print(f"{Fore.GREEN}[+] Port {port} ({service}): OPEN{Fore.RESET}")

            try:
                # [핵심 수정] 1. 먼저 말을 건넨다! (가장 무난한 HTTP 요청)
                # "야, 너 누구야?" 라고 찔러보는 패킷
                msg = b"GET / HTTP/1.1\r\nHost: " + target_ip.encode() + b"\r\n\r\n"
                sock.send(msg)

                # 2. 대답을 듣는다
                banner = sock.recv(1024)

                # 3. 깨짐 방지 (SMB 같은 애들은 이상한 문자 보내므로 ignore 처리)
                print(f" -> {Fore.YELLOW}{banner.decode('utf-8', errors='ignore').strip()[:50]}...{Fore.RESET}")

            except:
                print(f" -> {Fore.WHITE}(응답 없음){Fore.RESET}")
        else:
            print(f"{Fore.RED}[-] Port {port}: CLOSED{Fore.RESET}")

        sock.close()
    except Exception as e:
        print(f"Error: {e}")

print(f"{Fore.CYAN}--- 스캔 완료 ---{Fore.RESET}")