"""
clean_raw.py
raw 텍스트 파일 정리:
- 페이지 번호 제거 (줄 전체가 숫자인 경우)
- 불필요한 빈 줄 정리
- 이상한 특수문자/링크 제거
- 줄바꿈 정리
"""

import re
import os

def clean_play1(text):
    """
    어린왕자 (play1_raw.txt) 정리
    - 페이지 번호 제거 (단독 숫자 줄)
    - 연속 빈 줄을 하나로
    - 불필요한 공백 정리
    """
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        stripped = line.strip()
        
        # 페이지 번호 제거 (줄 전체가 숫자인 경우)
        if re.match(r'^\d+$', stripped):
            continue
        
        # 챕터 번호만 있는 줄 유지 (예: "2", "3" 등은 챕터)
        # 하지만 5, 6 같은 페이지 번호는 제거해야 함
        # 페이지 번호는 보통 더 큰 숫자이므로 제거
        
        cleaned_lines.append(line)
    
    # 연속 빈 줄을 하나로 정리
    result = '\n'.join(cleaned_lines)
    result = re.sub(r'\n{3,}', '\n\n', result)
    
    return result.strip()


def clean_play2(text):
    """
    고도를 기다리며 (play2_raw.txt) 정리
    - 페이지 번호 제거
    - # 기호 및 이상한 마커 제거
    - Image from 등 링크/참조 제거
    - 연속 빈 줄 정리
    - 불필요한 공백 정리
    """
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        stripped = line.strip()
        
        # 페이지 번호 제거 (줄 전체가 숫자인 경우)
        if re.match(r'^\d+$', stripped):
            continue
        
        # "Image from" 등 이미지 참조 줄 제거
        if 'Image from' in stripped or 'timil.com' in stripped:
            continue
        
        # # 기호 제거 (줄 끝에 붙은 경우)
        line = re.sub(r'\s*#\s*$', '', line)
        line = re.sub(r'#\s+', '', line)  # 줄 중간의 # 제거
        
        # URL 패턴 제거
        line = re.sub(r'https?://\S+', '', line)
        
        cleaned_lines.append(line)
    
    # 연속 빈 줄을 하나로 정리
    result = '\n'.join(cleaned_lines)
    result = re.sub(r'\n{3,}', '\n\n', result)
    
    # 대사 앞의 불필요한 빈 줄 정리 (캐릭터: 형식 앞)
    # VLADIMIR:\n\n  text -> VLADIMIR:\ntext
    result = re.sub(r'(VLADIMIR|ESTRAGON|POZZO|LUCKY|BOY):\n\n+', r'\1:\n', result)
    
    return result.strip()


def main():
    raw_dir = os.path.join("data", "raw")
    
    # play1 정리
    play1_path = os.path.join(raw_dir, "play1_raw.txt")
    if os.path.exists(play1_path):
        print(f"정리 중: {play1_path}")
        with open(play1_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        cleaned = clean_play1(text)
        
        output_path = os.path.join("data", "play1.txt")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(cleaned)
        
        print(f"저장 완료: {output_path}")
        print(f"  원본 줄 수: {len(text.split(chr(10)))}")
        print(f"  정리 후 줄 수: {len(cleaned.split(chr(10)))}")
    
    # play2 정리
    play2_path = os.path.join(raw_dir, "play2_raw.txt")
    if os.path.exists(play2_path):
        print(f"\n정리 중: {play2_path}")
        with open(play2_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        cleaned = clean_play2(text)
        
        output_path = os.path.join("data", "play2.txt")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(cleaned)
        
        print(f"저장 완료: {output_path}")
        print(f"  원본 줄 수: {len(text.split(chr(10)))}")
        print(f"  정리 후 줄 수: {len(cleaned.split(chr(10)))}")


if __name__ == "__main__":
    main()
