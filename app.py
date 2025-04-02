from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import os
import requests
import random
from dotenv import load_dotenv

# .env 파일에서 API 키 로드
load_dotenv()
API_KEY = os.getenv('RIOT_API_KEY')

app = Flask(__name__)
bootstrap = Bootstrap(app)

def get_champion_data():
    """챔피언 데이터 가져오기"""
    url = "https://ddragon.leagueoflegends.com/cdn/13.24.1/data/ko_KR/champion.json"
    response = requests.get(url)
    print("챔피언 데이터 응답:", response.status_code)
    return response.json()

def get_champion_details(champion_id):
    """챔피언 상세 정보 가져오기"""
    url = f"https://ddragon.leagueoflegends.com/cdn/13.24.1/data/ko_KR/champion/{champion_id}.json"
    response = requests.get(url)
    print(f"챔피언 상세 정보 응답 ({champion_id}):", response.status_code)
    if response.status_code == 200:
        return response.json()["data"][champion_id]
    return None

def get_items_data():
    """아이템 데이터 가져오기"""
    url = "https://ddragon.leagueoflegends.com/cdn/13.24.1/data/ko_KR/item.json"
    response = requests.get(url)
    print("아이템 데이터 응답:", response.status_code)
    if response.status_code == 200:
        return response.json()
    return None

def get_patch_notes():
    """최근 패치 노트 정보 가져오기 (실제로는 API가 아니라 정적 데이터)"""
    patch_notes = {
        "version": "13.24.1",
        "highlights": [
            "아칼리 스킬 조정",
            "징크스 버프",
            "카직스 너프",
            "가렌 질럿 스킨 추가",
            "새로운 서포터 아이템"
        ],
        "date": "2023.12.15"
    }
    return patch_notes

def get_free_rotation():
    """무료 챔피언 로테이션 정보 가져오기"""
    url = "https://kr.api.riotgames.com/lol/platform/v3/champion-rotations"
    headers = {"X-Riot-Token": API_KEY}
    response = requests.get(url, headers=headers)
    print("무료 로테이션 응답:", response.status_code)
    return response.json()

def get_challenger_league():
    """챌린저 리그 정보 가져오기"""
    url = "https://kr.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5"
    headers = {"X-Riot-Token": API_KEY}
    response = requests.get(url, headers=headers)
    print("챌린저 리그 응답:", response.status_code)
    return response.json()

def get_grandmaster_league():
    """그랜드마스터 리그 정보 가져오기"""
    url = "https://kr.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5"
    headers = {"X-Riot-Token": API_KEY}
    response = requests.get(url, headers=headers)
    print("그랜드마스터 리그 응답:", response.status_code)
    return response.json()

def get_master_league():
    """마스터 리그 정보 가져오기"""
    url = "https://kr.api.riotgames.com/lol/league/v4/masterleagues/by-queue/RANKED_SOLO_5x5"
    headers = {"X-Riot-Token": API_KEY}
    response = requests.get(url, headers=headers)
    print("마스터 리그 응답:", response.status_code)
    return response.json()

def get_summoner_name(summoner_id, puuid):
    """소환사 ID와 puuid로 소환사 이름 조회"""
    # Development API Key 제한으로 사용하지 않음
    return f"소환사 #{summoner_id[:6]}..."

@app.route('/')
def index():
    try:
        # 챔피언 데이터 가져오기
        champion_data = get_champion_data()
        champion_dict = {champion['key']: champion['name'] for champion in champion_data['data'].values()}
        champion_id_dict = {champion['key']: champion_id for champion_id, champion in champion_data['data'].items()}
        
        # 무료 로테이션 데이터 가져오기
        rotation_data = get_free_rotation()
        free_champions = []
        for champion_id in rotation_data['freeChampionIds']:
            if str(champion_id) in champion_dict:
                free_champions.append({
                    'id': champion_id_dict.get(str(champion_id), ""),
                    'name': champion_dict[str(champion_id)]
                })
        
        new_player_champions = []
        for champion_id in rotation_data['freeChampionIdsForNewPlayers']:
            if str(champion_id) in champion_dict:
                new_player_champions.append({
                    'id': champion_id_dict.get(str(champion_id), ""),
                    'name': champion_dict[str(champion_id)]
                })
        
        # 랭킹 데이터 가져오기
        challenger_data = get_challenger_league()
        challenger_players = sorted(challenger_data['entries'], key=lambda x: x['leaguePoints'], reverse=True)[:10]
        
        grandmaster_data = get_grandmaster_league()
        grandmaster_players = sorted(grandmaster_data['entries'], key=lambda x: x['leaguePoints'], reverse=True)[:10]
        
        master_data = get_master_league()
        master_players = sorted(master_data['entries'], key=lambda x: x['leaguePoints'], reverse=True)[:10]
        
        # 패치 노트 가져오기
        patch_notes = get_patch_notes()
        
        # 아이템 데이터 가져오기
        items_data = get_items_data()
        popular_items = []
        if items_data:
            item_list = list(items_data['data'].items())
            random.shuffle(item_list)
            for item_id, item in item_list[:8]:
                # 일부 아이템만 표시 (소모품, 특수 아이템 제외)
                if item.get('gold', {}).get('total', 0) > 1000:
                    popular_items.append({
                        'id': item_id,
                        'name': item['name'],
                        'description': item.get('plaintext', ''),
                        'gold': item.get('gold', {}).get('total', 0)
                    })
        
        # 영웅 상세 정보 가져오기 (무작위 3명)
        featured_champions = []
        champion_keys = list(champion_data['data'].keys())
        random.shuffle(champion_keys)
        for champion_key in champion_keys[:3]:
            champion_detail = get_champion_details(champion_key)
            if champion_detail:
                featured_champions.append({
                    'id': champion_key,
                    'name': champion_detail['name'],
                    'title': champion_detail['title'],
                    'lore': champion_detail['lore'][:200] + '...' if len(champion_detail['lore']) > 200 else champion_detail['lore'],
                    'spells': champion_detail['spells'][:4]
                })
        
        return render_template('index.html',
                             free_champions=free_champions,
                             new_player_champions=new_player_champions,
                             challenger_players=challenger_players,
                             grandmaster_players=grandmaster_players,
                             master_players=master_players,
                             patch_notes=patch_notes,
                             popular_items=popular_items,
                             featured_champions=featured_champions)
    except Exception as e:
        print("에러 발생:", str(e))
        return f"데이터를 가져오는 중 오류가 발생했습니다: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True) 