"""
Quick analysis of results so far
"""

import json
from collections import defaultdict

# Load results
with open('responses/simple_attacks_results.json', 'r', encoding='utf-8') as f:
    results = json.load(f)

print("="*70)
print("CURRENT RESULTS ANALYSIS")
print("="*70)

# Overall stats
total = len(results)
by_eval = defaultdict(int)
for r in results:
    by_eval[r.get('evaluation', 'unknown')] += 1

print(f"\nTotal responses: {total}")
print(f"  Successful (y): {by_eval['y']}")
print(f"  Refused (n): {by_eval['n']}")
print(f"  Partial: {by_eval['partial']}")
print(f"  Errors: {by_eval['error']}")

# By model
models = set(r['model'] for r in results)
print(f"\n{'='*70}")
print("BY MODEL")
print(f"{'='*70}")

for model in sorted(models):
    model_results = [r for r in results if r['model'] == model]
    total_m = len(model_results)
    success_m = sum(1 for r in model_results if r.get('evaluation') == 'y')
    asr = (success_m / total_m * 100) if total_m > 0 else 0
    
    print(f"\n{model}:")
    print(f"  Tests: {total_m}")
    print(f"  Jailbreaks: {success_m}")
    print(f"  ASR: {asr:.1f}%")

# By language
print(f"\n{'='*70}")
print("BY LANGUAGE")
print(f"{'='*70}")

languages = set(r['language'] for r in results)
for lang in sorted(languages):
    lang_results = [r for r in results if r['language'] == lang]
    total_l = len(lang_results)
    success_l = sum(1 for r in lang_results if r.get('evaluation') == 'y')
    asr = (success_l / total_l * 100) if total_l > 0 else 0
    
    print(f"\n{lang}:")
    print(f"  Tests: {total_l}")
    print(f"  Jailbreaks: {success_l}")
    print(f"  ASR: {asr:.1f}%")

# By category
print(f"\n{'='*70}")
print("BY CATEGORY")
print(f"{'='*70}")

categories = set(r['category'] for r in results)
for cat in sorted(categories):
    cat_results = [r for r in results if r['category'] == cat]
    total_c = len(cat_results)
    success_c = sum(1 for r in cat_results if r.get('evaluation') == 'y')
    asr = (success_c / total_c * 100) if total_c > 0 else 0
    
    print(f"\n{cat}:")
    print(f"  Tests: {total_c}")
    print(f"  Jailbreaks: {success_c}")
    print(f"  ASR: {asr:.1f}%")

# Cross-analysis: Model × Language
print(f"\n{'='*70}")
print("MODEL × LANGUAGE")
print(f"{'='*70}")

for model in sorted(models):
    print(f"\n{model}:")
    for lang in sorted(languages):
        subset = [r for r in results if r['model'] == model and r['language'] == lang]
        total_s = len(subset)
        success_s = sum(1 for r in subset if r.get('evaluation') == 'y')
        asr = (success_s / total_s * 100) if total_s > 0 else 0
        
        print(f"  {lang:12s}: {success_s:2d}/{total_s:2d} = {asr:5.1f}%")

