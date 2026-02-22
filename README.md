

📚 [프로젝트 결산] 파이썬 기반 고속 포트 스캐너 개발 및 보안 점검 도구화
1. 프로젝트 개요
네트워크 보안의 첫걸음인 '포트 스캐닝(Port Scanning)'의 원리를 이해하고, 파이썬을 이용해 단일 소켓 통신부터 멀티스레딩 기반의 고속 병렬 스캔, 그리고 취약점 탐지까지 수행하는 자동화 CLI 도구를 개발함.

2. 핵심 단계별 학습 내용 및 구현 기술
Phase 1: 네트워크 소켓 통신과 배너 그래빙 (Socket & Banner Grabbing)
TCP 연결 원리 파악: socket 모듈의 connect_ex() 함수를 사용하여 3-Way Handshake 기반의 TCP 연결 가능 여부를 확인하고, 포트의 개방(OPEN)/폐쇄(CLOSED) 상태를 판별함.

서비스 식별 (Service Identification): socket.getservbyport()를 통해 표준 포트 번호에 매핑된 서비스 이름(예: 445 -> microsoft-ds)을 조회하는 방식을 구현.

배너 그래빙 (Banner Grabbing): 포트가 열려있을 때 능동적으로 페이로드(예: GET / HTTP/1.1)를 보내고 recv()로 서버의 응답(버전 정보 등)을 읽어오는 해킹의 기본 정보 수집(Reconnaissance) 기법을 실습함.

Phase 2: CLI 도구화 (Command Line Interface)
표준화된 도구 설계: 스크립트 실행 중 입력을 기다리는 동기적 input() 방식의 한계를 벗어나, argparse 모듈을 도입하여 실행과 동시에 인자값을 전달받도록 개선.

자동화 친화적 구조: -t (타겟 IP), -p (포트 범위) 옵션과 -h (도움말) 기능을 구현하여 다른 셸 스크립트나 데브옵스 환경에서 파이프라인으로 연결하기 쉬운 형태로 발전시킴.

Phase 3: 멀티스레딩을 통한 성능 극대화 (Multi-Threading)
동시성(Concurrency) 제어: 단일 스레드(Single-Thread) 순차 탐색 시 발생하는 극심한 병목 현상(I/O Bound)을 해결하기 위해 concurrent.futures.ThreadPoolExecutor를 도입.

100배의 성능 향상 증명: 100개의 스레드(Worker)를 스레드 풀(Thread Pool)에 할당하여 병렬 처리를 구현한 결과, 1,000개의 포트 스캔을 약 1000초에서 단 10초 내외로 단축시키는 압도적인 성능 최적화를 경험함.

Phase 4: 취약점 분석 로직 통합 (Vulnerability Scanning)
보안 위협 탐지 메커니즘: 단순 상태 점검을 넘어, 잘 알려진 해킹 타겟 포트(예: 135번 RPC, 445번 SMB 등)에 대한 딕셔너리(사전) 기반의 블랙리스트를 구성.

실시간 경고 시스템: 스캔 결과와 블랙리스트를 대조하여, 위험 포트 개방 시 즉각적인 경고 메시지와 그 이유를 출력하는 취약점 스캐너의 기본 아키텍처를 완성.

3. 트러블슈팅 및 개발 환경 관리 (DevOps/Infra)
의존성 및 가상환경 관리 (uv): 파이썬의 최신 패키지 매니저인 uv를 활용하여 격리된 가상환경(.venv)을 구축하고 빠르고 안전하게 라이브러리를 관리함.

운영체제 레벨 오류 해결: DLL 의존성 누락으로 인한 Exit Code 1 (-1073741515) 발생 시, 가상환경을 파기하고 Python 엔진 버전을 강제 고정(pin 3.12)하여 재구축(Immutable Infrastructure 개념 적용)함으로써 깔끔하게 문제를 해결함.

버전 관리 (Git): git commit --date를 활용한 커밋 기록 관리 및 Staging(add), Push 워크플로우를 숙달함.
