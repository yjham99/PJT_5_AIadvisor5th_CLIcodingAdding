# Jules 연동 및 활용 전략 (Project Antigravity)

## 1. 개요 (Overview)
본 문서는 자율 AI 코딩 에이전트 **Jules**를 우리 워크플로우에 통합하기 위한 전략을 담고 있습니다.
- **미션**: 단순 반복 코딩 작업은 Jules에게 위임하여 생산성을 극대화하고, 코다리(에이전트 매니저)는 설계와 관리 감독에 집중한다.
- **핵심 컨셉**: "코다리가 설계하면, Jules가 구현한다."

## 2. 역할 정의 (Role Definition)
| 에이전트 | 역할 | 책임 및 임무 |
| :--- | :--- | :--- |
| **대표님 (CEO)** | 사령관 (Commander) | 큰 그림의 목표(Goal) 설정 및 최종 결과물 승인. |
| **코다리 (Manager)** | 설계자 & 감독관 | 작업 단위를 쪼개고, Jules에게 업무를 하달하며, PR을 리뷰하고, 저장소를 관리. |
| **Jules (Worker)** | 자율 개발자 | 실제 코딩 수행, 빌드/테스트 실행, Pull Request(PR) 생성. (묵묵히 일함) |

## 3. 환경 구축 계획 (Environment Setup Plan)
Jules를 부려먹기(?) 위해서는 로컬 환경, 구글 클라우드, 그리고 GitHub 간의 연결 통로를 뚫어야 합니다.

### 3.1. 필수 준비물 (Prerequisites)
- [ ] **GitHub 저장소**: Jules와 연동할 타겟 저장소가 있어야 합니다.
- [ ] **Jules 접근 권한**: [jules.google.com](https://jules.google.com)에 접속 가능한지 확인 필요.
- [ ] **Gemini CLI (선택)**: 터미널에서 직접 명령을 내리려면 필요합니다.

### 3.2. 연동 단계 (Integration Steps)
1.  **Git 초기화 (필수)**:
    *   로컬 저장소 생성: `git init` (완료).
    *   **원격 저장소 연결**: GitHub 웹사이트에서 새 저장소(`PJT_5_AIadvisor5th_CLIcodingAdding`) 생성 후, `git remote add origin <URL>` 명령으로 연결.
    *   **초기 커밋**: `git add .` -> `git commit -m "Initial commit"` -> `git push -u origin main`.
2.  **저장소 연결**: 타겟 GitHub 저장소에 "Google Jules" GitHub App을 설치합니다.
3.  **CLI 설정**:
    *   설치: `npm install -g @google/jules` (Verified).
    *   인증: `jules login` 명령어로 구글 계정 인증.
    *   **GitHub 연동 (필수)**: [이곳](https://github.com/apps/google-labs-jules/installations/select_target)에서 Jules가 접근할 저장소를 선택해야 합니다.
    *   연동: `jules new "Initial Setup"` 명령어로 테스트 세션 시작.

## 4. 운영 시나리오 (Operational Workflow)
### 상황: "유틸리티 모듈 리팩토링"
1.  **명령 (Command)**: 대표님이 코다리에게 지시합니다. "유틸리티 폴더 좀 깔끔하게 정리해."
2.  **위임 (Delegation)**: 코다리가 작업을 분석하고 Jules에게 명령을 내립니다.
    ```bash
    jules run "utils 폴더를 파일 입출력과 데이터 처리 로직으로 분리해서 리팩토링해줘. 다 되면 PR 올려."
    ```
3.  **실행 (Execution)**: Jules가 클라우드 상에서 `refactor/utils` 브랜치를 따고 작업을 시작합니다.
4.  **보고 (Notification)**: Jules가 "작업 완료! PR 생성했습니다."라고 보고합니다.
5.  **검토 (Review)**: 코다리(또는 대표님)가 PR 내용을 확인합니다.
    *   *코다리의 센스*: `gh pr diff`로 변경 사항을 미리 요약해서 대표님께 브리핑합니다.
6.  **병합 (Merge)**: 대표님 승인 떨어지면 병합(Merge) 완료!

## 5. 효율 극대화 전략 (The "Kodari Protocol")
- **배치 처리 (Batch Processing)**: 자잘한 수정 사항(주석 추가, 들여쓰기 교정 등)은 모아서 한 방에 Jules에게 시킵니다.
- **TDD 위임 (Test-Driven Delegation)**: "기능 구현하기 전에 테스트 코드부터 짜봐"라고 시켜서 코드 품질을 높입니다.
- **문서화 봇**: 스프린트 끝날 때마다 "전체 코드 읽고 README.md 최신화해"라고 시키면 문서화 스트레스 끝!

## 6. 다음 단계 (Next Steps)
1.  **설치 완료 확인**: `npm install` 성공 여부 확인.
2.  **GitHub Repo 생성**: 웹에서 생성 후 로컬 연결.
3.  **인증 및 테스트**: `jules login` -> **GitHub App 설치** -> `jules new "Test Mission"` -> 탐색.
