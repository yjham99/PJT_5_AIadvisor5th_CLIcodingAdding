import csv
import os
import asyncio
from typing import Dict, List
from models import AnalysisResult
from staff_prompts import STAFF_PERSONAS

# Try to use pandas if available for better performance and compatibility
try:
    import pandas as pd

    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


class AutoDataAnalyzer:
    """데이터 자동 분석 엔진 (AI 기반 통찰력 제공)"""

    def __init__(self, upload_dir: str, ai_scheduler=None):
        self.upload_dir = upload_dir
        self.ai_scheduler = ai_scheduler
        self.balance = None
        self.inst_buy_kospi = None
        self.featured_stocks = None

    def detect_new_files(self) -> List[str]:
        """새로운 파일 감지"""
        recent_files = []
        if not os.path.exists(self.upload_dir):
            os.makedirs(self.upload_dir, exist_ok=True)

        for filename in os.listdir(self.upload_dir):
            if filename.lower().endswith(".csv"):
                recent_files.append(os.path.join(self.upload_dir, filename))

        return recent_files

    def _read_csv(self, filepath: str) -> List[Dict]:
        """다양한 인코딩(UTF-8, CP949)으로 CSV 파일을 읽습니다."""
        encodings = ["utf-8", "cp949", "euc-kr"]

        # Pandas 사용 가능 시
        if PANDAS_AVAILABLE:
            for enc in encodings:
                try:
                    df = pd.read_csv(filepath, encoding=enc)
                    return df.to_dict("records")
                except (UnicodeDecodeError, Exception):
                    continue

        # Pandas 불가 또는 실패 시 csv 모듈 사용
        for enc in encodings:
            try:
                with open(filepath, mode="r", encoding=enc) as f:
                    reader = csv.DictReader(f)
                    return list(reader)
            except (UnicodeDecodeError, Exception):
                continue

        print(f"❌ 에러: {filepath} 파일을 읽을 수 없습니다. (인코딩 문제)")
        return []

    def load_and_clean_data(self, filepaths: List[str]):
        """데이터 로드 & 클리닝"""
        for filepath in filepaths:
            filename = os.path.basename(filepath)

            try:
                data = self._read_csv(filepath)
                if not data:
                    continue

                if "잔고" in filename:
                    self.balance = data
                elif "기관_매수" in filename and "코스피" in filename:
                    self.inst_buy_kospi = data
                elif "특징주" in filename:
                    self.featured_stocks = data
            except Exception as e:
                print(f"⚠️ {filename} 처리 실패: {e}")

    async def analyze_all_staff(self, target_stocks: List[str] = None) -> List[AnalysisResult]:
        """전 능력자 분석 실행 (비동기 AI 분석 지원)"""
        tasks = []

        # 1. 기본 전체 분석 트랙
        if self.inst_buy_kospi:
            tasks.append(self.analyze_strategy())
            tasks.append(self.analyze_money_flow())

        if self.balance:
            tasks.append(self.analyze_portfolio())

        if self.featured_stocks:
            tasks.append(self.analyze_featured_stocks())

        # 2. 사용자 지정 특정 종목 분석 트랙 (추가)
        if target_stocks:
            tasks.append(self.analyze_specific_stocks(target_stocks))

        if not tasks:
            return []

        return await asyncio.gather(*tasks)

    async def _get_ai_insight(self, staff_name: str, raw_data_str: str) -> str:
        """Gemini를 통해 AI 통찰력을 얻습니다."""
        if not self.ai_scheduler:
            return "⚠️ AI 엔진이 설정되지 않아 기본 데이터만 제공합니다."

        persona = STAFF_PERSONAS.get(staff_name)
        if not persona:
            return "⚠️ 해당 능력자의 페르소나 정보를 찾을 수 없습니다."

        prompt = persona["template"].format(data=raw_data_str)
        system_instruction = persona["instruction"]

        insight = await self.ai_scheduler.generate_content(
            prompt=prompt, system_instruction=system_instruction
        )
        return insight

    async def analyze_strategy(self) -> AnalysisResult:
        """전략 최부장 분석 (AI 기반)"""
        staff_name = "전략 최부장"
        top_buy = self.inst_buy_kospi[:15]  # 조금 더 많은 데이터 제공

        # 데이터 텍스트화
        data_str = "## 기관 매수 상위 종목\n"
        for row in top_buy:
            name = row.get("종목명", "N/A")
            amount = row.get("순매수금액(백만)", row.get("순매수금액", "0"))
            data_str += f"- {name}: {amount}백만\n"

        # AI 분석 요청
        insight = await self._get_ai_insight(staff_name, data_str)

        content = f"# {staff_name} 전략 리포트\n\n{insight}\n\n"
        content += f"--- \n### 분석 기초 데이터\n{data_str}"

        return AnalysisResult(
            staff_name=staff_name,
            analysis_type="거시 시장",
            content=content,
            priority=1,
        )

    async def analyze_specific_stocks(self, target_stocks: List[str]) -> AnalysisResult:
        """종목 마스터 분석 (특정 종목 집중 분석)"""
        staff_name = "종목 마스터"

        # 모든 가용 데이터에서 타겟 종목 정보 추출
        combined_data = f"## 타겟 분석 종목: {', '.join(target_stocks)}\n"
        found_any = False

        # 1. 잔고 데이터에서 확인
        if self.balance:
            combined_data += "\n### 포트폴리오 현황\n"
            for row in self.balance:
                if row.get("종목명") in target_stocks or row.get("종목코드") in target_stocks:
                    name = row.get("종목명", row.get("종목코드"))
                    profit = row.get("수익률", "0")
                    combined_data += f"- {name}: 우리 포트폴리오 수익률 {profit}%\n"
                    found_any = True

        # 2. 기관 매수 데이터에서 확인
        if self.inst_buy_kospi:
            combined_data += "\n### 기관 매수 순위\n"
            for row in self.inst_buy_kospi:
                if row.get("종목명") in target_stocks:
                    name = row.get("종목명")
                    amount = row.get("순매수금액(백만)", row.get("순매수금액", "0"))
                    combined_data += f"- {name}: 기관이 {amount}백만 순매수 중\n"
                    found_any = True

        # 3. 특징주 데이터에서 확인
        if self.featured_stocks:
            combined_data += "\n### 특징주 포착 이력\n"
            for row in self.featured_stocks:
                if row.get("종목명") in target_stocks:
                    name = row.get("종목명")
                    reason = row.get("사유", "특이 사항 없음")
                    combined_data += f"- {name}: 특징주 포착 (사유: {reason})\n"
                    found_any = True

        if not found_any:
            combined_data += "\n⚠️ 현재 데이터 파일 내에서 해당 종목의 구체적인 매매 이력을 찾을 수 없습니다. 일반적인 정보를 바탕으로 분석합니다.\n"

        insight = await self._get_ai_insight(staff_name, combined_data)

        content = f"# {staff_name} 특정 종목 집중 분석\n\n{insight}\n\n"
        content += f"--- \n### 분석 대상 데이터 요약\n{combined_data}"

        return AnalysisResult(
            staff_name=staff_name,
            analysis_type="특정 종목 분석",
            content=content,
            priority=1,
        )

    async def analyze_money_flow(self) -> AnalysisResult:
        """자금흐름 박차장 분석 (AI 기반)"""
        staff_name = "자금흐름 박차장"
        # 여기서는 기관 매수 데이터를 자금 흐름 관점에서 분석하도록 전달
        data_str = "## 시장 자금 유입 현황 (기관 순매수 기준)\n"
        for row in self.inst_buy_kospi[:15]:
            name = row.get("종목명", "N/A")
            amount = row.get("순매수금액(백만)", row.get("순매수금액", "0"))
            data_str += f"- {name}: {amount}백만\n"

        insight = await self._get_ai_insight(staff_name, data_str)

        content = f"# {staff_name} 수급 브리핑\n\n{insight}\n\n"

        return AnalysisResult(
            staff_name=staff_name,
            analysis_type="투자 주체",
            content=content,
            priority=1,
        )

    async def analyze_portfolio(self) -> AnalysisResult:
        """종목분석 이과장 분석 (AI 기반)"""
        staff_name = "종목분석 이과장"

        data_str = "## 현재 포트폴리오 잔고 현황\n"
        for row in self.balance:
            name = row.get("종목명", row.get("종목코드", "N/A"))
            profit = row.get("수익률", "0")
            data_str += f"- {name}: 수익률 {profit}% \n"

        insight = await self._get_ai_insight(staff_name, data_str)

        content = f"# {staff_name} 종목 진단\n\n{insight}\n\n"
        content += f"--- \n### 보유 종목 상세\n{data_str}"

        return AnalysisResult(
            staff_name=staff_name,
            analysis_type="포트폴리오",
            content=content,
            priority=2,
        )

    async def analyze_featured_stocks(self) -> AnalysisResult:
        """트레이딩 김대리 분석 (AI 기반 특징주 찾기)"""
        staff_name = "트레이딩 김대리"

        data_str = "## 오늘 포착된 특징주 리스트\n"
        for row in self.featured_stocks[:10]:
            name = row.get("종목명", "N/A")
            price = row.get("현재가", "N/A")
            change = row.get("등락률", "0")
            reason = row.get("사유", row.get("비고", "재료 파악 중"))
            data_str += f"- {name} ({change}%): {price}원 - 사유: {reason}\n"

        insight = await self._get_ai_insight(staff_name, data_str)

        content = f"# {staff_name} 특징주 리포트\n\n{insight}\n\n"
        content += f"--- \n### 특징주 상세 데이터\n{data_str}"

        return AnalysisResult(
            staff_name=staff_name,
            analysis_type="특징주 찾기",
            content=content,
            priority=1,
        )
