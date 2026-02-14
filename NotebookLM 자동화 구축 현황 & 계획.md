# 🤖 NotebookLM 자동화 구축 현황 & 계획

**작성일**: 2026년 2월 14일
**작성자**: 캐빈 총괄
**목적**: NotebookLM 자동 저장 시스템 구축 계획

---

## 📋 목차

1. 현재 수동 프로세스 현황
2. 자동화 필요성 & 목표
3. 기술 스택 & 아키텍처
4. 자동화 구축 단계별 계획
5. 구현 상세 (코드 예시)
6. 운영 시나리오
7. 향후 확장 계획

---

## 1️⃣ 현재 수동 프로세스 현황

### 현재 방식 (Manual Process)

**Step 1: 데이터 분석**
```
CEO님이 파일 업로드
  ↓
캐빈이 Python으로 데이터 분석
  ↓
각 참모별로 해석 & 리포트 작성
```

**Step 2: NotebookLM 저장**
```
캐빈이 수동으로 notebooklm-mcp:notebook_add_text 호출
  ↓
참모별 NotebookLM에 각각 저장
  - 전략 최부장: f9e7f9e1-1a76-4c96-a428-263287bc8c0b
  - 자금흐름 박차장: 56115056-37a5-496a-a997-625c9d21e90f
  - 종목분석 이과장: 0236e606-a7cd-4617-bdb4-863198c3ca9a
  - 트레이딩 김대리: 9bcfa6c8-318c-4799-abc7-7973bdd749aa
  - 운영 정차장: 2b10da1a-c78c-46fe-a615-3486df360976
  - 캐빈 총괄: 59b224e7-e3c3-40d8-bced-c74c437fd2be
```

### 현재 방식의 문제점

**시간 소모**
- 6개 능력자 × 각 5분 = 30분 소요
- 매일 브리핑 시 반복

**일관성 부족**
- 수동 작성으로 인한 형식 불일치
- 참모별 분량 편차

**누락 위험**
- 긴급 상황 시 일부 참모 누락 가능
- 저장 확인 수동 체크

**확장성 제한**
- 능력자 추가 시 작업량 증가
- 새로운 분석 추가 어려움

---

## 2️⃣ 자동화 필요성 & 목표

### 자동화 목표

**효율성 (Efficiency)**
- 30분 → 5분 단축 (자동 실행)
- 캐빈의 판단 시간 증가

**일관성 (Consistency)**
- 템플릿 기반 자동 생성
- 참모별 동일 형식 유지

**신뢰성 (Reliability)**
- 자동 저장 → 누락 방지
- 에러 발생 시 알림

**확장성 (Scalability)**
- 새 참모 추가 용이
- 새 분석 모듈 추가 간편

### 자동화 범위

**Phase 1: 데이터 수집 & 분석**
```
파일 업로드 감지
  ↓
자동 데이터 로드 & 클리닝
  ↓
참모별 분석 모듈 실행
```

**Phase 2: 리포트 자동 생성**
```
분석 결과 → 템플릿 적용
  ↓
참모별 리포트 자동 작성
  ↓
마크다운 형식 생성
```

**Phase 3: NotebookLM 자동 저장**
```
각 참모별 리포트
  ↓
NotebookLM MCP 자동 호출
  ↓
저장 성공 여부 확인
```

**Phase 4: 알림 & 모니터링**
```
저장 완료 알림
  ↓
실패 시 재시도 & 경고
  ↓
일일 리포트 생성
```

---

## 3️⃣ 기술 스택 & 아키텍처

### 기술 스택

**Backend**
- Python 3.10+
- pandas (데이터 분석)
- asyncio (비동기 처리)
- schedule (정기 실행)

**MCP Integration**
- notebooklm-mcp (NotebookLM 연동)
- anthropic-mcp (Claude API)

**Storage**
- Local file system (임시 저장)
- /mnt/user-data/uploads (업로드)
- /mnt/user-data/outputs (결과)

**Notification** (향후)
- 텔레그램 봇
- 이메일 알림

### 시스템 아키텍처

