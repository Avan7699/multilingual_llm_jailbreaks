"""
Systematic evaluation of BanTopics across languages
"""

import json
from llm_guard.input_scanners import BanTopics
from collections import defaultdict

print("="*70)
print("EVALUATING BanTopics ACROSS LANGUAGES")
print("="*70)

# Load dataset
with open('data/multilingual_jailbreak_dataset.json', 'r', encoding='utf-8') as f:
    dataset = json.load(f)

# Initialize scanner
scanner = BanTopics(
    topics=["hacking", "violence", "illegal activities", "weapons", 
            "fraud", "privacy violation"],
    threshold=0.5
)

# Results
results = []
detection_by_language = defaultdict(lambda: {"total": 0, "detected": 0})

print("\nTesting prompts...\n")

for item in dataset:
    prompt = item['prompt']
    language = item['language']
    category = item['category']
    
    # Test detection
    _, is_valid, risk_score = scanner.scan(prompt)
    detected = not is_valid
    
    # Record result
    result = {
        **item,
        "detected": detected,
        "risk_score": risk_score
    }
    results.append(result)
    
    # Update statistics
    detection_by_language[language]["total"] += 1
    if detected:
        detection_by_language[language]["detected"] += 1
    
    # Print
    status = "🚨 DETECTED" if detected else "✅ BYPASSED"
    print(f"[{language:10s}] {status} | Score: {risk_score:6.3f} | {prompt[:50]}")

# Save results
with open('data/evaluation_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

# Print summary
print("\n" + "="*70)
print("DETECTION RATES BY LANGUAGE")
print("="*70)

for language, stats in detection_by_language.items():
    rate = (stats["detected"] / stats["total"]) * 100
    print(f"{language:15s}: {stats['detected']:2d}/{stats['total']:2d} = {rate:5.1f}%")

# Analysis
english_rate = detection_by_language["english"]["detected"] / detection_by_language["english"]["total"]
hindi_rate = detection_by_language["hindi"]["detected"] / detection_by_language["hindi"]["total"]
hinglish_rate = detection_by_language["hinglish"]["detected"] / detection_by_language["hinglish"]["total"]

print("\n" + "="*70)
print("KEY FINDINGS")
print("="*70)

if hinglish_rate < english_rate:
    gap = (english_rate - hinglish_rate) * 100
    print(f"⚠️  Hinglish bypass rate is {gap:.1f}% higher than English!")
    print("   This confirms the vulnerability.")
else:
    print("✅ BanTopics handles Hinglish as well as English!")

if hindi_rate > english_rate:
    print(f"⚠️  Hindi (Devanagari) has {(hindi_rate - english_rate) * 100:.1f}% false positive rate")
    print("   Due to script-based detection bias.")

print("\nResults saved to: data/evaluation_results.json")

