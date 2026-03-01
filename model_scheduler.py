import os
import time
import logging
import asyncio
from dotenv import load_dotenv

# Try importing google-genai
try:
    from google import genai
    from google.genai import types
except ImportError:
    print(
        "❌ 'google-genai' 라이브러리가 설치되지 않았습니다. 'pip install google-genai'를 실행해주세요."
    )
    exit(1)

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("GeminiScheduler")

# .env 로드
load_dotenv()


class GeminiSmartScheduler:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            logger.warning(
                "⚠️ GOOGLE_API_KEY가 환경 변수에 설정되지 않았습니다. API 호출 시 실패할 수 있습니다."
            )

        self.client = genai.Client(api_key=self.api_key) if self.api_key else None

        # 모델별 설정 (RPD, RPM, TPM 등)
        # 출처: Google AI Studio 가격 정책 및 사용자 제공 데이터
        self.model_configs = {
            "gemini-2.0-flash": {
                "rpm": 15,
                "tpm": 1000000,
                "rpd": 1500,
                "weight": 1,
                "desc": "가장 빠르고 효율적 (메인)",
            },
            "gemini-2.0-pro-exp-02-05": {  # 최신 실험적 모델
                "rpm": 10,
                "tpm": 4000000,
                "rpd": 50,
                "weight": 2,
                "desc": "고성능 추론 (서브)",
            },
            "gemini-1.5-flash": {
                "rpm": 15,
                "tpm": 1000000,
                "rpd": 1500,
                "weight": 3,
                "desc": "안정적인 구버전 Flash",
            },
            "gemini-1.5-pro": {
                "rpm": 2,
                "tpm": 32000,
                "rpd": 50,
                "weight": 4,
                "desc": "고성능 (RPM 낮음 주의)",
            },
        }

        # 모델별 사용 기록 초기화
        # 실제 운영 시에는 DB나 파일로 상태를 영구 저장하는 것이 좋습니다.
        self.usage_stats = {
            model: {"calls_today": 0, "last_call": 0, "token_usage": 0}
            for model in self.model_configs
        }

        # 우선순위 큐 (가중치 오름차순)
        self.priority_list = sorted(
            self.model_configs.keys(), key=lambda x: self.model_configs[x]["weight"]
        )

        # 모델별 비동기 락 (Concurrent 요청 시 RPM 준수 보장)
        self.locks = {model: asyncio.Lock() for model in self.model_configs}

    def _get_wait_time(self, model_name):
        """RPM 준수를 위한 대기 시간 계산"""
        config = self.model_configs[model_name]
        elapsed = time.time() - self.usage_stats[model_name]["last_call"]
        required_gap = 60.0 / config["rpm"]

        wait = required_gap - elapsed
        return max(0, wait)

    def _check_reset_daily_limit(self):
        """(옵션) 일일 한도 초기화: 실제로는 서버 시간 기준 0시 또는 갱신 시점에 맞춰야 함"""
        # 여기서는 간단히 메모리 상에서만 동작하므로 생략하거나,
        # 파일 기반으로 날짜가 바뀌었는지 체크하는 로직이 필요함.
        pass

    async def generate_content(self, prompt, system_instruction=None):
        """
        가용 자원을 최우선으로 사용하여 콘텐츠 생성
        """
        if not self.client:
            return "❌ API Key Error: GOOGLE_API_KEY is missing."

        last_error = None

        for model_name in self.priority_list:
            config = self.model_configs[model_name]
            stats = self.usage_stats[model_name]
            lock = self.locks[model_name]

            async with lock:
                # 1. RPD(일일 한도) 체크
                if stats["calls_today"] >= config["rpd"]:
                    logger.info(
                        f"⏭️ {model_name}: 일일 한도 초과 ({stats['calls_today']}/{config['rpd']}). 다음 모델로 넘어갑니다."
                    )
                    continue

                # 2. RPM(속도 제한) 체크 및 대기
                wait_time = self._get_wait_time(model_name)
                if wait_time > 0:
                    if wait_time > 5:  # 5초 이상 기다려야 하면 다음 모델로
                        logger.info(
                            f"⏭️ {model_name}: 대기 시간({wait_time:.1f}s) 과다. 다음 모델로 넘어갑니다."
                        )
                        continue
                    else:
                        logger.debug(
                            f"⏳ {model_name}: RPM 조절을 위해 {wait_time:.2f}초 대기..."
                        )
                        await asyncio.sleep(wait_time)

                # 3. API 호출 시도
                try:
                    logger.info(
                        f"🚀 {model_name} 호출 중... (오늘 사용: {stats['calls_today']})"
                    )

                    # API 호출 파라미터 구성
                    generate_config = (
                        types.GenerateContentConfig(
                            system_instruction=system_instruction
                        )
                        if system_instruction
                        else None
                    )

                    response = await self.client.aio.models.generate_content(
                        model=model_name, contents=prompt, config=generate_config
                    )

                    # 4. 성공 처리
                    stats["calls_today"] += 1
                    stats["last_call"] = time.time()

                    # 토큰 사용량 추적 (근사치 또는 response 객체에서 추출 가능 시 업데이트)
                    # stats["token_usage"] += ...

                    return response.text

                except Exception as e:
                    error_msg = str(e)
                    logger.error(f"❌ {model_name} 실패: {error_msg}")

                    # 429 Resource Exhausted (Rate Limit)
                    if "429" in error_msg or "Resource has been exhausted" in error_msg:
                        logger.warning(
                            f"⚠️ {model_name} 리소스 고갈. 잠시 봉인하고 다음 모델로 전환합니다."
                        )
                        # 패널티: 마지막 호출 시간을 미래로 설정하여 당분간 건너뛰게 함
                        stats["last_call"] = time.time() + 60
                    else:
                        # 그 외 에러(권한, 잘못된 요청 등) 기록
                        last_error = e

                    continue  # 다음 모델 시도

        return f"❌ 모든 모델의 가용 자원이 소진되었거나 호출에 실패했습니다. 최후 에러: {last_error}"


# --- 테스트 실행 블록 ---
if __name__ == "__main__":
    print("\n[Gemini Smart Scheduler Test]")

    # .env 파일 체크
    if not os.path.exists(".env"):
        print(
            "⚠️ 경고: .env 파일이 없습니다. 키가 설정되어 있지 않다면 실패할 것입니다."
        )
        print(
            "    -> .env.template을 복사하여 .env를 만들고 GOOGLE_API_KEY를 입력하세요."
        )

    scheduler = GeminiSmartScheduler()

    test_prompt = "안녕하세요! 당신은 누구인가요? 짧게 자기소개 부탁해요."
    print(f"\n질문: {test_prompt}")

    result = asyncio.run(scheduler.generate_content(test_prompt))
    print(f"\n답변:\n{result}")