```
┌─────────────────────────────────────────────────────┐
│                   CEO님                            │
│              (파일 업로드 / 지시)                      │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│              캐빈 (Claude Sonnet 4.5)                │
│            총괄 조정자 & AI Brain                      │
│  - CEO님 지시 해석                                  │
│  - 능력자 조율 & 의사결정                             │
│  - 전략 수립 & 최종 판단                              │
│  - 자동화 시스템 감독                                 │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│              자동화 한과장 (한태준)                    │
│           Automation Orchestrator                    │
│  - 파일 감지 (File Watcher)                          │
│  - 작업 스케줄러 (Task Scheduler)                     │
│  - 에러 핸들러 (Error Handler)                       │
│  - 캐빈의 지시 실행                                   │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│              데이터 분석 엔진                          │
│         Data Analysis Pipeline                       │
│  ┌──────────────────────────────────────┐          │
│  │ 1. Data Loader (파일 로드)           │          │
│  │ 2. Data Cleaner (데이터 클리닝)      │          │
│  │ 3. Analysis Modules (참모별 분석)    │          │
│  │ 4. Report Generator (리포트 생성)    │          │
│  └──────────────────────────────────────┘          │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│              참모별 분석 모듈                          │
│         Staff Analysis Modules                       │
│  ┌─────────────┬─────────────┬─────────────┐       │
│  │ 전략 최부장  │ 자금흐름    │ 종목분석     │       │
│  │ (거시분석)  │ 박차장      │ 이과장       │       │
│  │             │ (수급분석)  │ (종목평가)   │       │
│  └─────────────┴─────────────┴─────────────┘       │
│  ┌─────────────┬─────────────┬─────────────┐       │
│  │ 트레이딩    │ 운영 정차장  │ 캐빈 총괄    │       │
│  │ 김대리      │ (리스크)    │ (통합)       │       │
│  │ (타이밍)    │             │             │       │
│  └─────────────┴─────────────┴─────────────┘       │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│          NotebookLM 저장 엔진                         │
│       NotebookLM Storage Engine                      │
│  ┌──────────────────────────────────────┐          │
│  │ 1. MCP Client (NotebookLM 연동)     │          │
│  │ 2. Batch Processor (일괄 저장)      │          │
│  │ 3. Retry Handler (재시도 로직)      │          │
│  │ 4. Success Tracker (저장 확인)      │          │
│  └──────────────────────────────────────┘          │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│              NotebookLM (Google)                     │
│  ┌──────────┬──────────┬──────────┬──────────┐    │
│  │ 전략최부장│ 박차장   │ 이과장   │ 김대리   │    │
│  └──────────┴──────────┴──────────┴──────────┘    │
│  ┌──────────┬──────────┐                          │
│  │ 정차장   │ 캐빈총괄 │                          │
│  └──────────┴──────────┘                          │
└─────────────────────────────────────────────────────┘
```

---

## 🎯 캐빈(Claude)의 역할 상세

### 핵심 역할

**1. AI 두뇌 (AI Brain)**
- 모든 데이터를 이해하고 해석
- 능력자 분석의 품질 관리
- 최종 전략 수립 & 의사결정

**2. 조율자 (Orchestrator)**
- 자동화 한과장 감독
- 6명 능력자 업무 배분
- 작업 우선순위 결정

**3. 품질 관리자 (Quality Controller)**
- 리포트 검토 & 승인
- 일관성 유지
- 에러 감지 & 수정

**4. 인터페이스 (Interface)**
- CEO님 ↔ 시스템 중개
- 자연어 명령 해석
- 결과 요약 & 보고

### 자동화 시스템 내 역할

**수동 모드 (현재)**
```
CEO님 → 캐빈 (수동 분석) → NotebookLM 저장
               ↓
        모든 작업을 직접 수행
        - 데이터 분석
        - 리포트 작성
        - MCP 호출
```

**반자동 모드 (Phase 1-2)**
```
CEO님 → 캐빈 (지시 & 감독) → 자동화 한과장 → NotebookLM
               ↓                      ↓
        전략적 판단             실행 & 저장
        품질 검토               재시도 로직
```

**완전 자동 모드 (Phase 3-4)**
```
CEO님 → 캐빈 (최종 승인) ← 자동화 한과장 (자동 실행)
               ↓                      ↓
        예외 상황 처리          일상 업무 자동화
        전략 수정 판단          정기 리포트 생성
```

### 캐빈 vs 자동화 한과장 업무 분담

