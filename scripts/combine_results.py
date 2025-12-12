"""
Combine detection performance with your model vulnerability data
"""

import json
import pandas as pd

# Load your model results
with open('responses/simple_attacks_results.json', 'r') as f:
    model_results = json.load(f)

# Load detection results
with open('detection_results/detector_performance.json', 'r') as f:
    detection_results = json.load(f)

# Create combined analysis
print("="*70)
print("COMBINED VULNERABILITY ANALYSIS")
print("="*70)

# For each language, calculate:
# 1. Detection rate
# 2. Model ASR (from your data)
# 3. Net vulnerability = (1 - detection_rate) × model_ASR

for language in ['english', 'hindi', 'hinglish']:
    print(f"\n{language.upper()}:")
    print("-"*70)
    
    # Detection performance
    for detector in ['BanTopics', 'PromptInjection']:
        det_results = [r for r in detection_results 
                      if r['language'] == language and r['detector'] == detector]
        detected = sum(1 for r in det_results if r['detected'])
        total = len(det_results)
        detection_rate = detected / total if total > 0 else 0
        
        # Model ASR from your data
        model_res = [r for r in model_results if r['language'] == language]
        successful = sum(1 for r in model_res if r['evaluation'] == 'y')
        model_asr = successful / len(model_res) if model_res else 0
        
        # Net vulnerability
        bypass_rate = 1 - detection_rate
        net_vulnerability = bypass_rate * model_asr
        
        print(f"\n{detector}:")
        print(f"  Detection rate: {detection_rate*100:.1f}%")
        print(f"  Model ASR: {model_asr*100:.1f}%")
        print(f"  Bypass rate: {bypass_rate*100:.1f}%")
        print(f"  Net vulnerability: {net_vulnerability*100:.1f}%")
        
        if language == 'hindi':
            english_det = [r for r in detection_results 
                          if r['language'] == 'english' and r['detector'] == detector]
            eng_detected = sum(1 for r in english_det if r['detected'])
            eng_rate = eng_detected / len(english_det) if english_det else 0
            
            gap = detection_rate - eng_rate
            print(f"  Detection gap vs English: {gap*100:+.1f}%")

