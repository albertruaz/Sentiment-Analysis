"""
analyze.py
파싱된 JSON 파일을 읽어서 HuggingFace 모델로 각 문장별 감정 분석 수행
모델: SamLowe/roberta-base-go_emotions

입력 형식: {id: {speaker, sentence}}
출력 형식: {id: {speaker, sentence, emotions}}

play1, play2 동시 처리
"""

import json
import os
from transformers import pipeline

# 처리할 파일 목록
PLAY_FILES = ["play1.json", "play2.json"]


def load_parsed_json(filepath):
    """파싱된 JSON 파일 로드"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def analyze_emotions(data, classifier, tokenizer, play_name):
    """각 문장에 대해 감정 분석 수행"""
    results = {}
    total_sentences = len(data)
    
    for sentence_id, item in data.items():
        print(f"[{play_name}] 문장 {sentence_id}/{total_sentences} 분석 중...")
        
        # 새 형식: item은 {speaker, sentence} 딕셔너리
        speaker = item["speaker"]
        sentence = item["sentence"]
        
        # 토큰 길이를 기준으로 정확하게 512 token으로 잘라내기
        tokens = tokenizer(
            sentence,
            max_length=512,
            truncation=True,
            return_tensors="pt"
        )
        truncated_text = tokenizer.decode(tokens["input_ids"][0], skip_special_tokens=True)
        
        # 감정 분석 수행
        model_output = classifier(truncated_text)[0]  # emotion 리스트
        
        # 결과 저장 (speaker 정보 포함)
        results[sentence_id] = {
            "speaker": speaker,
            "sentence": sentence,
            "emotions": model_output
        }
    
    return results


def save_results(results, output_path):
    """분석 결과를 JSON으로 저장"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"결과 저장 완료: {output_path}")


def print_summary(results, play_name):
    """간단한 요약 출력"""
    print(f"\n=== [{play_name}] 분석 요약 (상위 10개 문장) ===")
    for i, (sentence_id, result) in enumerate(results.items()):
        if i >= 10:
            break
        top_emotion = max(result["emotions"], key=lambda x: x["score"])
        print(f"문장 {sentence_id} ({result['speaker']}): {top_emotion['label']} ({top_emotion['score']:.4f})")


def main():
    # 모델 한 번만 로드
    print("모델 로딩 중...")
    classifier = pipeline(
        task="text-classification", 
        model="SamLowe/roberta-base-go_emotions", 
        top_k=None,
        truncation=True,
        max_length=512
    )
    tokenizer = classifier.tokenizer
    print("모델 로딩 완료!\n")
    
    # play1, play2 순차 처리
    for filename in PLAY_FILES:
        input_path = os.path.join("data", "parsed", filename)
        
        if not os.path.exists(input_path):
            print(f"파일 없음, 건너뜀: {input_path}")
            continue
        
        play_name = os.path.splitext(filename)[0]  # "play1" 또는 "play2"
        print(f"\n{'='*50}")
        print(f"처리 중: {play_name}")
        print(f"{'='*50}")
        
        # 출력 파일 경로
        output_filename = f"{play_name}_result.json"
        output_path = os.path.join("result", output_filename)
        
        # 로드, 분석, 저장
        data = load_parsed_json(input_path)
        results = analyze_emotions(data, classifier, tokenizer, play_name)
        save_results(results, output_path)
        print_summary(results, play_name)
    
    print("\n\n모든 작품 분석 완료!")


if __name__ == "__main__":
    main()