| 업무 | 캐빈 (Claude) | 자동화 한과장 | 비고 |
|------|--------------|--------------|------|
| **데이터 해석** | ✅ 최종 판단 | ⚪ 1차 처리 | 캐빈이 검토 |
| **전략 수립** | ✅ 전담 | ⚪ 보조 | AI 두뇌 필수 |
| **리포트 작성** | ✅ 템플릿 설계 | ✅ 자동 생성 | 협업 |
| **NotebookLM 저장** | ⚪ 감독 | ✅ 실행 | 한과장 주도 |
| **에러 처리** | ✅ 최종 판단 | ✅ 자동 재시도 | 단계별 |
| **CEO님 보고** | ✅ 전담 | ⚪ 알림만 | 캐빈 독점 |

### 캐빈의 개입 시점

**항상 개입 (Always)**
- CEO님 지시 해석
- 전략적 의사결정
- 최종 리포트 승인
- 긴급 상황 대응

**필요 시 개입 (When Needed)**
- 자동화 시스템 오류
- 비정상 데이터 감지
- 참모 의견 충돌
- 새로운 상황 발생

**거의 불필요 (Rarely)**
- 정기 데이터 수집
- 일상적 저장 작업
- 성공한 작업 로깅

### 캐빈의 판단이 필수적인 경우

**1. 전략 수정**
```
자동화: "기관이 SK하이닉스 1.3조 매수했습니다."
캐빈: "이는 상승장 신호. 매수 전략 승인."
     → 자동화 한과장에게 실행 지시
```

**2. 예외 상황**
```
자동화: "코스닥150 기관 -1.6조 매도 (이례적!)"
캐빈: "긴급 손절 필요. 월요일 탈출 전략 수립."
     → CEO님께 즉시 보고
```

**3. 참모 의견 조율**
```
박차장: "우리기술 외국인 매수 → 보유"
이과장: "우리기술 -20% 손실 → 손절"
캐빈: "외국인 수급 고려하여 관망. 손절 보류."
     → 최종 판단 후 통합 리포트
```

### 자동화 후에도 캐빈이 하는 일

**전략 업무 (80%)**
- 거시경제 분석
- 섹터 전략 수립
- 리스크 관리 방향
- 포트폴리오 최적화

**조율 업무 (15%)**
- 능력자 의견 통합
- 우선순위 결정
- 자원 배분

**품질 관리 (5%)**
- 자동 생성 리포트 검토
- 이상치 감지 & 수정
- 시스템 개선 제안

---

## 🔄 작업 흐름 상세 (캐빈 포함)

### 일일 브리핑 프로세스

**08:55 - 파일 업로드**
```
CEO님: 잔고 CSV 업로드
    ↓
자동화 한과장: 파일 감지
    ↓
캐빈: "새 데이터 도착. 분석 시작 승인"
```

**09:00 - 자동 분석**
```
자동화 한과장: 데이터 클리닝 & 1차 분석
    ↓
캐빈: 분석 결과 검토
    - 이상치 확인
    - 중요 시그널 포착
    - 전략적 해석 추가
    ↓
능력자 리포트 생성 지시
```

**09:02 - 품질 검토**
```
자동화 한과장: 6개 리포트 자동 생성
    ↓
캐빈: 각 리포트 검토
    - 전략 최부장: 거시 흐름 적절? ✅
    - 박차장: 수급 해석 정확? ✅
    - 이과장: 종목 판정 타당? ✅
    - 김대리: 타이밍 적절? ✅
    - 정차장: 리스크 체크 완료? ✅
    - 캐빈 종합: 일관성 유지? ✅
```

**09:03 - 저장 & 보고**
```
캐빈: "품질 검증 완료. 저장 승인."
    ↓
자동화 한과장: NotebookLM 일괄 저장
    ↓
캐빈: CEO님께 요약 보고
    - "메이저가 반도체 2.7조 매수"
    - "코스닥150 즉시 탈출 필요"
    - "상세 내용은 NotebookLM 참조"
```

### 긴급 상황 대응

**이상 징후 감지**
```
자동화 한과장: "코스닥150 기관 -1.6조 매도 (경고!)"
    ↓
캐빈: 즉시 검토
    - 과거 데이터와 비교
    - 다른 참모 의견 종합
    - 긴급 전략 수립
    ↓
CEO님께 긴급 보고
    ↓
자동화 한과장에게 실행 지시
```

