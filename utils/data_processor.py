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
    if '연도' not in region_data.columns or len(region_data) <= 1:
        return "트렌드 분석을 위한 충분한 데이터가 없습니다."
    
    recent_years = region_data.sort_values('연도').tail(5)
    total_emissions = recent_years['총배출량']
    
    if len(total_emissions) < 2:
        return "트렌드 분석을 위한 충분한 연도 데이터가 없습니다."
    
    trend = "증가" if total_emissions.iloc[-1] > total_emissions.iloc[0] else "감소"
    percent_change = ((total_emissions.iloc[-1] - total_emissions.iloc[0]) / total_emissions.iloc[0]) * 100
    
    analysis = f"최근 {len(recent_years)}년간 총 배출량은 {trend} 추세입니다. "
    analysis += f"첫 해 대비 마지막 해의 배출량 변화율은 {percent_change:.2f}%입니다."
    
    return analysis
