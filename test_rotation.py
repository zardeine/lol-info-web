import os
import requests
from dotenv import load_dotenv

# .env 파일에서 API 키 로드
load_dotenv()
RIOT_API_KEY = os.getenv('RIOT_API_KEY')

def get_champion_data():
    """챔피언 데이터 가져오기"""
    url = "http://ddragon.leagueoflegends.com/cdn/14.7.1/data/ko_KR/champion.json"
    response = requests.get(url)
    return response.json()

def get_free_rotation():
    """무료 로테이션 챔피언 가져오기"""
    url = "https://kr.api.riotgames.com/lol/platform/v3/champion-rotations"
    headers = {"X-Riot-Token": RIOT_API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()

def main():
    try:
        # 챔피언 데이터 가져오기
        champion_data = get_champion_data()
        
        # ID를 이름으로 변환하기 위한 딕셔너리 생성
        champion_dict = {}
        for champ_name, champ_info in champion_data['data'].items():
            champion_dict[int(champ_info['key'])] = champ_name
        
        # 무료 로테이션 정보 가져오기
        rotation_data = get_free_rotation()
        
        # 일반 로테이션 챔피언 출력
        print("\n이번 주 무료 챔피언:")
        print("-" * 50)
        for champ_id in rotation_data['freeChampionIds']:
            if champ_id in champion_dict:
                print(f"- {champion_dict[champ_id]}")
        
        # 뉴비 로테이션 챔피언 출력
        print("\n신규 유저 무료 챔피언:")
        print("-" * 50)
        for champ_id in rotation_data['freeChampionIdsForNewPlayers']:
            if champ_id in champion_dict:
                print(f"- {champion_dict[champ_id]}")
                
    except Exception as e:
        print(f"오류 발생: {str(e)}")

if __name__ == "__main__":
    main() 