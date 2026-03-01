import asyncio
import argparse
from automation_orchestrator import AutomationOrchestrator


async def run_scheduler(interval_hours: float, simulate: bool):
    """
    정해진 시간 간격으로 자동화 프로세스를 실행하는 스케줄러 서비스입니다.
    """
    orchestrator = AutomationOrchestrator("uploads")

    print(f"⏰ AI 어드바이저 스케줄러가 시작되었습니다. (주기: {interval_hours}시간)")

    while True:
        try:
            # 전체 분석 및 저장 프로세스 실행
            await orchestrator.run_daily_analysis(simulate=simulate)

            print(f"\n💤 다음 실행까지 {interval_hours}시간 동안 대기합니다...")
            await asyncio.sleep(interval_hours * 3600)

        except Exception as e:
            print(f"❌ 스케줄러 실행 중 오류 발생: {e}")
            print("🔄 1분 후 재시도합니다...")
            await asyncio.sleep(60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Advisor Periodic Scheduler")
    parser.add_argument(
        "--interval", type=float, default=24, help="실행 간격 (시간 단위, 기본 24시간)"
    )
    parser.add_argument(
        "--simulate", action="store_true", help="시뮬레이션 모드로 실행"
    )

    args = parser.parse_args()

    try:
        asyncio.run(run_scheduler(args.interval, args.simulate))
    except KeyboardInterrupt:
        print("\n👋 스케줄러를 종료합니다.")
