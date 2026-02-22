import socket
import argparse  # [추가] 명령어 인자값을 처리하는 라이브러리
from datetime import datetime
from colorama import init, Fore

init(autoreset=True)

# ---------------- [CLI 설정 파트] ----------------
# 1. 파서 객체 생성 (프로그램 설명서 쓰기)
parser = argparse.ArgumentParser(description="나만의 짱 쎈 포트 스캐너 (v1.1)")

# 2. 옵션 추가하기 (단축어, 원래이름, 필수여부, 도움말)
parser.add_argument('-t', '--target', required=True, help="스캔할 타겟 IP 주소 (예: 127.0.0.1)")
parser.add_argument('-p', '--ports', default="21,22,80,135,443,445,3306,8080,11434", help="스캔할 포트 번호들 (쉼표로 구분)")

# 3. 사용자가 터미널에 친 명령어 읽어오기
args = parser.parse_args()

target_ip = args.target

# "80,443" 같은 문자열을 잘라서 [80, 443] 같은 정수 리스트로 변환
try:
    target_ports = [int(p.strip()) for p in args.ports.split(',')]
except ValueError:
    print(f"{Fore.RED}[오류] 포트는 숫자와 쉼표로만 입력해야 합니다!{Fore.RESET}")
    exit(1)
# -------------------------------------------------

print(f"{Fore.CYAN}--- [{target_ip}] 스캔 시작 (대상 포트: {len(target_ports)}개) ---{Fore.RESET}")

for port in target_ports:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2) # 타임아웃을 조금 넉넉히 2초로
        
        result = sock.connect_ex((target_ip, port))
        #123
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

                ## 참고로, 일부 서비스는 아무런 패킷을 보내지 않아도 배너를 보내주는 경우가 많습니다.
                
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