import os
import requests
from dotenv import load_dotenv

# .env 파일에서 API 키 로드
load_dotenv()
RIOT_API_KEY = os.getenv('RIOT_API_KEY')

def test_api(url, description):
    """API 테스트"""
    headers = {"X-Riot-Token": RIOT_API_KEY}
    print(f"\n{description}:")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, headers=headers)
        print(f"상태 코드: {response.status_code}")
        print(f"응답 내용: {response.text[:200]}...")
    except Exception as e:
        print(f"오류: {str(e)}")
    print("-" * 50)

def main():
    # 테스트할 API 목록
    apis = [
        ("https://kr.api.riotgames.com/lol/platform/v3/champion-rotations", "무료 챔피언 로테이션"),
        ("https://kr.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5", "챌린저 랭킹"),
        ("https://kr.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5", "그랜드마스터 랭킹"),
        ("https://kr.api.riotgames.com/lol/league/v4/masterleagues/by-queue/RANKED_SOLO_5x5", "마스터 랭킹"),
        ("https://kr.api.riotgames.com/lol/clash/v1/tournaments", "클래시 토너먼트")
    ]
    
    print("API 테스트 시작")
    for url, desc in apis:
        test_api(url, desc)

if __name__ == "__main__":
    main() 