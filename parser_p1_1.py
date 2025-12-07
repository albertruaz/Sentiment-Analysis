"""
parser_p1.py
어린왕자 (play1.txt) 파싱

규칙:
- 따옴표("") 안: 대사 → 하나의 문장으로
- 따옴표 밖: 나레이션 → 하나의 문장으로
- 줄바꿈은 공백으로 변환
"""

import json
import re
import os

# ===== 설정 =====
INPUT_FILENAME = "data/play1.txt"
OUTPUT_FILENAME = "data/parsed/play1_1.json"


def load_text(filepath: str) -> str:
    """텍스트 파일을 UTF-8로 읽어서 문자열 반환"""
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    return text


def clean_whitespace(s: str) -> str:
    """줄바꿈을 포함한 모든 연속 공백을 하나의 공백으로 정리"""
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def split_to_blocks(text: str):
    """
    텍스트를
      - 따옴표 안: 대사(dialogue)
      - 따옴표 밖: 나레이션(narration)
    으로 블록 단위로 분리.

    규칙:
      - 같은 " ... " 안은 한 문장으로 취급 (대사)
      - 따옴표 밖 부분은 다음 " 가 나오기 전까지 한 덩어리 (나레이션)
      - 줄바꿈은 모두 공백으로 바꾸고, 여러 공백은 하나로 축소
    """
    # 개행 통일
    text = text.replace("\r\n", "\n")

    # 곱슬 따옴표도 일반 따옴표로 통일
    text = text.replace(""", '"').replace(""", '"')

    blocks = []
    current_chars = []
    in_quote = False  # 지금 따옴표 안인지 여부

    for ch in text:
        if ch == '"':
            if in_quote:
                # 따옴표 닫힘: 지금까지 모은 글자를 하나의 '대사' 블록으로
                segment = "".join(current_chars).strip()
                if segment:
                    blocks.append(("DIALOGUE", clean_whitespace(segment)))
                current_chars = []
                in_quote = False
            else:
                # 따옴표 열림: 지금까지 모인 것은 '나레이션' 블록
                segment = "".join(current_chars).strip()
                if segment:
                    blocks.append(("NARRATOR", clean_whitespace(segment)))
                current_chars = []
                in_quote = True
        else:
            current_chars.append(ch)

    # 파일 끝까지 돌고 남은 부분 (보통 나레이션)
    segment = "".join(current_chars).strip()
    if segment:
        blocks.append(("NARRATOR", clean_whitespace(segment)))

    return blocks


def blocks_to_json(blocks):
    """
    블록 리스트를 JSON 구조로 변환.

    형태:
    {
      "1": { "speaker": "NARRATOR" or "DIALOGUE", "sentence": "..." },
      "2": { "speaker": "...", "sentence": "..." },
      ...
    }
    """
    data = {}
    for idx, (speaker, text) in enumerate(blocks, start=1):
        data[str(idx)] = {
            "speaker": speaker,
            "sentence": text
        }
    return data


def main():
    # 1) 텍스트 읽기
    print(f"파일 읽는 중: {INPUT_FILENAME}")
    text = load_text(INPUT_FILENAME)

    # 2) 따옴표 기준으로 대사/나레이션 블록 분리
    blocks = split_to_blocks(text)

    # 3) JSON 구조로 변환
    json_data = blocks_to_json(blocks)

    # 4) 출력 디렉토리 생성
    os.makedirs(os.path.dirname(OUTPUT_FILENAME), exist_ok=True)

    # 5) JSON 파일로 저장
    with open(OUTPUT_FILENAME, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    print(f"총 {len(json_data)}개 문장을 생성했습니다.")
    print(f"결과 파일: {OUTPUT_FILENAME}")
    
    # 통계 출력
    narrator_count = sum(1 for b in blocks if b[0] == "NARRATOR")
    dialogue_count = sum(1 for b in blocks if b[0] == "DIALOGUE")
    print(f"\n통계:")
    print(f"  NARRATOR: {narrator_count}개")
    print(f"  DIALOGUE: {dialogue_count}개")


if __name__ == "__main__":
    main()
