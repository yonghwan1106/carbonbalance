import pandas as pd

# 데이터가 담긴 파일이나 데이터베이스에서 데이터를 읽어오는 함수
def load_data():
    # 여기서는 예시로 DataFrame을 직접 생성합니다.
    # 실제 사용 시에는 데이터 파일을 읽거나 데이터베이스에서 쿼리하는 코드로 대체됩니다.
    data = {
        '연도': [2019, 2020, 2021, 2022, 2023],
        '총탄소배출량': [50000, 52000, 53000, 55000, 57000]
    }
    df = pd.DataFrame(data)
    return df

def get_latest_national_data():
    df = load_data()
    
    # 최신 데이터와 전년 대비 변화량 계산
    latest_year = df['연도'].max()
    latest_data = df[df['연도'] == latest_year]
    
    previous_year = latest_year - 1
    previous_data = df[df['연도'] == previous_year]
    
    total_emissions = latest_data['총탄소배출량'].values[0]
    
    emissions_change = 0
    if not previous_data.empty:
        previous_emissions = previous_data['총탄소배출량'].values[0]
        emissions_change = ((total_emissions - previous_emissions) / previous_emissions) * 100
    
    return {
        'total_emissions': total_emissions,
        'emissions_change': emissions_change
    }

def analyze_emissions_trend(region_data):
    """
    특정 지역의 배출 트렌드를 분석합니다.
    """
    recent_years = region_data.sort_values('연도').tail(5)
    
    total_change = recent_years['탄소배출량'].iloc[-1] - recent_years['탄소배출량'].iloc[0]
    percent_change = (total_change / recent_years['탄소배출량'].iloc[0]) * 100
    
    if percent_change > 0:
        trend = f"증가 추세 (+{percent_change:.1f}%)"
    elif percent_change < 0:
        trend = f"감소 추세 ({percent_change:.1f}%)"
    else:
        trend = "안정적"
    
    return f"최근 5년간 {trend}. 연간 평균 변화량: {total_change/5:.0f} tCO2eq"
