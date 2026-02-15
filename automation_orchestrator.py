import asyncio
import sys
from datetime import datetime
from kiwoom_login import login, check_login_status
from data_analyzer import AutoDataAnalyzer
from notebooklm_client import NotebookLMClient
from model_scheduler import GeminiSmartScheduler


class AutomationOrchestrator:
    """자동화 총괄 (자동화 한과장)"""

    def __init__(self, upload_dir: str = "uploads"):
        # AI 분석 엔진 초기화
        self.ai_scheduler = GeminiSmartScheduler()

        # 분석기에 AI 엔진 주입
        self.analyzer = AutoDataAnalyzer(upload_dir, ai_scheduler=self.ai_scheduler)
        self.notebooklm_client = NotebookLMClient()

    async def run_daily_analysis(self, simulate=None):
        """일일 분석 및 저장 프로세스 실행"""
        # simulate가 None이면 윈도우가 아닐 때만 True로 설정
        if simulate is None:
            simulate = sys.platform != "win32"

        print(
            f"🔄 [시작] 일일 자동화 프로세스 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})"
        )
        if simulate:
            print("ℹ️  현재 시뮬레이션 모드로 동작 중입니다.")
        else:
            print("🚀 실제 운영 모드로 동작합니다.")

        # 1. 키움 증권 로그인 확인
        print("\n[Step 1] 키움 증권 로그인 확인 중...")
        if not login(simulate=simulate):
            print("❌ 에러: 로그인 프로세스 시작 실패. 작업을 중단합니다.")
            return False

        if not check_login_status(simulate=simulate):
            print("❌ 에러: 로그인 상태를 확인할 수 없습니다.")
            return False
        print("✅ 로그인 단계 통과")

        # 2. 파일 감지
        print("\n[Step 2] 새로운 데이터 파일 감지 중...")
        files = self.analyzer.detect_new_files()
        if not files:
            print("⚪ 감지된 새로운 CSV 파일이 없습니다. 업로드 폴더를 확인해 주세요.")
            return True

        print(f"📂 {len(files)}개의 CSV 파일이 감지되었습니다.")

        # 3. 데이터 로딩 및 분석
        print("\n[Step 3] 데이터 분석 및 AI 리포트 생성 중...")
        print("   (AI가 데이터를 심층 분석 중이므로 시간이 다소 소요될 수 있습니다.)")
        self.analyzer.load_and_clean_data(files)

        # 비동기 분석 실행 (await 추가)
        results = await self.analyzer.analyze_all_staff()

        if not results:
            print(
                "⚠️ 경고: 분석 결과가 생성되지 않았습니다. 데이터 형식을 확인해 주세요."
            )
            return False

        print(f"✅ AI 분석 완료 ({len(results)}개의 전문 리포트 생성됨)")

        # 4. NotebookLM 저장
        print("\n[Step 4] NotebookLM에 리포트 전송 및 저장 중...")
        summary = await self.notebooklm_client.batch_save(results)
        print(
            f"📊 최종 저장 결과: 성공 {summary['success']}, 실패 {summary['failure']}"
        )

        print(
            f"\n✨ [완료] 모든 프로세스가 성공적으로 종료되었습니다. ({datetime.now().strftime('%H:%M:%S')})"
        )
        return True


if __name__ == "__main__":
    # 기본 업로드 폴더 지정
    orchestrator = AutomationOrchestrator("uploads")
    # 실행 시 simulate=False를 주면 실제 윈도우에서 로그인 파일 실행을 시도합니다.
    asyncio.run(orchestrator.run_daily_analysis(simulate=None))
