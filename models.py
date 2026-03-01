from dataclasses import dataclass


@dataclass
class AnalysisResult:
    """분석 결과 데이터 클래스"""

    staff_name: str
    analysis_type: str
    content: str
    priority: int  # 1(긴급), 2(중요), 3(일반)
