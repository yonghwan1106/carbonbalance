import streamlit as st
import plotly.express as px

def show_basic_info():
    st.title("탄소발자국 기본 정보")

    st.header("탄소발자국이란?")
    st.write("""
    탄소발자국은 개인, 조직, 제품 또는 이벤트가 직접 또는 간접적으로 발생시키는 온실가스 배출량을 이산화탄소 등가량으로 표현한 것입니다.
    이는 우리의 일상 활동이 기후변화에 미치는 영향을 측정하는 데 사용됩니다.
    """)

    st.header("전체 인류의 탄소배출 항목 순위")
    global_emissions = {
        '전기 및 난방': 31,
        '농업 및 토지 이용': 18,
        '산업': 12,
        '교통': 16,
        '건물': 5,
        '기타 에너지': 18
    }

    fig_global = px.pie(
        values=list(global_emissions.values()),
        names=list(global_emissions.keys()),
        title="전체 인류의 탄소배출 항목 비율"
    )
    st.plotly_chart(fig_global)

    st.header("개인 기준 탄소배출 항목 순위")
    personal_emissions = {
        '주거': 29,
        '교통': 24,
        '음식': 17,
        '소비재': 16,
        '서비스': 14
    }

    fig_personal = px.bar(
        x=list(personal_emissions.keys()),
        y=list(personal_emissions.values()),
        title="개인 기준 탄소배출 항목 비율",
        labels={'x': '항목', 'y': '비율 (%)'}
    )
    st.plotly_chart(fig_personal)

    st.header("탄소발자국 줄이는 방법")
    st.write("""
    1. 에너지 효율적인 가전제품 사용
    2. 대중교통, 자전거 이용 또는 도보 증가
    3. 육류 소비 줄이기
    4. 일회용품 사용 줄이기
    5. 재생 에너지 사용
    6. 불필요한 전자기기 플러그 뽑기
    7. 재활용 및 업사이클링 실천
    8. 로컬 푸드 소비하기
    """)

    st.header("알고 계셨나요?")
    st.info("""
    - 평균적으로 한 사람이 1년 동안 배출하는 이산화탄소량은 약 4톤입니다.
    - 1톤의 이산화탄소를 상쇄하기 위해서는 약 50그루의 나무를 심어야 합니다.
    - 육류 생산은 전 세계 온실가스 배출량의 약 15%를 차지합니다.
    """)

if __name__ == "__main__":
    show_basic_info()
