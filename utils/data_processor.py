import pandas as pd
import random

def load_gyeonggi_data():
    """
    경기도 탄소 배출 데이터를 로드합니다.
    실제 구현에서는 이 부분에 실제 데이터 파일을 로드하는 코드가 들어갑니다.
    """
    # 가상의 데이터 생성 (실제 구현 시 이 부분을 실제 데이터 로딩으로 대체해야 합니다)
    regions = ['수원시', '성남시', '용인시', '고양시', '부천시', '안산시', '안양시', '평택시', '시흥시', '김포시']
    years = range(2015, 2024)
    
    data = []
    for region in regions:
        for year in years:
            emissions = random.randint(1000000, 5000000)  # 가상의 배출량 (단위: tCO2eq)
            absorption = random.randint(100000, 500000)  # 가상의 흡수량
            data.append({
                '지역': region,
                '연도': year,
                '탄소배출량': emissions,
                '탄소흡수량': absorption,
                '가정': random.randint(100000, 500000),
                '상업': random.randint(100000, 500000),
                '산업': random.randint(200000, 1000000),
                '수송': random.randint(200000, 1000000),
                '공공': random.randint(50000, 200000),
                '기타': random.randint(50000, 200000)
            })
    
    return pd.DataFrame(data)

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
