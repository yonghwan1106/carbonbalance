import streamlit as st
import plotly.express as px

def show_basic_info():
    st.title("🌍 탄소발자국 기본 정보")

    
    st.header("🔍 탄소발자국이란?")
    st.write("""
    탄소발자국은 개인, 조직, 제품 또는 이벤트가 직접 또는 간접적으로 발생시키는 온실가스 배출량을 이산화탄소 등가량으로 표현한 것입니다.
    이는 우리의 일상 활동이 기후변화에 미치는 영향을 측정하는 데 사용됩니다.
    """)

    
    st.header("🌐 전체 인류의 탄소배출 항목 순위")
    st.write("""
    전 세계적으로 인간 활동으로 인한 탄소 배출은 다음과 같은 비율로 이루어집니다:
    """)
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

    st.write("""
    - **전기 및 난방 (31%)**: 화석 연료를 사용한 전기 생산과 난방이 가장 큰 비중을 차지합니다.
    - **농업 및 토지 이용 (18%)**: 
        - 농업: 가축의 메탄 배출, 비료 사용, 벼 재배 등
        - 토지 이용 변화: 삼림 벌채, 초지를 농지로 전환 등
        - 이 비중이 큰 이유는 전 세계적으로 식량 생산을 위한 대규모 토지 변화와 집약적 농업이 이뤄지고 있기 때문입니다.
    - **교통 (16%)**: 자동차, 비행기, 선박 등 화석 연료를 사용하는 모든 운송 수단
    - **산업 (12%)**: 제조업, 건설업 등에서 사용되는 에너지와 공정 과정에서의 배출
    - **건물 (5%)**: 건물의 냉난방, 조명 등 건물 운영에 필요한 에너지 사용
    - **기타 에너지 (18%)**: 에너지 생산 과정에서의 누출, 연료 추출 및 처리 과정 등
    """)

    
    st.header("👤 개인 기준 탄소배출 항목 순위")
    st.write("""
    개인의 일상생활에서 발생하는 탄소 배출은 다음과 같은 비율로 이루어집니다:
    """)
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

    st.write("""
    - **주거 (29%)**: 
        - 전기 사용: 조명, 가전제품, 냉난방 등
        - 가스 사용: 취사, 온수 등
        - 주택 유지 보수 및 건축 과정에서의 배출
    - **교통 (24%)**:
        - 개인 차량 사용
        - 대중교통 이용
        - 항공 여행
    - **음식 (17%)**:
        - 식품 생산 및 가공 과정
        - 식품 운송
        - 음식물 쓰레기
    - **소비재 (16%)**:
        - 의류, 전자제품, 가구 등의 구매와 사용
        - 제품 생산, 운송, 폐기 과정에서의 배출
    - **서비스 (14%)**:
        - 의료, 교육, 금융 등 각종 서비스 이용
        - 여가 활동 및 문화 생활

    개인의 생활 방식과 선택에 따라 이 비율은 달라질 수 있습니다. 예를 들어, 대중교통을 주로 이용하는 사람은 교통 부문의 비율이 낮을 수 있고, 채식 위주의 식단을 가진 사람은 음식 부문의 비율이 낮을 수 있습니다.
    """)
    

    
    st.header("💡 탄소발자국 줄이는 방법")
    st.write("""
    1. 🏠 에너지 효율적인 가전제품 사용
    2. 🚲 대중교통, 자전거 이용 또는 도보 증가
    3. 🥗 육류 소비 줄이기
    4. ♻️ 일회용품 사용 줄이기
    5. 🌞 재생 에너지 사용
    6. 🔌 불필요한 전자기기 플러그 뽑기
    7. 🔄 재활용 및 업사이클링 실천
    8. 🍎 로컬 푸드 소비하기
    """)

    
    st.header("❓ 알고 계셨나요?")
    st.info("""
    - 🌳 평균적으로 한 사람이 1년 동안 배출하는 이산화탄소량은 약 4톤입니다.
    - 🌱 1톤의 이산화탄소를 상쇄하기 위해서는 약 50그루의 나무를 심어야 합니다.
    - 🥩 육류 생산은 전 세계 온실가스 배출량의 약 15%를 차지합니다.
    """)

if __name__ == "__main__":
    show_basic_info()

