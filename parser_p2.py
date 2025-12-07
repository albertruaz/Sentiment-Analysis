"""
parser_p2.py
고도를 기다리며 (play2.txt) 파싱

규칙:
- 화자 라벨: VLADIMIR: / ESTRAGON: / POZZO: / LUCKY: / BOY:
- ^[A-Z]+:$ 패턴인 줄을 만나면 화자 변경
- 첫 화자 등장 전까지는 Narrator
- 같은 화자의 연속 대사는 하나로 합침
"""

import json
import re
import os

# ===== 설정 =====
INPUT_FILENAME = "data/play2.txt"
OUTPUT_FILENAME = "data/parsed/play2.json"

# 화자 라벨 패턴 (대문자로 시작하고 콜론으로 끝나는 줄)
SPEAKER_PATTERN = re.compile(r'^(VLADIMIR|ESTRAGON|POZZO|LUCKY|BOY):$')


def load_text(filepath: str) -> str:
    """텍스트 파일을 UTF-8로 읽어서 문자열 반환"""
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    return text


def clean_whitespace(s: str) -> str:
    """줄바꿈을 포함한 모든 연속 공백을 하나의 공백으로 정리"""
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def parse_play2(text: str):
    """
    play2.txt 파싱
    
    1. 줄 단위로 읽기
    2. SPEAKER: 패턴인 줄을 만나면 현재 블록 flush, 화자 변경
    3. 첫 화자 등장 전까지는 NARRATOR
    4. 각 블록은 줄바꿈 제거하고 하나의 문장으로
    """
    lines = text.split('\n')
    
    blocks = []
    current_speaker = "NARRATOR"
    current_lines = []
    
    for line in lines:
        stripped = line.strip()
        
        # 화자 라벨인지 확인
        match = SPEAKER_PATTERN.match(stripped)
        
        if match:
            # 현재까지 쌓인 텍스트를 블록으로 flush
            if current_lines:
                combined = ' '.join(current_lines)
                combined = clean_whitespace(combined)
                if combined:
                    blocks.append((current_speaker, combined))
                current_lines = []
            
            # 새 화자로 변경
            current_speaker = match.group(1)
        else:
            # 일반 텍스트 줄 - 현재 블록에 추가
            if stripped:
                current_lines.append(stripped)
    
    # 마지막 블록 flush
    if current_lines:
        combined = ' '.join(current_lines)
        combined = clean_whitespace(combined)
        if combined:
            blocks.append((current_speaker, combined))
    
    return blocks


def blocks_to_json(blocks):
    """
    블록 리스트를 JSON 구조로 변환.

    형태:
    {
      "1": { "speaker": "NARRATOR", "sentence": "..." },
      "2": { "speaker": "ESTRAGON", "sentence": "..." },
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

    # 2) 화자 기준으로 블록 분리
    blocks = parse_play2(text)

    # 3) JSON 구조로 변환
    json_data = blocks_to_json(blocks)

    # 4) 출력 디렉토리 생성
    os.makedirs(os.path.dirname(OUTPUT_FILENAME), exist_ok=True)

    # 5) JSON 파일로 저장
    with open(OUTPUT_FILENAME, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    print(f"총 {len(json_data)}개 문장을 생성했습니다.")
    print(f"결과 파일: {OUTPUT_FILENAME}")
    
    # 화자별 통계 출력
    speaker_counts = {}
    for speaker, _ in blocks:
        speaker_counts[speaker] = speaker_counts.get(speaker, 0) + 1
    
    print(f"\n화자별 통계:")
    for speaker, count in sorted(speaker_counts.items(), key=lambda x: -x[1]):
        print(f"  {speaker}: {count}개")


if __name__ == "__main__":
    main()
