"""
Finding the optimal threshold for BanTopics
"""

import json
from llm_guard.input_scanners import BanTopics
from collections import defaultdict

print("="*70)
print("THRESHOLD SENSITIVITY ANALYSIS")
print("="*70)

# Load dataset
with open('data/multilingual_jailbreak_dataset.json', 'r', encoding='utf-8') as f:
    dataset = json.load(f)

# Test different thresholds
thresholds = [0.3, 0.4, 0.5, 0.6, 0.7]

results_by_threshold = {}

for threshold in thresholds:
    print(f"\n{'='*70}")
    print(f"TESTING THRESHOLD: {threshold}")
    print(f"{'='*70}")
    
    scanner = BanTopics(
        topics=["hacking", "violence", "illegal activities", "weapons", 
                "fraud", "privacy violation"],
        threshold=threshold
    )
    
    detection_by_language = defaultdict(lambda: {"total": 0, "detected": 0})
    
    for item in dataset:
        prompt = item['prompt']
        language = item['language']
        
        _, is_valid, risk_score = scanner.scan(prompt)
        detected = not is_valid
        
        detection_by_language[language]["total"] += 1
        if detected:
            detection_by_language[language]["detected"] += 1
    
    # Calculate rates
    rates = {}
    for language, stats in detection_by_language.items():
        rate = (stats["detected"] / stats["total"]) * 100
        rates[language] = rate
        print(f"  {language:15s}: {stats['detected']:2d}/{stats['total']:2d} = {rate:5.1f}%")
    
    results_by_threshold[threshold] = rates

# Summary
print("\n" + "="*70)
print("SUMMARY: DETECTION RATES BY THRESHOLD")
print("="*70)
print(f"{'Threshold':<12} {'English':>10} {'Hindi':>10} {'Hinglish':>10}")
print("-"*70)

for threshold in thresholds:
    rates = results_by_threshold[threshold]
    print(f"{threshold:<12.1f} {rates['english']:>9.1f}% {rates['hindi']:>9.1f}% {rates['hinglish']:>9.1f}%")

print("\n" + "="*70)
print("RECOMMENDATIONS")
print("="*70)

# Find best threshold (highest detection without too many false positives)
best_threshold = None
best_avg = 0

for threshold in thresholds:
    rates = results_by_threshold[threshold]
    avg = (rates['english'] + rates['hinglish']) / 2  # Average of Roman scripts
    
    if avg > best_avg:
        best_avg = avg
        best_threshold = threshold

print(f"""
For jailbreak detection, you want HIGH detection rates (catch harmful prompts).

Recommended threshold: {best_threshold}
- This catches the most harmful prompts
- English detection: {results_by_threshold[best_threshold]['english']:.1f}%
- Hinglish detection: {results_by_threshold[best_threshold]['hinglish']:.1f}%

Note: Lower threshold = more sensitive = catches more (but may have false positives)
      Higher threshold = less sensitive = misses more (but fewer false positives)

For safety-critical applications, err on the side of LOWER thresholds!
""")

