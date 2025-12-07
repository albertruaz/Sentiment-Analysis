"""
parser_p1_2.py
play1_1.json (문장 데이터)과 play1_character.json (캐릭터 매핑)을
합쳐서 play1.json 생성

입력:
- data/parsed/play1_1.json: {"1": {"sentence": "..."}, ...}
- data/other/play1_character.json: {"Narrator": [], "Little Prince": [20, 22, ...], ...}

출력:
- data/parsed/play1.json: {"1": {"speaker": "NARRATOR", "sentence": "..."}, ...}
"""

import json
import os


# ===== 설정 =====
SENTENCES_FILE = "data/parsed/play1_1.json"
CHARACTER_FILE = "data/other/play1_character.json"
OUTPUT_FILE = "data/parsed/play1.json"


def load_json(filepath: str) -> dict:
    """JSON 파일 로드"""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def build_id_to_speaker(character_map: dict) -> dict:
    """
    캐릭터 매핑에서 {sentence_id: speaker} 딕셔너리 생성
    
    character_map: {"Little Prince": [20, 22, ...], "Pilot": [8, 10, ...], ...}
    반환: {"20": "LITTLE_PRINCE", "22": "LITTLE_PRINCE", ...}
    """
    id_to_speaker = {}
    
    for character, ids in character_map.items():
        # 캐릭터 이름 정규화 (공백 -> 언더스코어, 대문자)
        normalized = character.upper().replace(" ", "_")
        
        for sentence_id in ids:
            id_to_speaker[str(sentence_id)] = normalized
    
    return id_to_speaker


def merge_data(sentences: dict, id_to_speaker: dict) -> dict:
    """
    문장 데이터와 캐릭터 매핑을 합쳐서 최종 JSON 생성
    
    매핑에 없는 ID는 "NARRATOR"로 처리
    """
    result = {}
    
    for sentence_id, data in sentences.items():
        speaker = id_to_speaker.get(sentence_id, "NARRATOR")
        
        result[sentence_id] = {
            "speaker": speaker,
            "sentence": data["sentence"]
        }
    
    return result


def main():
    # 1) 파일 로드
    print(f"문장 데이터 로딩: {SENTENCES_FILE}")
    sentences = load_json(SENTENCES_FILE)
    
    print(f"캐릭터 매핑 로딩: {CHARACTER_FILE}")
    character_map = load_json(CHARACTER_FILE)
    
    # 2) ID -> Speaker 매핑 생성
    id_to_speaker = build_id_to_speaker(character_map)
    print(f"캐릭터 매핑된 대사 수: {len(id_to_speaker)}개")
    
    # 3) 데이터 병합
    result = merge_data(sentences, id_to_speaker)
    
    # 4) 출력 디렉토리 확인 및 저장
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n결과 파일 저장: {OUTPUT_FILE}")
    print(f"총 문장 수: {len(result)}개")
    
    # 5) 통계 출력
    speaker_counts = {}
    for data in result.values():
        speaker = data["speaker"]
        speaker_counts[speaker] = speaker_counts.get(speaker, 0) + 1
    
    print(f"\n캐릭터별 통계:")
    for speaker, count in sorted(speaker_counts.items(), key=lambda x: -x[1]):
        print(f"  {speaker}: {count}개")


if __name__ == "__main__":
    main()
