import random
from datetime import date

def get_emission_reduction_tips(footprint, transportation, energy_usage, food_habits, consumer_goods):
    """
    탄소 발자국 감소를 위한 맞춤형 팁을 생성합니다.
    """
    tips = [
        f"당신의 탄소 발자국은 {footprint}kg CO2e입니다. 대중교통이나 자전거 이용을 늘려 {transportation * 0.2:.1f}kg 줄일 수 있습니다.",
        f"에너지 사용량 {energy_usage}kWh를 줄이기 위해 LED 조명으로 교체하면 약 {energy_usage * 0.1:.1f}kg의 CO2를 절감할 수 있습니다.",
        f"육류 소비를 주 {food_habits}회에서 {max(0, food_habits-1)}회로 줄이면 약 {food_habits * 5:.1f}kg의 CO2를 절감할 수 있습니다.",
        f"재사용 가능한 제품을 선택하여 {consumer_goods * 0.5:.1f}kg의 CO2 발생을 막을 수 있습니다.",
        "로컬 농산물을 구매하여 운송 과정에서 발생하는 탄소 배출을 줄이세요.",
        f"사용하지 않는 전자기기의 플러그를 뽑으면 연간 약 {energy_usage * 0.05:.1f}kg의 CO2를 절감할 수 있습니다.",
        "재활용을 철저히 하고, 업사이클링을 시도해보세요.",
        f"실내 온도를 1-2도 조절하여 에너지 사용을 줄이면 연간 약 {energy_usage * 0.08:.1f}kg의 CO2를 절감할 수 있습니다."
    ]
    return random.sample(tips, 3)

def get_policy_suggestions(region, emissions_data):
    """
    지역 특성에 맞는 정책을 제안합니다.
    """
    total_emission = sum(emissions_data.values())
    max_emission_sector = max(emissions_data, key=emissions_data.get)
    
    policies = [
        f"{region}의 {max_emission_sector} 부문 배출량({emissions_data[max_emission_sector]}천톤 CO2e)을 줄이기 위한 집중 정책 도입",
        f"{region} 내 신재생 에너지 발전 시설 확대로 연간 {total_emission * 0.1:.1f}천톤 CO2e 감축 목표",
        f"{region} 기업들의 탄소 배출 감축을 위한 인센티브 제도 도입으로 {total_emission * 0.05:.1f}천톤 CO2e 감축 유도",
        f"{region} 내 녹지 공간 확충 및 도시 숲 조성으로 연간 {total_emission * 0.02:.1f}천톤 CO2e 흡수 증대",
        f"{region} 주민 대상 탄소중립 교육 프로그램 운영으로 가정 부문 {emissions_data.get('가정', 0) * 0.1:.1f}천톤 CO2e 감축",
        f"{region} 내 에너지 효율이 높은 건물 리모델링 지원으로 건물 부문 {emissions_data.get('건물', 0) * 0.15:.1f}천톤 CO2e 감축",
        f"{region} 폐기물 재활용률 향상을 위한 분리수거 개선으로 폐기물 부문 {emissions_data.get('폐기물', 0) * 0.2:.1f}천톤 CO2e 감축",
        f"{region} 내 전기차 충전 인프라 확충 및 전기차 보급 확대로 수송 부문 {emissions_data.get('수송', 0) * 0.1:.1f}천톤 CO2e 감축"
    ]
    return random.sample(policies, 4)

def generate_eco_mission():
    """
    일일 환경 미션을 생성합니다.
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
    탄소 배출 데이터를 바탕으로 퀴즈 문제를 생성합니다.
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
            "question": "탄소 배출량이 가장 많은 지역은?",
            "options": options,
            "correct_answer": highest_emitter,
            "explanation": f"{highest_emitter}의 탄소 배출량은 {carbon_data[highest_emitter]}천톤 CO2eq로, 가장 높습니다."
        }
    
    elif question_type == "lowest_emitter":
        lowest_emitter = min(carbon_data, key=carbon_data.get)
        options = random.sample(list(carbon_data.keys()), 4)
        if lowest_emitter not in options:
            options[0] = lowest_emitter
        random.shuffle(options)
        
        return {
            "question": "탄소 배출량이 가장 적은 지역은?",
            "options": options,
            "correct_answer": lowest_emitter,
            "explanation": f"{lowest_emitter}의 탄소 배출량은 {carbon_data[lowest_emitter]}천톤 CO2eq로, 가장 낮습니다."
        }
    
    elif question_type == "compare_cities":
        cities = random.sample(list(carbon_data.keys()), 2)
        higher_emitter = max(cities, key=lambda x: carbon_data[x])
        lower_emitter = min(cities, key=lambda x: carbon_data[x])
        
        return {
            "question": f"{cities[0]}와 {cities[1]} 중 탄소 배출량이 더 많은 지역은?",
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
            "question": "전체 지역의 총 탄소 배출량은 약 얼마일까요? (천톤 CO2eq)",
            "options": options,
            "correct_answer": round(total_emissions),
            "explanation": f"전체 지역의 총 탄소 배출량은 약 {round(total_emissions)}천톤 CO2eq입니다."
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
            "question": "평균 이상의 탄소를 배출하는 지역의 수는?",
            "options": options,
            "correct_answer": correct_answer,
            "explanation": f"전체 지역의 평균 탄소 배출량은 약 {round(average_emission)}천톤 CO2eq이며, {correct_answer}개 지역이 이를 초과합니다."
        }

    # 기본 반환 (이 부분까지 오면 안 되지만, 혹시 모를 경우를 대비)
    return {
        "question": "탄소 배출에 대한 다음 설명 중 옳은 것은?",
        "options": ["탄소 배출이 전혀 없는 지역이 있다", "모든 지역의 탄소 배출량이 동일하다", "서울이 가장 많은 탄소를 배출한다", "산업 지역이 가장 많은 탄소를 배출한다"],
        "correct_answer": "산업 지역이 가장 많은 탄소를 배출한다",
        "explanation": "일반적으로 산업 활동이 많은 지역의 탄소 배출량이 가장 높습니다."
    }

def get_daily_eco_tip():
    """
    일일 환경 팁을 제공합니다.
    """
    tips = [
        "오늘은 짧은 거리는 걸어가보는 건 어떨까요? 건강에도 좋고 환경에도 좋습니다!",
        "식사 시 지역에서 생산된 채소를 선택해보세요. 운송 과정에서의 탄소 배출을 줄일 수 있습니다.",
        "오늘 하루 사용하지 않는 전자기기의 플러그를 뽑아보세요. 대기전력을 줄일 수 있습니다.",
        "샤워 시간을 1분만 줄여도 연간 CO2 배출량을 크게 줄일 수 있습니다.",
        "오늘은 재사용 가능한 컵이나 텀블러를 사용해보세요. 일회용품 사용을 줄일 수 있습니다.",
        "세탁은 모아서 한 번에 하면 에너지와 물을 절약할 수 있습니다.",
        "오늘 하루 냉난방 온도를 1도만 조절해보세요. 에너지 사용량을 크게 줄일 수 있습니다.",
        "장보러 갈 때는 재사용 가능한 장바구니를 사용해보세요. 비닐봉지 사용을 줄일 수 있습니다."
    ]
    
    # 날짜를 시드로 사용하여 매일 다른 팁을 제공
    random.seed(date.today().toordinal())
    return random.choice(tips)