
import csv
import os
from typing import Dict, List, Tuple
from models import AnalysisResult

# Try to use pandas if available for better performance and compatibility
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


class AutoDataAnalyzer:
    """데이터 자동 분석 엔진 (Pandas 및 표준 라이브러리 지원)"""

    def __init__(self, upload_dir: str):
        self.upload_dir = upload_dir
        self.balance = None
        self.inst_buy_kospi = None

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
            except Exception as e:
                print(f"⚠️ {filename} 처리 실패: {e}")

    def analyze_all_staff(self) -> List[AnalysisResult]:
        """전 능력자 분석 실행"""
        results = []

        if self.inst_buy_kospi:
            results.append(self.analyze_strategy())

        if self.balance:
            results.append(self.analyze_portfolio())

        return results

    def analyze_strategy(self) -> AnalysisResult:
        """전략 최부장 분석 (기관 매수 TOP 10)"""
        top_buy = self.inst_buy_kospi[:10]

        content = "# 전략 최부장 데이터 분석\n\n## 기관 매수 TOP 10\n"
        for row in top_buy:
            name = row.get("종목명", "N/A")
            amount = row.get("순매수금액(백만)", row.get("순매수금액", "0"))
            content += f"- {name}: {amount}백만\n"

        return AnalysisResult(
            staff_name="전략 최부장",
            analysis_type="거시 시장",
            content=content,
            priority=1,
        )

    def analyze_portfolio(self) -> AnalysisResult:
        """종목분석 이과장 분석"""
        content = f"# 종목분석 이과장 데이터 분석\n\n## 포트폴리오 현황\n보유 종목 수: {len(self.balance)}\n"
        for row in self.balance:
            name = row.get("종목명", row.get("종목코드", "N/A"))
            profit = row.get("수익률", "0")
            content += f"- {name}: 수익률 {profit}% \n"

        return AnalysisResult(
            staff_name="종목분석 이과장",
            analysis_type="포트폴리오",
            content=content,
            priority=2,
        )
