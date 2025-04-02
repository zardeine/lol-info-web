import os
import requests
from dotenv import load_dotenv
import urllib.parse

# .env 파일에서 API 키 로드
load_dotenv()
RIOT_API_KEY = os.getenv('RIOT_API_KEY')

def test_api():
    # 여러 엔드포인트 테스트
    endpoints = [
        "https://kr.api.riotgames.com/lol/platform/v3/champion-rotations",
        "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/Faker",
        "https://asia.api.riotgames.com/lol/status/v4/platform-data"
    ]
    
    # 헤더 설정
    headers = {
        "X-Riot-Token": RIOT_API_KEY
    }
    
    print(f"테스트 시작")
    print(f"API 키: {RIOT_API_KEY}")
    
    for url in endpoints:
        print(f"\n엔드포인트 테스트: {url}")
        try:
            # API 요청
            response = requests.get(url, headers=headers)
            
            # 응답 출력
            print(f"응답 상태 코드: {response.status_code}")
            print(f"응답 내용: {response.text[:200]}...")  # 응답 내용 일부만 출력
            
        except Exception as e:
            print(f"오류 발생: {str(e)}")
        print("-" * 50)

if __name__ == "__main__":
    test_api() 