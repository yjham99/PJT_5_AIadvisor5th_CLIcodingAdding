import os
import csv
import asyncio
from automation_orchestrator import AutomationOrchestrator


async def run_simulation():
    print("=== [Simulation] AI Advisor Automation System ===")

    # 1. 테스트 데이터 디렉토리 설정
    test_dir = "simulation_uploads"
    os.makedirs(test_dir, exist_ok=True)

    # 2. 가상 데이터 생성 (CSV)
    print("📝 가상 데이터 생성 중...")

    # 기관 매수 데이터
    with open(
        os.path.join(test_dir, "20260214_기관_매수_코스피.csv"),
        mode="w",
        encoding="utf-8",
        newline="",
    ) as f:
        writer = csv.writer(f)
        writer.writerow(["종목명", "순매수금액(백만)"])
        writer.writerow(["삼성전자", "150000"])
        writer.writerow(["SK하이닉스", "80000"])
        writer.writerow(["현대차", "30000"])

    # 잔고 데이터
    with open(
        os.path.join(test_dir, "20260214_잔고_현황.csv"),
        mode="w",
        encoding="utf-8",
        newline="",
    ) as f:
        writer = csv.writer(f)
        writer.writerow(["종목코드", "종목명", "수량", "수익률"])
        writer.writerow(["005930", "삼성전자", "100", "5.2"])
        writer.writerow(["000660", "SK하이닉스", "50", "-1.5"])

    # 3. 오케스트레이터 실행
    orchestrator = AutomationOrchestrator(test_dir)
    success = await orchestrator.run_daily_analysis(simulate=True)

    if success:
        print("\n✅ 전체 시스템 시뮬레이션 성공!")
    else:
        print("\n❌ 시뮬레이션 과정 중 오류 발생")


if __name__ == "__main__":
    asyncio.run(run_simulation())