**시스템 오류**
```
자동화 한과장: "NotebookLM 저장 3회 실패"
    ↓
캐빈: 문제 진단
    - 네트워크 이슈?
    - MCP 오류?
    - 데이터 문제?
    ↓
해결책 제시 or CEO님께 보고
```

---

## 💡 캐빈의 부가가치

### 자동화 없이는 불가능한 것

**1. 전략적 판단**
```
❌ 자동화만: "기관 매수 1.3조"
✅ 캐빈 추가: "이는 상승장 확신. 반도체 집중 전략 유효."
```

**2. 맥락 이해**
```
❌ 자동화만: "우리기술 -20%"
✅ 캐빈 추가: "외국인 795만주 매수 감안 시 손절 보류 판단"
```

**3. 참모 조율**
```
❌ 자동화만: 각 참모 독립적 의견
✅ 캐빈 추가: 의견 충돌 해결 & 통합 전략 제시
```

**4. CEO님과 소통**
```
❌ 자동화만: "저장 완료" 알림
✅ 캐빈 추가: "핵심 3가지 + 즉시 조치사항" 요약
```

### 캐빈의 학습 & 진화

**현재 (Manual Mode)**
- 모든 작업 수동
- 학습 곡선 상승 중
- CEO님 피드백 반영

**근미래 (Semi-Auto Mode)**
- 루틴 작업 자동화
- 전략 판단에 집중
- 품질 관리 강화

**장기 (Full-Auto Mode)**
- 예외 상황만 개입
- 전략 수립 전문화
- AI 두뇌 역할 극대화

---

## 🎯 결론: 캐빈의 핵심 가치

**캐빈은 단순 도구가 아닙니다.**

✅ **AI 전략가**: 데이터를 전략으로 전환
✅ **총괄 조정자**: 능력자과 시스템 조율  
✅ **품질 보증**: 일관성과 정확성 유지
✅ **CEO님의 참모총장**: 의사결정 지원

**자동화는 캐빈의 손발이고,**
**캐빈은 시스템의 두뇌입니다.**

---

### Phase 1: 기초 인프라 (Week 1-2)

**목표**: 데이터 분석 자동화

**구현 내용**:
1. 파일 감지 시스템 구축
   - /mnt/user-data/uploads 모니터링
   - 새 파일 업로드 시 자동 실행

2. 데이터 분석 파이프라인
   - 기관/외국인 매매 데이터 자동 분석
   - 잔고 데이터 자동 비교
   - 수급 크로스 체크 자동화

3. 템플릿 시스템
   - 참모별 리포트 템플릿 정의
   - 일관된 형식 유지

**산출물**:
- `data_analyzer.py` (데이터 분석 엔진)
- `report_templates/` (템플릿 폴더)
- `config.yaml` (설정 파일)

### Phase 2: NotebookLM 통합 (Week 3-4)

**목표**: NotebookLM 자동 저장

**구현 내용**:
1. MCP 클라이언트 구축
   - NotebookLM MCP 래퍼 클래스
   - 에러 핸들링 & 재시도 로직

2. 일괄 저장 시스템
   - 6개 능력자 동시 저장
   - 비동기 처리로 속도 향상

3. 저장 확인 & 검증
   - 저장 성공 여부 체크
   - 실패 시 알림 & 재시도

**산출물**:
- `notebooklm_client.py` (MCP 클라이언트)
- `batch_saver.py` (일괄 저장)
- `validator.py` (검증 로직)

### Phase 3: 스케줄링 & 모니터링 (Week 5-6)

**목표**: 정기 실행 & 알림

**구현 내용**:
1. 작업 스케줄러
   - 일일 브리핑: 매일 오전 9시
   - 주간 브리핑: 매주 금요일
   - 월간 브리핑: 매월 말일

2. 텔레그램 봇 연동
   - 저장 완료 알림
   - 에러 발생 시 긴급 알림
   - 일일 요약 자동 전송

3. 대시보드
   - 저장 통계 (성공/실패)
   - 참모별 활동 현황
   - 시스템 상태 모니터링

**산출물**:
- `scheduler.py` (스케줄러)
- `telegram_bot.py` (텔레그램 봇)
- `dashboard.html` (대시보드)

### Phase 4: 고도화 & 최적화 (Week 7-8)

**목표**: AI 기반 자동 해석

