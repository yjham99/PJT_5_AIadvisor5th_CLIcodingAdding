import os
import csv
import asyncio
import sys
from unittest.mock import MagicMock

# 1. AI 호출을 위한 모킹 설정
mock_genai = MagicMock()
sys.modules["google"] = MagicMock()
sys.modules["google.genai"] = mock_genai
sys.modules["google.genai.types"] = MagicMock()
sys.modules["dotenv"] = MagicMock()

from automation_orchestrator import AutomationOrchestrator  # noqa: E402


# Gemini 응답 시뮬레이션
async def mock_generate_content(*args, **kwargs):
    instruction = str(kwargs.get("system_instruction", ""))
    if "최부장" in instruction:
        return "최부장 의견: 반도체 섹터의 기관 매집은 매우 긍정적입니다."
    elif "박차장" in instruction:
        return "박차장 의견: IT 및 자동차 섹터로 자금이 집중 유입되고 있습니다."
    elif "이과장" in instruction:
        return "이과장 의견: 삼성전자 수익률 12.5%는 훌륭합니다. 보유 유지하세요."
    elif "김대리" in instruction:
        return "김대리 의견: 특징주인 '에코프로'는 뉴스 재료가 강력하여 단기 추세 지속이 기대됩니다."
    elif "종목 마스터" in instruction:
        return "종목 마스터 의견: 삼성전자와 에코프로는 각각 반도체와 2차전지의 대장주로, 현재 기관 수급과 뉴스 재료가 동시에 살아있어 분할 매수 관점이 유효합니다."
    return "AI 분석 완료."


async def run_simulation():
    print("=== [Simulation] AI Advisor Targeted Stock Analysis System ===")

    # 모킹 적용
    from model_scheduler import GeminiSmartScheduler

    GeminiSmartScheduler.generate_content = mock_generate_content

    # 2. 테스트 데이터 디렉토리 설정
    test_dir = "simulation_uploads"
    os.makedirs(test_dir, exist_ok=True)

    # 3. 가상 데이터 생성 (CSV)
    print("📝 타겟 종목 포함 가상 데이터 생성 중...")

    # 기관 매수 데이터
    with open(
        os.path.join(test_dir, "20260215_기관_매수_코스피.csv"),
        mode="w",
        encoding="utf-8",
        newline="",
    ) as f:
        writer = csv.writer(f)
        writer.writerow(["종목명", "순매수금액(백만)"])
        writer.writerow(["삼성전자", "250000"])
        writer.writerow(["SK하이닉스", "120000"])

    # 잔고 데이터
    with open(
        os.path.join(test_dir, "20260215_잔고_현황.csv"),
        mode="w",
        encoding="utf-8",
        newline="",
    ) as f:
        writer = csv.writer(f)
        writer.writerow(["종목코드", "종목명", "수량", "수익률"])
        writer.writerow(["005930", "삼성전자", "200", "12.5"])

    # 특징주 데이터
    with open(
        os.path.join(test_dir, "20260215_특징주_포착.csv"),
        mode="w",
        encoding="utf-8",
        newline="",
    ) as f:
        writer = csv.writer(f)
        writer.writerow(["종목명", "현재가", "등락률", "사유"])
        writer.writerow(["에코프로", "150000", "15.5", "실적 서프라이즈"])

    # 4. 오케스트레이터 실행 (타겟 종목 지정)
    target_stocks = ["삼성전자", "에코프로"]
    orchestrator = AutomationOrchestrator(test_dir)
    success = await orchestrator.run_daily_analysis(
        simulate=True, target_stocks=target_stocks
    )

    if success:
        print(f"\n✅ '{', '.join(target_stocks)}' 맞춤형 AI 분석 성공!")
    else:
        print("\n❌ 시뮬레이션 과정 중 오류 발생")


if __name__ == "__main__":
    asyncio.run(run_simulation())
