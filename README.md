# Sentiment-Analysis

문학 작품 속 문장을 통해 주인공의 감정을 분석하고, 작품 내용 변경에 따른 감정 변화를 비교하는 프로젝트입니다.

## 환경 설정

### Conda 환경 생성

```bash
# 환경 생성
conda create -n emotion python=3.10 -y

# 환경 활성화
conda activate emotion

# 필수 패키지 설치
pip install transformers torch matplotlib seaborn numpy
```

### 환경 삭제 (필요시)

```bash
conda deactivate
conda remove -n emotion --all -y
```

## 프로젝트 구조

```
emotion/
├── data/
│   ├── TheLittlePrince.txt
│   ├── Waiting for Godot.txt
│   └── parsed/
│       ├── {작품명}.json          # 파싱된 문장
│       └── {작품명}_group.json    # 그룹화된 블록
├── result/
│   ├── {작품명}_group_result.json # 감정 분석 결과
│   └── {작품명}_heatmap.png       # 시각화 이미지
├── parser.py      # 텍스트 → 문장 파싱
├── group.py       # 문장 → 블록 그룹화
├── analyze.py     # 감정 분석 (HuggingFace)
├── visualize.py   # 히트맵 시각화
└── README.md
```

## 사용 방법

### 1. 텍스트 파싱
```bash
# parser.py의 FILENAME 수정 후 실행
python parser.py
```

### 2. 블록 그룹화
```bash
# group.py의 FILENAME, NEW_START_LIST, BLOCK_SIZE 수정 후 실행
python group.py
```

### 3. 감정 분석
```bash
# analyze.py의 FILENAME 수정 후 실행
python analyze.py
```

### 4. 시각화
```bash
# visualize.py의 RESULT_FILENAME, TITLE 수정 후 실행
python visualize.py
```

## 모델 정보

- **모델**: [SamLowe/roberta-base-go_emotions](https://huggingface.co/SamLowe/roberta-base-go_emotions)
- **감정 종류**: 28가지 (admiration, amusement, anger, annoyance, approval, caring, confusion, curiosity, desire, disappointment, disapproval, disgust, embarrassment, excitement, fear, gratitude, grief, joy, love, nervousness, optimism, pride, realization, relief, remorse, sadness, surprise, neutral)