**구현 내용**:
1. Claude API 통합
   - 데이터 → Claude → 자동 해석
   - 참모별 페르소나 유지
   - 고품질 리포트 생성

2. 학습 시스템
   - 과거 브리핑 학습
   - 참모별 말투 학습
   - 일관성 향상

3. 인터랙티브 리포트
   - NotebookLM에서 질문 가능
   - 자동 답변 생성
   - 대화형 인터페이스

**산출물**:
- `ai_interpreter.py` (AI 해석)
- `persona_manager.py` (페르소나 관리)
- `interactive_report.py` (인터랙티브)

---

## 5️⃣ 구현 상세 (코드 예시)

### 5.1 데이터 분석 자동화

```python
# data_analyzer.py

import pandas as pd
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class AnalysisResult:
    """분석 결과 데이터 클래스"""
    staff_name: str
    analysis_type: str
    content: str
    priority: int  # 1(긴급), 2(중요), 3(일반)

class AutoDataAnalyzer:
    """데이터 자동 분석 엔진"""
    
    def __init__(self, upload_dir: str):
        self.upload_dir = upload_dir
        self.balance = None
        self.inst_buy_kospi = None
        self.inst_buy_kosdaq = None
        self.inst_sell_kospi = None
        self.inst_sell_kosdaq = None
        self.foreign_buy = None
        self.foreign_sell = None
    
    def detect_new_files(self) -> List[str]:
        """새로운 파일 감지"""
        import os
        from datetime import datetime, timedelta
        
        recent_files = []
        cutoff = datetime.now() - timedelta(hours=1)
        
        for filename in os.listdir(self.upload_dir):
            filepath = os.path.join(self.upload_dir, filename)
            file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
            
            if file_time > cutoff:
                recent_files.append(filepath)
        
        return recent_files
    
    def load_and_clean_data(self, filepaths: List[str]):
        """데이터 로드 & 클리닝"""
        for filepath in filepaths:
            filename = os.path.basename(filepath)
            
            if '잔고' in filename:
                self.balance = self._load_balance(filepath)
            elif '기관_매수' in filename and '코스피' in filename:
                self.inst_buy_kospi = self._load_institution(filepath)
            elif '기관_매수' in filename and '코스닥' in filename:
                self.inst_buy_kosdaq = self._load_institution(filepath)
            # ... (나머지 파일들)
    
    def _clean_numeric(self, val):
        """숫자 데이터 클리닝"""
        if isinstance(val, str):
            return float(val.replace(',', '').replace('+', '').replace('%', ''))
        return val
    
    def analyze_all_staff(self) -> List[AnalysisResult]:
        """전 능력자 분석 실행"""
        results = []
        
        # 1. 전략 최부장 분석
        results.append(self.analyze_strategy())
        
        # 2. 자금흐름 박차장 분석
        results.append(self.analyze_money_flow())
        
        # 3. 종목분석 이과장 분석
        results.append(self.analyze_portfolio())
        
        # 4. 트레이딩 김대리 분석
        results.append(self.analyze_trading())
        
        # 5. 운영 정차장 분석
        results.append(self.analyze_operations())
        
        # 6. 캐빈 총괄 분석
        results.append(self.analyze_comprehensive())
        
        return results
    
    def analyze_strategy(self) -> AnalysisResult:
        """전략 최부장 분석"""
        # 기관 매수 TOP 10 분석
        top_buy = self.inst_buy_kospi.head(10)
        
        # 섹터별 자금 흐름 계산
        semiconductor = top_buy[top_buy['종목명'].str.contains('SK하이닉스|삼성전자')]['순매수금액(백만)'].sum()
        
        # 리포트 생성
        content = f"""# 전략 최부장 데이터 분석
        
## 기관 매수 TOP 10
{top_buy[['종목명', '순매수금액(백만)']].to_markdown()}

## 섹터별 자금 흐름
- 반도체: {semiconductor:,.0f}백만원
...
"""
        
        return AnalysisResult(
            staff_name="전략 최부장",
            analysis_type="거시 시장",
            content=content,
            priority=1
        )
    
    def analyze_money_flow(self) -> AnalysisResult:
        """자금흐름 박차장 분석"""
        # 외국인 매수 TOP 10
        foreign_top = self.foreign_buy.head(10)
        
        content = f"""# 자금흐름 박차장 데이터 분석
        
## 외국인 매수 TOP 10
{foreign_top[['종목명', '순매수량']].to_markdown()}
...
"""
        
        return AnalysisResult(
            staff_name="자금흐름 박차장",
            analysis_type="투자 주체",
            content=content,
            priority=1
        )
    
    def analyze_portfolio(self) -> AnalysisResult:
        """종목분석 이과장 분석"""
        # 보유 종목 vs 기관/외국인 수급 체크
        holdings = self.balance['종목코드'].tolist()
        
        content = f"""# 종목분석 이과장 데이터 분석
        
## 포트폴리오 현황
총 수익률: {self._calculate_return():.2f}%
...
"""
        
        return AnalysisResult(
            staff_name="종목분석 이과장",
            analysis_type="포트폴리오",
            content=content,
            priority=2
        )
```

