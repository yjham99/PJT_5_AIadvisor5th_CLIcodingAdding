import asyncio
from typing import List, Dict
from models import AnalysisResult


class NotebookLMClient:
    """NotebookLM MCP 클라이언트"""

    STAFF_NOTEBOOKS = {
        "전략 최부장": "f9e7f9e1-1a76-4c96-a428-263287bc8c0b",
        "자금흐름 박차장": "56115056-37a5-496a-a997-625c9d21e90f",
        "종목분석 이과장": "0236e606-a7cd-4617-bdb4-863198c3ca9a",
        "트레이딩 김대리": "9bcfa6c8-318c-4799-abc7-7973bdd749aa",
        "운영 정차장": "2b10da1a-c78c-46fe-a615-3486df360976",
        "캐빈 총괄": "59b224e7-e3c3-40d8-bced-c74c437fd2be",
        "종목 마스터": "59b224e7-e3c3-40d8-bced-c74c437fd2be",  # 캐빈 총괄 노트북 공유 또는 별도 ID 지정 가능
    }

    def __init__(self):
        self.success_count = 0
        self.failure_count = 0

    async def save_to_notebook(
        self, staff_name: str, title: str, content: str, retry: int = 3
    ) -> bool:
        """NotebookLM에 저장 시뮬레이션"""
        notebook_id = self.STAFF_NOTEBOOKS.get(staff_name)
        if not notebook_id:
            print(f"❌ {staff_name}: Notebook ID 미설정")
            return False

        for attempt in range(retry):
            try:
                # 시뮬레이션: 성공으로 가정
                await asyncio.sleep(0.1)
                self.success_count += 1
                print(f"✅ {staff_name}: '{title}' 저장 성공")
                return True
            except Exception as e:
                if attempt == retry - 1:
                    self.failure_count += 1
                    print(f"❌ {staff_name}: 저장 실패 ({e})")
        return False

    async def batch_save(self, analysis_results: List[AnalysisResult]) -> Dict:
        """일괄 저장 (비동기 처리)"""
        from datetime import datetime

        date_str = datetime.now().strftime("%Y.%m.%d")

        tasks = []
        for result in analysis_results:
            task = self.save_to_notebook(
                staff_name=result.staff_name,
                title=f"{result.analysis_type} 분석 ({date_str})",
                content=result.content,
            )
            tasks.append(task)

        await asyncio.gather(*tasks)
        return {"success": self.success_count, "failure": self.failure_count}


if __name__ == "__main__":
    client = NotebookLMClient()
    mock_results = [
        AnalysisResult("전략 최부장", "거시 시장", "내용", 1),
        AnalysisResult("종목분석 이과장", "포트폴리오", "내용", 2),
    ]
    asyncio.run(client.batch_save(mock_results))
