import random
import time
import pandas as pd

# 게임 상태 저장 및 업데이트를 위한 클래스
class EcoGame:
    def __init__(self):
        self.city_status = {
            '탄소배출량': 1000,  # 초기 탄소 배출량
            '점수': 0,
            '탄소크레딧': 0,
            '레벨': 1
        }
        self.missions = [
            {'이름': '재활용 캠페인', '점수': 10, '탄소감소': 50},
            {'이름': '전기 절약', '점수': 15, '탄소감소': 70},
            {'이름': '친환경 교통수단 이용', '점수': 20, '탄소감소': 100},
            {'이름': '에너지 효율 개선', '점수': 25, '탄소감소': 150}
        ]

    def show_status(self):
        print("\n현재 도시 상태")
        print(f"탄소 배출량: {self.city_status['탄소배출량']} 톤 CO2e")
        print(f"점수: {self.city_status['점수']}")
        print(f"탄소 크레딧: {self.city_status['탄소크레딧']}")
        print(f"레벨: {self.city_status['레벨']}")
    
    def perform_mission(self):
        mission = random.choice(self.missions)
        print(f"\n미션 수행: {mission['이름']}")
        print(f"점수 +{mission['점수']}, 탄소 배출량 -{mission['탄소감소']}")

        self.city_status['탄소배출량'] -= mission['탄소감소']
        self.city_status['점수'] += mission['점수']
        self.city_status['탄소크레딧'] += mission['점수'] * 0.5  # 0.5는 예시, 실제 비율에 따라 조정 가능

        if self.city_status['탄소배출량'] < 0:
            self.city_status['탄소배출량'] = 0
        
        # 레벨업
        if self.city_status['점수'] >= self.city_status['레벨'] * 50:
            self.city_status['레벨'] += 1
            print(f"\n레벨 업! 현재 레벨: {self.city_status['레벨']}")

    def game_loop(self):
        print("게임을 시작합니다!")
        while True:
            self.show_status()
            action = input("\n미션 수행하려면 '1' 입력, 종료하려면 'q' 입력: ")
            if action == '1':
                self.perform_mission()
            elif action.lower() == 'q':
                print("게임 종료!")
                break
            else:
                print("잘못된 입력입니다. 다시 시도해주세요.")

if __name__ == "__main__":
    game = EcoGame()
    game.game_loop()