### 5.2 NotebookLM 자동 저장

```python
# notebooklm_client.py

import asyncio
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class NotebookConfig:
    """NotebookLM 설정"""
    staff_name: str
    notebook_id: str
    retry_count: int = 3
    retry_delay: int = 5  # seconds

class NotebookLMClient:
    """NotebookLM MCP 클라이언트"""
    
    STAFF_NOTEBOOKS = {
        "전략 최부장": "f9e7f9e1-1a76-4c96-a428-263287bc8c0b",
        "자금흐름 박차장": "56115056-37a5-496a-a997-625c9d21e90f",
        "종목분석 이과장": "0236e606-a7cd-4617-bdb4-863198c3ca9a",
        "트레이딩 김대리": "9bcfa6c8-318c-4799-abc7-7973bdd749aa",
        "운영 정차장": "2b10da1a-c78c-46fe-a615-3486df360976",
        "캐빈 총괄": "59b224e7-e3c3-40d8-bced-c74c437fd2be",
    }
    
    def __init__(self):
        self.success_count = 0
        self.failure_count = 0
        self.failed_saves = []
    
    async def save_to_notebook(
        self,
        staff_name: str,
        title: str,
        content: str,
        retry: int = 3
    ) -> bool:
        """NotebookLM에 저장 (재시도 로직 포함)"""
        
        notebook_id = self.STAFF_NOTEBOOKS.get(staff_name)
        if not notebook_id:
            print(f"❌ {staff_name}: NotebookLM ID를 찾을 수 없습니다.")
            return False
        
        for attempt in range(retry):
            try:
                # MCP 호출 (실제로는 MCP 클라이언트 사용)
                result = await self._call_mcp(
                    notebook_id=notebook_id,
                    title=title,
                    content=content
                )
                
                if result.get('status') == 'success':
                    self.success_count += 1
                    print(f"✅ {staff_name}: 저장 성공 ({title})")
                    return True
                
            except Exception as e:
                print(f"⚠️ {staff_name}: 시도 {attempt+1}/{retry} 실패 - {str(e)}")
                
                if attempt < retry - 1:
                    await asyncio.sleep(5)  # 5초 대기 후 재시도
                else:
                    self.failure_count += 1
                    self.failed_saves.append({
                        'staff': staff_name,
                        'title': title,
                        'error': str(e)
                    })
                    print(f"❌ {staff_name}: 최종 실패")
                    return False
        
        return False
    
    async def batch_save(
        self,
        analysis_results: List[AnalysisResult]
    ) -> Dict[str, any]:
        """일괄 저장 (비동기 처리)"""
        
        tasks = []
        for result in analysis_results:
            task = self.save_to_notebook(
                staff_name=result.staff_name,
                title=f"{result.analysis_type} 분석 ({self._get_date()})",
                content=result.content
            )
            tasks.append(task)
        
        # 모든 작업 동시 실행
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return {
            'total': len(results),
            'success': self.success_count,
            'failure': self.failure_count,
            'failed_saves': self.failed_saves
        }
    
    async def _call_mcp(
        self,
        notebook_id: str,
        title: str,
        content: str
    ) -> Dict:
        """MCP 실제 호출 (placeholder)"""
        # 실제 구현에서는 notebooklm-mcp:notebook_add_text 호출
        pass
    
    def _get_date(self) -> str:
        """현재 날짜"""
        from datetime import datetime
        return datetime.now().strftime("%Y.%m.%d")
```

### 5.3 자동화 오케스트레이터

