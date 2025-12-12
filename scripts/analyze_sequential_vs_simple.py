"""
Compare sequential attack success vs simple attacks
"""

import json

# Load Day 1 simple attack results
with open('responses/simple_attacks_results.json', 'r') as f:
    simple_results = json.load(f)

# Load sequential test results
with open('responses/sequential_test_results.json', 'r') as f:
    sequential_results = json.load(f)

print("="*70)
print("SEQUENTIAL vs SIMPLE ATTACK COMPARISON")
print("="*70)

# Analyze by language
for language in ['english', 'hindi', 'hinglish']:
    print(f"\n{language.upper()}:")
    print("-"*70)
    
    # Simple attack (from Day 1 - just final turn)
    # Find the corresponding base behavior
    simple_lang = [r for r in simple_results 
                   if r['language'] == language and r['model'] == 'mistral:7b']
    
    # For banking/hacking specifically (to match our sequential test)
    hacking_simple = [r for r in simple_lang if 'hack' in r['prompt'].lower() or 'bank' in r['prompt'].lower()]
    
    if hacking_simple:
        simple_success = any(r['evaluation'] == 'y' for r in hacking_simple)
        print(f"Simple attack (Day 1):")
        print(f"  Prompt: {hacking_simple[0]['prompt'][:60]}...")
        print(f"  Result: {'✗ Model complied' if simple_success else '✓ Model refused'}")
    
    # Sequential attack
    seq_lang = [r for r in sequential_results if r['language'] == language]
    
    if seq_lang:
        # Check if ANY turn succeeded
        seq_success = any(r.get('evaluation') == 'y' for r in seq_lang)
        
        # Find which turn first succeeded
        first_success = None
        for r in sorted(seq_lang, key=lambda x: x['turn']):
            if r.get('evaluation') == 'y':
                first_success = r['turn']
                break
        
        print(f"\nSequential attack (Day 2):")
        print(f"  Total turns: 4")
        print(f"  Result: {'✗ Model complied' if seq_success else '✓ Model refused'}")
        if first_success:
            print(f"  First compliance at: Turn {first_success}")
        
        # Comparison
        print(f"\nComparison:")
        if seq_success and not simple_success:
            print(f"  🎯 Sequential attack WORKED where simple failed!")
            print(f"     Context-building increased effectiveness")
        elif seq_success and simple_success:
            print(f"  ⚠️  Both attacks succeeded")
            print(f"     Model vulnerable either way")
        elif not seq_success and simple_success:
            print(f"  🤔 Simple worked but sequential didn't")
            print(f"     Unexpected - context may have helped model refuse")
        else:
            print(f"  ✓ Both attacks failed")
            print(f"     Model has good defenses")

print("\n" + "="*70)
print("HYPOTHESIS TEST")
print("="*70)
print("""
Hypothesis: Context-building increases jailbreak success rate

Evidence needed:
- Sequential attack succeeds where simple attack failed
- Across multiple languages
- Consistent pattern

If YES → Scale up to 10-15 scenarios
If NO → Try different approach (obfuscation, role-play, etc.)
""")

