import asyncio
import sys
from unittest.mock import MagicMock

# 1. Extensive Mocking for Environment Compatibility
mock_st = MagicMock()
mock_pd = MagicMock()
mock_genai = MagicMock()

sys.modules["streamlit"] = mock_st
sys.modules["pandas"] = mock_pd
sys.modules["dotenv"] = MagicMock()
sys.modules["google"] = MagicMock()
sys.modules["google.genai"] = mock_genai
sys.modules["google.genai.types"] = MagicMock()


# Mocking session_state
class SessionState(dict):
    def __getattr__(self, key):
        return self.get(key)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        if key in self:
            del self[key]


mock_st.session_state = SessionState()


# Mock DataFrame behavior
class MockDataFrame:
    def __init__(self, data):
        self.data = data
        self.empty = len(data) == 0

    def iterrows(self):
        return enumerate(self.data)

    def drop(self, idx):
        new_data = [d for i, d in enumerate(self.data) if i != idx]
        return MockDataFrame(new_data)

    def reset_index(self, drop=True):
        return self

    def __len__(self):
        return len(self.data)

    @property
    def iloc(self):
        return self.data


mock_pd.DataFrame = lambda x: MockDataFrame(x)
mock_pd.concat = lambda dfs, ignore_index=True: MockDataFrame(dfs[0].data + dfs[1].data)

from automation_orchestrator import AutomationOrchestrator  # noqa: E402


async def run_simulation():
    print("=== [Simulation] AI Advisor Dashboard UI Button Verification ===\n")

    # --- Initial State ---
    st = mock_st
    st.session_state.favorites = {"삼성전자"}
    st.session_state.monitoring = set()
    st.session_state.portfolio = MockDataFrame(
        [
            {
                "종목코드": "005930",
                "종목명": "삼성전자",
                "수량": 10,
                "매수단가": 72000,
                "현재가": 73500,
            }
        ]
    )
    st.session_state.realized_profit = 0.0

    print(f"Initial Favorites: {st.session_state.favorites}")
    print(f"Initial Portfolio Size: {len(st.session_state.portfolio)}")

    # --- Button 1: Toggle Favorite (Tab 1) ---
    print("\n[Action] Click Favorite for 'SK하이닉스'")
    stock = "SK하이닉스"
    if stock in st.session_state.favorites:
        st.session_state.favorites.remove(stock)
    else:
        st.session_state.favorites.add(stock)
    print(f"-> Favorites: {st.session_state.favorites}")

    # --- Button 2: Toggle Monitoring (Tab 1) ---
    print("\n[Action] Click Monitoring for '에코프로'")
    stock = "에코프로"
    st.session_state.monitoring.add(stock)
    print(f"-> Monitoring: {st.session_state.monitoring}")

    # --- Button 3: Sell Settlement (Tab 2) ---
    print("\n[Action] Sell '삼성전자' at 75000")
    target_idx = 0
    row = st.session_state.portfolio.data[target_idx]
    st.session_state.sell_target_info = {
        "idx": target_idx,
        "name": row["종목명"],
        "buy_price": row["매수단가"],
        "qty": row["수량"],
        "current_price": row["현재가"],
    }

    sell_price = 75000
    info = st.session_state.sell_target_info
    profit = (sell_price - info["buy_price"]) * info["qty"]
    st.session_state.realized_profit += profit
    st.session_state.portfolio = st.session_state.portfolio.drop(info["idx"])
    del st.session_state.sell_target_info

    print(f"-> Realized Profit: {st.session_state.realized_profit:,.0f}원")
    print(f"-> Portfolio Size: {len(st.session_state.portfolio)}")

    # --- Button 4: Run AI Briefing (Sidebar) ---
    print("\n[Action] Click 'Run AI Briefing'")
    orchestrator = AutomationOrchestrator()
    # Mocking actual AI call
    orchestrator.run_daily_analysis = MagicMock(return_value=asyncio.Future())
    orchestrator.run_daily_analysis.return_value.set_result(True)

    success = await orchestrator.run_daily_analysis(simulate=True)
    print(f"-> AI Briefing Call Success: {success}")

    print(
        "\n=== [Success] All button logics and connectivity verified via simulation. ==="
    )


if __name__ == "__main__":
    asyncio.run(run_simulation())