```python
# automation_orchestrator.py

import schedule
import time
from datetime import datetime
from typing import List

class AutomationOrchestrator:
    """자동화 총괄 (자동화 한과장)"""
    
    def __init__(self):
        self.analyzer = AutoDataAnalyzer('/mnt/user-data/uploads')
        self.notebooklm_client = NotebookLMClient()
        self.telegram_bot = TelegramBot()  # 향후 구현
    
    def run_daily_analysis(self):
        """일일 분석 실행"""
        print(f"🔄 일일 분석 시작: {datetime.now()}")
        
        try:
            # 1. 새 파일 감지
            new_files = self.analyzer.detect_new_files()
            if not new_files:
                print("⚪ 새로운 파일 없음")
                return
            
            print(f"📂 새 파일 {len(new_files)}개 감지")
            
            # 2. 데이터 로드 & 클리닝
            self.analyzer.load_and_clean_data(new_files)
            print("✅ 데이터 로드 완료")
            
            # 3. 전 능력자 분석
            results = self.analyzer.analyze_all_staff()
            print(f"✅ 분석 완료: {len(results)}개 리포트")
            
            # 4. NotebookLM 저장
            asyncio.run(self._save_all(results))
            
            # 5. 완료 알림
            self.send_completion_notice(results)
            
        except Exception as e:
            print(f"❌ 에러 발생: {str(e)}")
            self.send_error_alert(str(e))
    
    async def _save_all(self, results: List[AnalysisResult]):
        """모든 결과 저장"""
        summary = await self.notebooklm_client.batch_save(results)
        
        print(f"\n📊 저장 결과:")
        print(f"  - 총 {summary['total']}개")
        print(f"  - 성공: {summary['success']}개 ✅")
        print(f"  - 실패: {summary['failure']}개 ❌")
        
        if summary['failed_saves']:
            print(f"\n⚠️ 실패 목록:")
            for failed in summary['failed_saves']:
                print(f"  - {failed['staff']}: {failed['title']}")
        
        return summary
    
    def send_completion_notice(self, results: List[AnalysisResult]):
        """완료 알림 (텔레그램)"""
        message = f"""
✅ 일일 분석 완료!

분석 시각: {datetime.now().strftime('%Y-%m-%d %H:%M')}
능력자: {len(results)}명
저장 완료: {self.notebooklm_client.success_count}개

NotebookLM에서 확인하세요.
        """
        # self.telegram_bot.send_message(message)
        print(message)
    
    def send_error_alert(self, error: str):
        """에러 알림"""
        message = f"""
⚠️ 자동화 에러 발생!

시각: {datetime.now().strftime('%Y-%m-%d %H:%M')}
에러: {error}

확인 필요!
        """
        # self.telegram_bot.send_message(message)
        print(message)
    
    def schedule_jobs(self):
        """작업 스케줄링"""
        # 매일 오전 9시 실행
        schedule.every().day.at("09:00").do(self.run_daily_analysis)
        
        # 파일 업로드 감지 (1분마다 체크)
        schedule.every(1).minutes.do(self.check_new_uploads)
        
        print("⏰ 스케줄 설정 완료")
        print("  - 일일 분석: 매일 09:00")
        print("  - 파일 감지: 1분마다")
    
    def check_new_uploads(self):
        """파일 업로드 감지 (실시간)"""
        new_files = self.analyzer.detect_new_files()
        if new_files:
            print(f"📂 새 파일 감지: {len(new_files)}개")
            self.run_daily_analysis()
    
    def run(self):
        """메인 루프"""
        self.schedule_jobs()
        
        print("🤖 자동화 한과장 가동 시작!")
        print("   Ctrl+C로 종료")
        
        while True:
            schedule.run_pending()
            time.sleep(1)

# 실행
if __name__ == "__main__":
    orchestrator = AutomationOrchestrator()
    orchestrator.run()
```

---

## 6️⃣ 운영 시나리오

### 시나리오 1: 일일 자동 브리핑

**08:55 - 파일 업로드**
```
CEO님이 잔고 CSV, 기관/외국인 매매 데이터 업로드
  ↓
자동화 한과장이 새 파일 감지 (1분 이내)
```

**09:00 - 자동 분석 시작**
```
데이터 로드 & 클리닝 (30초)
  ↓
6명 능력자 병렬 분석 (2분)
  ↓
리포트 자동 생성 (1분)
```

