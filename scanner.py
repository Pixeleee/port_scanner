import socket
import argparse  # [추가] 명령어 인자값을 처리하는 라이브러리
import concurrent.futures # [추가] 분신술을 쓰기 위한 모듈
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

# 범위를 입력받는 기능 추가! (예: 1-1000)
if '-' in args.ports:
    start, end = map(int, args.ports.split('-'))
    target_ports = list(range(start, end + 1))
else:
    target_ports = [int(p.strip()) for p in args.ports.split(',')]
# ----------------------------------------------------------------

VULNERABLE_PORTS = {
    21: "FTP (암호화 안 됨! 비밀번호 도청 위험)",
    23: "Telnet (절대 사용 금지! 해킹 1순위)",
    135: "RPC (시스템 정보 유출 가능성)",
    445: "SMB (워너크라이 랜섬웨어 단골 타겟. 외부 노출 금지!)",
    3389: "RDP (원격 데스크톱. 무차별 대입 공격 주의)"
}

# [핵심 1] 작업 지시서(함수) 만들기
# 일꾼 한 명이 포트 한 개를 맡아서 실행할 코드입니다.
def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # 속도가 생명이니 타임아웃은 1초!
        result = sock.connect_ex((ip, port))

        if result == 0:
            try:
                service = socket.getservbyport(port, 'tcp')
            except:
                service = "Unknown"

            # 주의: 다중 스레드에서는 화면이 엉킬 수 있어서 배너 가져오기는 일단 뺐습니다.
            print(f"{Fore.GREEN}[+] Port {port} ({service}): OPEN{Fore.RESET}")

            # 2. [추가] 만약 열린 포트가 블랙리스트에 있다면? 빨간색 경고 날리기!
            if port in VULNERABLE_PORTS:
                print(f" └── {Fore.RED}[🚨 취약점 경고] {VULNERABLE_PORTS[port]}{Fore.RESET}")

        sock.close()
    except Exception:
        pass


# --- 메인 실행 파트 ---
print(f"{Fore.CYAN}--- [{target_ip}] 멀티스레드 스캔 시작 (대상 포트: {len(target_ports)}개) ---{Fore.RESET}")
start_time = datetime.now()  # 스캔 시작 시간 기록

# [핵심 2] 일꾼 100명 고용해서 동시에 일 시키기!
# max_workers가 일꾼의 수입니다. (너무 많으면 컴퓨터가 힘들어해요)
with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    for port in target_ports:
        # 일꾼에게 (함수이름, IP, 포트)를 던져주면 알아서 동시에 실행합니다.
        executor.submit(scan_port, target_ip, port)

end_time = datetime.now()  # 스캔 종료 시간 기록
print(f"{Fore.CYAN}--- 스캔 완료 (소요 시간: {end_time - start_time}) ---{Fore.RESET}")