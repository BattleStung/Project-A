#!/usr/bin/env python3
"""
Log Analysis Tool
Analyzes interaction logs to find improvement opportunities
"""

import json
import os
from collections import Counter, defaultdict
from datetime import datetime

LOG_DIR = "logs"

class LogAnalyzer:
    def __init__(self):
        self.interactions = []
        self.load_logs()
    
    def load_logs(self):
        """Load all log files"""
        if not os.path.exists(LOG_DIR):
            print(f"❌ No logs directory found at {LOG_DIR}")
            return
        
        for filename in os.listdir(LOG_DIR):
            if filename.startswith('interactions_') and filename.endswith('.jsonl'):
                filepath = os.path.join(LOG_DIR, filename)
                with open(filepath, 'r') as f:
                    for line in f:
                        try:
                            self.interactions.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue
        
        print(f"📊 Loaded {len(self.interactions)} interactions")
    
    def analyze(self):
        """Run full analysis"""
        if not self.interactions:
            print("No data to analyze yet. Generate some replies first!")
            return
        
        print("\n" + "="*60)
        print("📈 AI CUSTOMER SUPPORT ANALYSIS REPORT")
        print("="*60 + "\n")
        
        self.basic_stats()
        self.edit_analysis()
        self.tone_performance()
        self.common_issues()
        self.improvement_suggestions()
    
    def basic_stats(self):
        """Calculate basic statistics"""
        total = len(self.interactions)
        edited = sum(1 for i in self.interactions if i.get('edited'))
        accuracy = ((total - edited) / total * 100) if total > 0 else 0
        
        print("📊 BASIC STATISTICS")
        print("-" * 40)
        print(f"Total Interactions: {total}")
        print(f"Edited Responses:   {edited}")
        print(f"Accuracy Rate:      {accuracy:.1f}%")
        print()
    
    def edit_analysis(self):
        """Analyze what users edit"""
        print("✏️  EDIT PATTERNS")
        print("-" * 40)
        
        edits = [i for i in self.interactions if i.get('edited')]
        
        if not edits:
            print("No edits yet - AI performing well!")
            print()
            return
        
        edit_types = defaultdict(int)
        
        for interaction in edits:
            original = interaction.get('ai_reply', '')
            edited = interaction.get('user_edit', '')
            
            # Analyze edit types
            if len(edited) > len(original):
                edit_types['Added content'] += 1
            elif len(edited) < len(original):
                edit_types['Shortened response'] += 1
            else:
                edit_types['Rephrased'] += 1
        
        for edit_type, count in edit_types.items():
            percentage = (count / len(edits)) * 100
            print(f"{edit_type}: {count} ({percentage:.1f}%)")
        
        print()
    
    def tone_performance(self):
        """Analyze performance by tone"""
        print("🎭 TONE PERFORMANCE")
        print("-" * 40)
        
        tone_stats = defaultdict(lambda: {'total': 0, 'edited': 0})
        
        for interaction in self.interactions:
            tone = interaction.get('settings', {}).get('tone', 'unknown')
            tone_stats[tone]['total'] += 1
            if interaction.get('edited'):
                tone_stats[tone]['edited'] += 1
        
        for tone, stats in tone_stats.items():
            accuracy = ((stats['total'] - stats['edited']) / stats['total'] * 100) if stats['total'] > 0 else 0
            print(f"{tone.capitalize()}: {accuracy:.1f}% accuracy ({stats['total']} uses)")
        
        print()
    
    def common_issues(self):
        """Find common customer issues"""
        print("🔍 COMMON CUSTOMER ISSUES")
        print("-" * 40)
        
        keywords = Counter()
        
        for interaction in self.interactions:
            message = interaction.get('customer_message', '').lower()
            
            # Count issue keywords
            if 'refund' in message or 'money back' in message:
                keywords['refund_requests'] += 1
            if 'shipping' in message or 'delivery' in message:
                keywords['shipping_inquiries'] += 1
            if 'not working' in message or 'broken' in message:
                keywords['technical_issues'] += 1
            if 'cancel' in message:
                keywords['cancellations'] += 1
            if 'help' in message or 'support' in message:
                keywords['general_support'] += 1
        
        for issue, count in keywords.most_common(5):
            percentage = (count / len(self.interactions)) * 100
            print(f"{issue.replace('_', ' ').title()}: {count} ({percentage:.1f}%)")
        
        print()
    
    def improvement_suggestions(self):
        """Provide actionable improvement suggestions"""
        print("💡 IMPROVEMENT SUGGESTIONS")
        print("-" * 40)
        
        total = len(self.interactions)
        edited = sum(1 for i in self.interactions if i.get('edited'))
        
        if total < 10:
            print("• Collect more data (at least 50 interactions recommended)")
        
        if edited / total > 0.3:
            print("• High edit rate - consider refining system prompts")
            print("• Review edited responses to identify patterns")
        
        if edited / total < 0.1:
            print("• Excellent performance! Consider adding more features")
            print("• Test with different industries and tones")
        
        print("• Review most common issues to create templates")
        print("• Consider A/B testing different prompt variations")
        print()

def main():
    analyzer = LogAnalyzer()
    analyzer.analyze()
    
    print("="*60)
    print("💾 Log files location: ./logs/")
    print("📝 Tip: Use this data to improve your prompts!")
    print("="*60)

if __name__ == '__main__':
    main()