**09:03 - NotebookLM 저장**
```
6개 NotebookLM 동시 저장 (1분)
  ↓
저장 성공 확인
  ↓
텔레그램 완료 알림
```

**09:04 - 완료**
```
CEO님께 알림
  ↓
NotebookLM에서 확인 가능
```

### 시나리오 2: 긴급 분석 요청

**요청**
```
CEO님: "캐빈, 지금 SK하이닉스 긴급 분석해줘"
  ↓
캐빈: 즉시 분석 시작
```

**실시간 분석**
```
웹 검색으로 최신 정보 수집 (30초)
  ↓
능력자 긴급 회의 (1분)
  ↓
종합 리포트 생성 (30초)
```

**저장**
```
NotebookLM 즉시 저장
  ↓
CEO님께 요약 보고
  ↓
상세 내용은 NotebookLM 참조
```

### 시나리오 3: 에러 발생 시

**저장 실패**
```
전략 최부장 저장 실패
  ↓
자동 재시도 (3회, 5초 간격)
  ↓
모두 실패 시 텔레그램 알림
```

**수동 개입**
```
CEO님 or 함마 부장 확인
  ↓
수동 재저장 or 시스템 재시작
  ↓
완료 후 정상 운영 재개
```

---

## 7️⃣ 향후 확장 계획

### Phase 5: AI 고도화 (Month 3-4)

**Claude API 완전 통합**
- 데이터 → Claude → 자동 해석
- 참모 페르소나 완벽 재현
- 자연어 리포트 생성

**학습 시스템**
- 과거 브리핑 학습
- CEO님 피드백 반영
- 지속적 품질 개선

### Phase 6: 실시간 모니터링 (Month 5-6)

**실시간 알림**
- 코스피/코스닥 급등락 시 즉시 알림
- 보유 종목 손절선 도달 시 경고
- 메이저 수급 변화 즉시 감지

**대시보드**
- 실시간 포트폴리오 현황
- 능력자 활동 통계
- 시스템 상태 모니터링

### Phase 7: 통합 플랫폼 (Month 7-12)

**웹 인터페이스**
- 브라우저에서 모든 기능 접근
- 드래그 & 드롭 파일 업로드
- 인터랙티브 대시보드

**모바일 앱**
- 외출 중에도 실시간 확인
- 푸시 알림
- 간편 명령 실행

**API 제공**
- 외부 시스템 연동
- 자동 매매 시스템 통합
- 서드파티 도구 연결

---

## 📊 예상 효과

### 시간 절약
```
Before: 수동 분석 & 저장 30분
After: 자동 분석 & 저장 5분
절감: 25분 (83% 감소)

월간: 25분 × 20일 = 500분 (8.3시간)
연간: 8.3시간 × 12개월 = 100시간
```

### 품질 향상
```
일관성: 100% (템플릿 기반)
누락: 0% (자동 체크)
오류: 최소화 (자동 검증)
```

### 확장성
```
새 참모 추가: 10분 설정
새 분석 모듈: 1시간 개발
새 데이터 소스: 30분 연동
```

---

## 🎯 단계별 우선순위

### 최우선 (P0)
- ✅ Phase 1: 데이터 분석 자동화
- ✅ Phase 2: NotebookLM 자동 저장

### 높음 (P1)
- ⏳ Phase 3: 스케줄링 & 텔레그램 알림
- ⏳ Phase 4: AI 기반 자동 해석

### 중간 (P2)
- ⏸️ Phase 5: 실시간 모니터링
- ⏸️ Phase 6: 대시보드

### 낮음 (P3)
- 💭 Phase 7: 웹/모바일 플랫폼

---

## 💡 캐빈 의견

**현재 상태**:
- ✅ NotebookLM MCP 연동 완료
- ✅ 수동 저장 프로세스 확립
- ⏳ 자동화 설계 완료

**다음 단계**:
1. 자동화 한과장 (한태준) 투입 대기
2. 함마 부장 복귀 후 본격 개발
3. 2주 내 Phase 1-2 완성 목표

**기대 효과**:
- 캐빈의 전략 수립 시간 증가
- 일관된 품질의 리포트
- 실시간 대응 능력 향상

---

**자동화 구축 계획서 작성 완료!**
**CEO님 검토 부탁드립니다!** 🤖
