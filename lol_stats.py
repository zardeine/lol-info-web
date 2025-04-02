import os
import requests
from dotenv import load_dotenv
from datetime import datetime

# .env 파일에서 API 키 로드
load_dotenv()
RIOT_API_KEY = os.getenv('RIOT_API_KEY')

def get_summoner_by_name(summoner_name):
    """소환사 정보 조회"""
    url = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
    headers = {"X-Riot-Token": RIOT_API_KEY}
    print(f"API 요청 URL: {url}")
    print(f"API 키: {RIOT_API_KEY}")
    response = requests.get(url, headers=headers)
    print(f"응답 상태 코드: {response.status_code}")
    print(f"응답 내용: {response.text}")
    return response.json()

def get_recent_matches(puuid):
    """최근 매치 ID 조회"""
    url = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    headers = {"X-Riot-Token": RIOT_API_KEY}
    params = {"count": 10}
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def get_match_details(match_id):
    """매치 상세 정보 조회"""
    url = f"https://asia.api.riotgames.com/lol/match/v5/matches/{match_id}"
    headers = {"X-Riot-Token": RIOT_API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()

def print_match_info(match_data, summoner_name):
    """매치 정보 출력"""
    for participant in match_data['info']['participants']:
        if participant['summonerName'] == summoner_name:
            champion = participant['championName']
            kills = participant['kills']
            deaths = participant['deaths']
            assists = participant['assists']
            win = participant['win']
            game_duration = match_data['info']['gameDuration']
            minutes = game_duration // 60
            seconds = game_duration % 60
            
            print(f"\n게임 결과: {'승리' if win else '패배'}")
            print(f"챔피언: {champion}")
            print(f"KDA: {kills}/{deaths}/{assists}")
            print(f"게임 시간: {minutes}분 {seconds}초")
            print("-" * 50)

def main():
    if not RIOT_API_KEY:
        print("Error: Riot API 키를 .env 파일에 설정해주세요.")
        return

    summoner_name = "Hide on bush"  # 소환사 이름을 직접 지정
    
    try:
        # 소환사 정보 조회
        summoner_data = get_summoner_by_name(summoner_name)
        if 'status' in summoner_data:
            print(f"Error: {summoner_data['status']['message']}")
            return

        puuid = summoner_data['puuid']
        print(f"\n{summoner_name}님의 최근 10게임 전적을 조회합니다...")
        
        # 최근 매치 ID 조회
        match_ids = get_recent_matches(puuid)
        
        # 각 매치의 상세 정보 조회 및 출력
        for match_id in match_ids:
            match_data = get_match_details(match_id)
            print_match_info(match_data, summoner_name)

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 