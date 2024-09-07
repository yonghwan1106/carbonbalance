
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

def generate_quiz_question(carbon_data):
    """
    경기도 탄소 배출 데이터를 바탕으로 퀴즈 문제를 생성합니다.
    """
    question_types = [
        "highest_emitter",
        "lowest_emitter",
        "compare_cities",
        "total_emissions",
        "above_average",
    ]
    
    question_type = random.choice(question_types)
    
    if question_type == "highest_emitter":
        highest_emitter = max(carbon_data, key=carbon_data.get)
        options = random.sample(list(carbon_data.keys()), 4)
        if highest_emitter not in options:
            options[0] = highest_emitter
        random.shuffle(options)
        
        return {
            "question": "2020년 기준 경기도에서 탄소 배출량이 가장 많은 도시는?",
            "options": options,
            "correct_answer": highest_emitter,
            "explanation": f"{highest_emitter}의 탄소 배출량은 {carbon_data[highest_emitter]}천톤 CO2eq로, 경기도 내에서 가장 높습니다."
        }
    
    elif question_type == "lowest_emitter":
        lowest_emitter = min(carbon_data, key=carbon_data.get)
        options = random.sample(list(carbon_data.keys()), 4)
        if lowest_emitter not in options:
            options[0] = lowest_emitter
        random.shuffle(options)
        
        return {
            "question": "2020년 기준 경기도에서 탄소 배출량이 가장 적은 도시는?",
            "options": options,
            "correct_answer": lowest_emitter,
            "explanation": f"{lowest_emitter}의 탄소 배출량은 {carbon_data[lowest_emitter]}천톤 CO2eq로, 경기도 내에서 가장 낮습니다."
        }
    
    elif question_type == "compare_cities":
        cities = random.sample(list(carbon_data.keys()), 2)
        higher_emitter = max(cities, key=lambda x: carbon_data[x])
        lower_emitter = min(cities, key=lambda x: carbon_data[x])
        
        return {
            "question": f"2020년 기준 {cities[0]}와 {cities[1]} 중 탄소 배출량이 더 많은 도시는?",
            "options": cities,
            "correct_answer": higher_emitter,
            "explanation": f"{higher_emitter}의 탄소 배출량은 {carbon_data[higher_emitter]}천톤 CO2eq로, {lower_emitter}의 {carbon_data[lower_emitter]}천톤 CO2eq보다 높습니다."
        }
    
    elif question_type == "total_emissions":
        total_emissions = sum(carbon_data.values())
        options = [
            round(total_emissions * 0.8),
            round(total_emissions * 0.9),
            round(total_emissions),
            round(total_emissions * 1.1)
        ]
        random.shuffle(options)
        
        return {
            "question": "2020년 기준 경기도의 총 탄소 배출량은 약 얼마일까요? (천톤 CO2eq)",
            "options": options,
            "correct_answer": round(total_emissions),
            "explanation": f"2020년 기준 경기도의 총 탄소 배출량은 약 {round(total_emissions)}천톤 CO2eq입니다."
        }
    
    elif question_type == "above_average":
        average_emission = sum(carbon_data.values()) / len(carbon_data)
        above_average_cities = [city for city, emission in carbon_data.items() if emission > average_emission]
        correct_answer = len(above_average_cities)
        options = [correct_answer - 2, correct_answer - 1, correct_answer, correct_answer + 1]
        options = [max(0, option) for option in options]
        options = list(set(options))  # Remove duplicates
        if len(options) < 4:
            options.append(correct_answer + 2)
        options = sorted(options)[:4]  # Ensure we have exactly 4 options
        
        return {
            "question": "2020년 기준 경기도에서 평균 이상의 탄소를 배출하는 도시의 수는?",
            "options": options,
            "correct_answer": correct_answer,
            "explanation": f"경기도의 평균 탄소 배출량은 약 {round(average_emission)}천톤 CO2eq이며, {correct_answer}개 도시가 이를 초과합니다."
        }

    # 기본 반환 (이 부분까지 오면 안 되지만, 혹시 모를 경우를 대비)
    return {
        "question": "경기도의 탄소 배출에 대한 다음 설명 중 옳은 것은?",
        "options": ["경기도는 탄소 배출이 없다", "모든 도시의 탄소 배출량이 동일하다", "수원시가 가장 많은 탄소를 배출한다", "화성시가 가장 많은 탄소를 배출한다"],
        "correct_answer": "화성시가 가장 많은 탄소를 배출한다",
        "explanation": "2020년 기준 화성시의 탄소 배출량이 경기도 내에서 가장 높습니다."
    }
