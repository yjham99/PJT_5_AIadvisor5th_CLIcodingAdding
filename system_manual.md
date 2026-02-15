# 스마트 모델 스케줄러 (Smart Model Scheduler) 가이드

이 시스템은 구글 GenAI(Gemini) 모델의 무료 티어 한도를 효율적으로 관리하며, 자동으로 최적의 모델을 선택해주는 Python 스크립트입니다.

## 1. 개요
- **목적**: 무료로 제공되는 API 호출량(RPM, RPD)을 최대한 활용하고, 한도 초과 시 자동으로 다른 모델로 전환하여 중단 없는 서비스를 제공합니다.
- **사용 라이브러리**: `google-genai` (구글 공식 최신 SDK)
- **지원 모델**:
    1. **Gemini 2.0 Flash** (메인, 빠름)
    2. **Gemini 2.0 Pro Experimental** (고성능, 서브)
    3. **Gemini 1.5 Flash** (안정적 구버전)
    4. **Gemini 1.5 Pro** (고성능 백업)

## 2. 설치 방법

### 2.1. 필수 프로그램 확인
Python 3.9 이상이 설치되어 있어야 합니다. (현재 시스템은 3.14 버전 확인됨)

### 2.2. 라이브러리 설치
터미널에서 아래 명령어를 실행하여 필수 패키지를 설치합니다.
```bash
pip install google-genai python-dotenv
```

## 3. 설정 (Configuration)

### 3.1. API 키 발급
1. [Google AI Studio](https://aistudio.google.com/)에 접속합니다.
2. **Get API key**를 클릭하여 키를 생성합니다. (무료 티어 선택)

### 3.2. 환경 변수 파일 생성 (.env)
프로젝트 폴더(`c:\PJT4AIadvisor5th`)에 `.env` 파일을 만들고 아래 내용을 붙여넣으세요.
(`YOUR_API_KEY` 부분에 발급받은 키를 넣어야 합니다.)

```ini
GOOGLE_API_KEY=YOUR_API_KEY_HERE
```

## 4. 사용법 (Usage)

### 4.1. 기본 실행 (테스트)
`model_scheduler.py` 파일을 직접 실행하면 내장된 테스트 코드가 작동합니다.

```bash
python model_scheduler.py
```
- **성공 시**: "Gemini Smart Scheduler Test" 메시지와 함께 AI의 답변이 출력됩니다.
- **실패 시**: 에러 메시지가 출력되며, `.env` 파일이나 키를 확인해야 합니다.

### 4.2. 내 코드에서 사용하기
다른 Python 스크립트에서 이 스케줄러를 불러와 사용할 수 있습니다. 이 시스템은 비동기(async) 방식으로 작동하므로 `await`와 함께 사용해야 합니다.

```python
import asyncio
from model_scheduler import GeminiSmartScheduler

async def main():
    # 스케줄러 초기화
    scheduler = GeminiSmartScheduler()

    # 질문하기
    response = await scheduler.generate_content("오늘 서울 날씨 어때?")
    print(response)

# 비동기 실행
asyncio.run(main())
```

## 5. 작동 원리 (알고리즘)
1. 요청이 들어오면 **우선순위 1위 모델(Gemini 2.0 Flash)**부터 확인합니다.
2. **일일 한도(RPD)**를 넘지 않았는지 체크합니다.
3. **분당 속도(RPM)** 제한에 걸리지 않도록 필요시 잠시 대기합니다. (비동기 락 적용)
4. 호출이 실패하거나 한부가 초과되면, 즉시 **다음 순위 모델**로 넘어갑니다.
5. 모든 모델이 실패할 경우에만 에러를 반환합니다.

## 6. 추가 자동화 모듈 (Optional)

### 6.1. 키움 증권 로그인 (`kiwoom_login.py`)
키움 증권 Open API와의 연동을 위한 로그인 모듈입니다.
- **실행 경로**: `C:\OpenAPI\opstarter.exe` (사용자 설정에 따라 수정 가능)
- **주요 기능**: 자동 로그인 실행 및 상태 확인

### 6.2. NotebookLM 자동화 프로세스
데이터 분석부터 NotebookLM 저장까지의 전 과정을 자동화합니다.
- `data_analyzer.py`: 업로드된 CSV 파일을 분석하여 리포트 생성
- `notebooklm_client.py`: 분석 결과를 NotebookLM에 비동기 일괄 저장
- `automation_orchestrator.py`: 전체 파이프라인(로그인 -> 분석 -> 저장) 관리

---
**주의사항**:
- 무료 티어는 공용 자원을 사용하므로, 간혹 예고 없이 429(Too Many Requests) 에러가 발생할 수 있습니다.
- 키움 증권 모듈은 Windows 환경에서 정상 작동하며, Linux 환경에서는 시뮬레이션 모드로 동작합니다.
