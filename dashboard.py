
import streamlit as st
import pandas as pd
import asyncio
import os
from automation_orchestrator import AutomationOrchestrator

# --- 설정 및 초기화 ---
st.set_page_config(page_title="AI Advisor Dashboard", layout="wide")

# 데이터 저장 폴더
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# 세션 상태 초기화
if 'favorites' not in st.session_state:
    st.session_state.favorites = set()
if 'monitoring' not in st.session_state:
    st.session_state.monitoring = set()
if 'portfolio' not in st.session_state:
    # 초기 포트폴리오 데이터 (삼성전자는 예시로 포함하되 삭제 가능하게)
    st.session_state.portfolio = pd.DataFrame([
        {'종목코드': '005930', '종목명': '삼성전자', '수량': 10, '매수단가': 72000, '현재가': 73500}
    ])
if 'briefing_history' not in st.session_state:
    st.session_state.briefing_history = []

# --- 사이드바: AI 컨트롤 ---
st.sidebar.title("🤖 AI Command Center")
if st.sidebar.button("🚀 Run AI Briefing (전체 분석)"):
    with st.spinner("AI가 전체 시장을 분석 중입니다..."):
        orchestrator = AutomationOrchestrator()
        # 비동기 함수 실행을 위한 헬퍼
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        success = loop.run_until_complete(orchestrator.run_daily_analysis(simulate=True))
        if success:
            st.sidebar.success("AI 브리핑 완료! NotebookLM을 확인하세요.")
        else:
            st.sidebar.error("브리핑 실행 중 오류 발생")

# --- 메인 화면 ---
st.title("📈 AI Advisor 통합 대시보드")

tab1, tab2, tab3 = st.tabs(["📊 시장 현황", "💼 포트폴리오 관리", "⭐ 즐겨찾기/모니터링"])

# --- Tab 1: 시장 현황 ---
with tab1:
    st.subheader("🔥 특징주 및 주요 종목 리스트")

    # 예시 데이터 (실제 운영 시 CSV 로드)
    market_data = pd.DataFrame({
        '종목명': ['삼성전자', 'SK하이닉스', '에코프로', '현대차', 'NAVER'],
        '현재가': [73500, 145000, 125000, 245000, 210000],
        '등락률': [1.2, 2.5, -3.1, 0.8, -1.5]
    })

    for idx, row in market_data.iterrows():
        col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 2])
        col1.write(f"**{row['종목명']}**")
        col2.write(f"{row['현재가']:,}원")
        col3.write(f"{row['등락률']}%")

        # 즐겨찾기 버튼
        fav_label = "⭐" if row['종목명'] in st.session_state.favorites else "☆"
        if col4.button(fav_label, key=f"fav_{idx}"):
            if row['종목명'] in st.session_state.favorites:
                st.session_state.favorites.remove(row['종목명'])
            else:
                st.session_state.favorites.add(row['종목명'])
            st.rerun()

        # 개별 AI 브리핑 버튼
        if col5.button("🧐 AI 분석", key=f"ai_{idx}"):
            with st.spinner(f"{row['종목명']} 심층 분석 중..."):
                orchestrator = AutomationOrchestrator()
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                # 특정 종목 타겟 분석 실행
                loop.run_until_complete(orchestrator.run_daily_analysis(simulate=True, target_stocks=[row['종목명']]))
                st.info(f"✅ {row['종목명']} 분석 완료! NotebookLM의 '종목 마스터' 리포트를 확인하세요.")

# --- Tab 2: 포트폴리오 관리 ---
with tab2:
    st.subheader("💰 현재 보유 자산")

    if st.session_state.portfolio.empty:
        st.write("보유 중인 종목이 없습니다.")
    else:
        # 포트폴리오 출력 및 Sell 기능
        for idx, row in st.session_state.portfolio.iterrows():
            pcol1, pcol2, pcol3, pcol4, pcol5 = st.columns([2, 1, 1, 1, 2])
            pcol1.write(f"**{row['종목명']}** ({row['종목코드']})")
            pcol2.write(f"{row['수량']}주")
            profit = (row['현재가'] - row['매수단가']) / row['매수단가'] * 100
            pcol3.write(f"{profit:+.2f}%")

            # Sell 버튼
            if pcol4.button("📉 Sell", key=f"sell_{idx}"):
                st.session_state.sell_target = row['종목명']
                st.session_state.sell_idx = idx

        # Sell 입력창 (버튼 클릭 시 활성화)
        if 'sell_target' in st.session_state:
            st.divider()
            st.write(f"### 📍 {st.session_state.sell_target} 매도 정산")
            sell_price = st.number_input("매도가를 입력하세요", value=float(st.session_state.portfolio.loc[st.session_state.sell_idx, '현재가']))
            if st.button("정산 완료"):
                # 수익률 계산 및 로그 (실제로는 DB 저장)
                buy_price = st.session_state.portfolio.loc[st.session_state.sell_idx, '매수단가']
                qty = st.session_state.portfolio.loc[st.session_state.sell_idx, '수량']
                final_profit = (sell_price - buy_price) * qty
                st.success(f"{st.session_state.sell_target} 매도 완료! 실현 손익: {final_profit:,.0f}원")

                # 포트폴리오에서 삭제 (사용자가 원한 'Sell 후 업데이트' 로직)
                st.session_state.portfolio = st.session_state.portfolio.drop(st.session_state.sell_idx).reset_index(drop=True)
                del st.session_state.sell_target
                st.rerun()

    st.divider()
    st.subheader("➕ 종목 추가")
    with st.form("add_stock"):
        new_name = st.text_input("종목명")
        new_code = st.text_input("종목코드")
        new_qty = st.number_input("수량", min_value=1)
        new_price = st.number_input("매수단가", min_value=0)
        if st.form_submit_button("포트폴리오에 추가"):
            new_entry = {'종목코드': new_code, '종목명': new_name, '수량': new_qty, '매수단가': new_price, '현재가': new_price}
            st.session_state.portfolio = pd.concat([st.session_state.portfolio, pd.DataFrame([new_entry])], ignore_index=True)
            st.success(f"{new_name} 추가 완료!")
            st.rerun()

# --- Tab 3: 즐겨찾기/모니터링 ---
with tab3:
    st.subheader("⭐ 나의 관심 종목")
    if not st.session_state.favorites:
        st.write("즐겨찾기한 종목이 없습니다.")
    else:
        for fav in st.session_state.favorites:
            st.write(f"- {fav}")

    st.divider()
    st.subheader("👁️ 실시간 모니터링")
    st.write("모니터링 중인 종목들이 여기에 표시됩니다.")
