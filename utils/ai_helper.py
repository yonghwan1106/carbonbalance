import random

def get_emission_reduction_tips(footprint, transportation, energy_usage, food_habits, consumer_goods):
    """
    탄소 발자국 감소를 위한 팁을 생성합니다.
    실제 구현에서는 이 부분에 Claude API를 연동하여 더 지능적인 팁을 제공할 수 있습니다.
    """
    tips = [
        "대중교통이나 자전거 이용을 늘려보세요.",
        "불필요한 전등은 끄고, 에너지 효율이 높은 가전제품을 사용하세요.",
        "육류 소비를 줄이고 채식 위주의 식단을 시도해보세요.",
        "일회용품 사용을 줄이고 재사용 가능한 제품을 선택하세요.",
        "로컬 농산물을 구매하여 운송 과정에서 발생하는 탄소 배출을 줄이세요.",
        "집에서 사용하지 않는 전자기기의 플러그를 뽑아두세요.",
        "재활용을 철저히 하고, 업사이클링을 시도해보세요.",
        "실내 온도를 1-2도 조절하여 에너지 사용을 줄이세요."
    ]
    return random.sample(tips, 3)  # 무작위로 3개의 팁 선택

def get_policy_suggestions(region, emissions_data):
    """
    지역 특성에 맞는 정책을 제안합니다.
    실제 구현에서는 이 부분에 Claude API를 연동하여 더 맞춤화된 정책을 제안할 수 있습니다.
    """
    policies = [
        f"{region}의 대중교통 인프라 확충 및 이용 장려 정책",
        f"{region} 내 신재생 에너지 발전 시설 확대",
        f"{region} 기업들의 탄소 배출 감축을 위한 인센티브 제도 도입",
        f"{region} 내 녹지 공간 확충 및 도시 숲 조성 사업",
        f"{region} 주민 대상 탄소중립 교육 프로그램 운영",
        f"{region} 내 에너지 효율이 높은 건물 리모델링 지원 사업",
        f"{region} 폐기물 재활용률 향상을 위한 분리수거 개선 정책",
        f"{region} 내 전기차 충전 인프라 확충 및 전기차 보급 확대 정책"
    ]
    return random.sample(policies, 4)  # 무작위로 4개의 정책 선택

def generate_eco_mission():
    """
    일일 환경 미션을 생성합니다.
    실제 구현에서는 이 부분에 Claude API를 연동하여 더 다양하고 개인화된 미션을 생성할 수 있습니다.
    """
    missions = [
        {"description": "오늘 하루 대중교통만 이용하기", "carbon_reduction": 2.5},
        {"description": "일회용품 사용하지 않기", "carbon_reduction": 0.5},
        {"description": "채식 식단으로 하루 먹기", "carbon_reduction": 4.0},
        {"description": "사용하지 않는 전자기기 플러그 뽑기", "carbon_reduction": 1.0},
        {"description": "5분 이내 거리는 걸어가기", "carbon_reduction": 0.8},
        {"description": "재활용 쓰레기 분리배출 철저히 하기", "carbon_reduction": 0.3},
        {"description": "양치할 때 컵 사용하기", "carbon_reduction": 0.2},
        {"description": "오늘 하루 냉난방 1도 줄이기", "carbon_reduction": 1.5}
    ]
    return random.choice(missions)
