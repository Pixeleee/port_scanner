# Python Port Scanner & Banner Grabber (v1.1)


[![Docker Build and Push](https://github.com/Pixeleee/port_scanner/actions/workflows/main.yml/badge.svg)](https://github.com/Pixeleee/port_scanner/actions/workflows/main.yml)
<div align="left">
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/Socket-000000?style=flat-square"/>
</div>

<br>

## 프로젝트 소개
Python의 소켓(Socket) 통신을 활용하여 타겟 IP의 열려있는 포트를 확인하고, 취약점 포트(SMB, RPC 등)를 자동으로 식별하여 경고해 주는 CLI 기반 네트워크 보안 유틸리티입니다.

멀티스레딩(Multi-threading)을 적용해 스캔 속도를 획기적으로 단축했으며, **Docker** 컨테이너화를 통해 파이썬이나 가상환경 세팅 없이 언제 어디서나 즉각적으로 실행 가능한 완벽한 이식성을 구현했습니다.

## 주요 기능
- **고속 병렬 스캐닝**: `concurrent.futures`의 ThreadPoolExecutor를 활용한 멀티스레드 기반 초고속 포트 스캔
- **CLI 인터페이스**: `argparse`를 활용한 직관적인 명령어 및 옵션(`-t`, `-p`) 지원
- **취약점 자동 경고**: 열린 포트 중 보안 위협이 높은 포트(FTP, Telnet, SMB, RDP 등) 감지 시 시각적 경고(🚨) 출력
- **서비스 이름 식별**: `getservbyport`를 활용하여 지정된 포트 번호에 할당된 서비스 이름 매칭
- **완벽한 컨테이너화**: `ENTRYPOINT` 기반의 Docker 이미지로 패키징하여 호스트 환경과 격리된 실행 지원

## 시작하기 (Getting Started)

### Docker로 즉시 실행하기 (Recommended)
파이썬 설치가 필요 없습니다. Docker만 있다면 아래 명령어 한 줄로 스캐너를 실행할 수 있습니다.

```bash
# 기본 스캔 (주요 포트 스캔)
docker run -it pixelee/port-scanner:v1.1 -t [타겟IP]

# 예시: 로컬 호스트(현재 내 컴퓨터) 스캔
docker run -it pixelee/port-scanner:v1.1 -t host.docker.internal

# 특정 포트 지정 스캔
docker run -it pixelee/port-scanner:v1.1 -t host.docker.internal -p 80,443,445

📝 개발 기록 (Velog)
프로젝트를 진행하며 겪은 트러블슈팅과 기술적 고민을 블로그에 기록했습니다.

https://velog.io/@pixeleee/%EB%AF%B8%EB%8B%88-%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8-%ED%8F%AC%ED%8A%B8%EC%8A%A4%EC%BA%90%EB%84%881


