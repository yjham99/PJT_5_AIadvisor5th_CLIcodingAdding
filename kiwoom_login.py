import subprocess
import os
import sys

# User provided path: C:\OpenAPI\opstarter.exe
KIWOOM_OPENAPI_PATH = r"C:\OpenAPI\opstarter.exe"


def login(simulate=None):
    """
    키움 증권 Open API 로그인을 시도합니다.
    Windows 환경에서는 실제 파일을 실행하고, 그 외에는 시뮬레이션 모드로 동작합니다.
    """
    # OS가 윈도우가 아니면 강제로 시뮬레이션 모드
    is_windows = sys.platform == "win32"
    if simulate is None:
        simulate = not is_windows

    if simulate:
        print(f"[Simulation] Starting Kiwoom Login via {KIWOOM_OPENAPI_PATH}")
        print("[Simulation] Login process started. Please check the login window.")
        return True

    try:
        if not os.path.exists(KIWOOM_OPENAPI_PATH):
            print(f"❌ 에러: {KIWOOM_OPENAPI_PATH} 경로를 찾을 수 없습니다.")
            print("   설치 경로를 확인하거나 OpenAPI가 설치되어 있는지 확인해 주세요.")
            return False

        print(f"🚀 {KIWOOM_OPENAPI_PATH} 실행 중...")
        # Windows에서 가장 권장되는 실행 방식 (os.startfile)
        if hasattr(os, "startfile"):
            os.startfile(KIWOOM_OPENAPI_PATH)
        else:
            subprocess.Popen([KIWOOM_OPENAPI_PATH], shell=True)

        return True
    except FileNotFoundError:
        print(f"❌ 에러: 파일을 찾을 수 없습니다. ({KIWOOM_OPENAPI_PATH})")
        return False
    except OSError as e:
        print(f"❌ 에러: 시스템 오류가 발생했습니다. ({e})")
        return False
    except Exception as e:
        print(f"❌ 로그인 실행 중 예상치 못한 오류 발생: {e}")
        return False


def check_login_status(simulate=None):
    """
    로그인 상태를 확인합니다.
    """
    is_windows = sys.platform == "win32"
    if simulate is None:
        simulate = not is_windows

    if simulate:
        print("[Simulation] Checking login status... Success!")
        return True

    # 실제 환경에서는 프로세스 목록(KHOpenAPI.exe 등)이나 윈도우 타이틀을 확인하는 로직이 필요할 수 있습니다.
    # 여기서는 프로세스가 정상적으로 시작되었다면 성공으로 간주합니다.
    return True


if __name__ == "__main__":
    print("--- Kiwoom Login Manager ---")
    # 로컬 테스트 시 simulate 인자를 조절할 수 있습니다.
    if login():
        if check_login_status():
            print("✅ 로그인 프로세스가 정상적으로 시작되었습니다.")
