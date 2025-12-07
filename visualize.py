"""
visualize.py
캐릭터별 감정 분석 결과를 히트맵으로 시각화
play1, play2 동시 처리 - result 파일에서 speaker별로 분리하여 시각화
"""

import json
import os
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ============== CONFIG ==============
# 처리할 작품 목록
PLAY_FILES = ["play1_result.json", "play2_result.json"]

# 출력 폴더
OUTPUT_BASE_DIR = "visualize"
# ====================================

# go_emotions 모델의 28가지 감정 레이블 (neutral 포함)
EMOTION_LABELS = [
    'admiration', 'amusement', 'anger', 'annoyance', 'approval', 
    'caring', 'confusion', 'curiosity', 'desire', 'disappointment',
    'disapproval', 'disgust', 'embarrassment', 'excitement', 'fear',
    'gratitude', 'grief', 'joy', 'love', 'nervousness',
    'optimism', 'pride', 'realization', 'relief', 'remorse',
    'sadness', 'surprise', 'neutral'
]


def load_result_json(filepath):
    """분석 결과 JSON 파일 로드"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def split_by_speaker(result_data):
    """
    결과 데이터를 speaker별로 분리
    반환: {speaker: {sentence_id: data, ...}, ...}
    """
    speaker_data = defaultdict(dict)
    
    for sentence_id, data in result_data.items():
        speaker = data.get("speaker", "UNKNOWN")
        speaker_data[speaker][sentence_id] = data
    
    return dict(speaker_data)

def create_heatmap_data(results):
    """
    히트맵 데이터 생성
    x축: 해당 캐릭터가 등장하는 문장들만 (순서대로)
    y축: 28가지 감정 (neutral 포함)
    
    Returns:
        heatmap_matrix: (28, num_sentences) 크기의 감정 점수 행렬
        sentence_ids: 문장 ID 리스트 (x축 레이블용)
    """
    # 문장 ID를 정렬하여 순서대로 처리
    sorted_ids = sorted(results.keys(), key=lambda x: int(x))
    num_sentences = len(sorted_ids)
    
    # 히트맵 매트릭스 초기화 (감정 x 해당 캐릭터 문장 수)
    heatmap_matrix = np.zeros((len(EMOTION_LABELS), num_sentences))
    
    # 감정 레이블을 인덱스로 매핑
    emotion_to_idx = {label: idx for idx, label in enumerate(EMOTION_LABELS)}
    
    # 각 문장별로 감정 점수 채우기
    for col_idx, sentence_id in enumerate(sorted_ids):
        data = results[sentence_id]
        emotion_scores = {item["label"]: item["score"] for item in data["emotions"]}
        for emotion, score in emotion_scores.items():
            if emotion in emotion_to_idx:
                heatmap_matrix[emotion_to_idx[emotion], col_idx] = score
    
    return heatmap_matrix, sorted_ids

def visualize_heatmap(heatmap_matrix, sentence_ids, title, output_path=None):
    """히트맵 시각화 (0~0.3 범위, 0.3 이상은 0.3으로 클리핑)"""
    num_sentences = len(sentence_ids)
    
    # 그림 크기 설정 (문장 수에 따라 동적으로 조절)
    fig_width = max(12, num_sentences * 0.02)
    fig_height = 10
    
    plt.figure(figsize=(fig_width, fig_height))
    
    # 히트맵 생성 (vmax=0.3으로 설정하여 0.3 이상은 동일하게 표시)
    ax = sns.heatmap(
        heatmap_matrix,
        xticklabels=sentence_ids,
        yticklabels=EMOTION_LABELS,
        cmap='YlOrRd',
        cbar_kws={'label': 'Emotion Score'},
        vmin=0,
        vmax=0.3
    )
    
    # 제목 및 레이블 설정
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('Sentence Number', fontsize=12)
    plt.ylabel('Emotion', fontsize=12)
    
    # x축 레이블: 일부만 표시
    step = max(1, num_sentences // 30)
    ax.set_xticks(range(0, num_sentences, step))
    ax.set_xticklabels([sentence_ids[i] for i in range(0, num_sentences, step)], rotation=90, fontsize=6)
    
    plt.yticks(fontsize=9)
    
    plt.tight_layout()
    
    # 저장 또는 표시
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"히트맵 저장 완료: {output_path}")
    else:
        plt.show()
    
    plt.close()


def main():
    # play1, play2 순차 처리
    for filename in PLAY_FILES:
        result_path = os.path.join("result", filename)
        
        if not os.path.exists(result_path):
            print(f"파일 없음, 건너뜀: {result_path}")
            continue
        
        play_name = filename.replace("_result.json", "")  # "play1" 또는 "play2"
        
        print(f"\n{'='*50}")
        print(f"작품: {play_name}")
        print(f"{'='*50}")
        
        # 결과 파일 로드
        print(f"로딩: {result_path}")
        result_data = load_result_json(result_path)
        
        # speaker별로 분리
        speaker_data = split_by_speaker(result_data)
        print(f"발견된 speaker: {len(speaker_data)}명\n")
        
        # 출력 디렉토리 생성
        output_dir = os.path.join(OUTPUT_BASE_DIR, play_name)
        os.makedirs(output_dir, exist_ok=True)
        
        # 각 speaker별로 시각화
        for speaker, data in sorted(speaker_data.items()):
            print(f"=== {speaker} ===")
            
            if not data:
                print(f"  데이터 없음, 건너뜀")
                continue
            
            # 히트맵 데이터 생성
            heatmap_matrix, sentence_ids = create_heatmap_data(data)
            
            print(f"  문장 수: {len(data)}개")
            
            # 히트맵 시각화
            title = f"{play_name} - {speaker} Emotion Analysis"
            safe_speaker = speaker.replace("/", "_").replace("\\", "_").replace(" ", "_")
            output_path = os.path.join(output_dir, f"{safe_speaker}_heatmap.png")
            visualize_heatmap(heatmap_matrix, sentence_ids, title, output_path)
            
            # 감정 통계 출력 (평균)
            avg_scores = np.mean(heatmap_matrix, axis=1)
            top_indices = np.argsort(avg_scores)[::-1][:3]
            top_emotions = [f"{EMOTION_LABELS[idx]}({avg_scores[idx]:.3f})" for idx in top_indices]
            print(f"  상위 감정: {', '.join(top_emotions)}")
            print()
        
        print(f"히트맵이 '{output_dir}' 폴더에 저장되었습니다.")
    
    print("\n\n모든 작품 시각화 완료!")


if __name__ == "__main__":
    main()
