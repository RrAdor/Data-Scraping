#!/usr/bin/env python3
"""
Test script for sentiment analyzer
"""

import sys
import os
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SentimentalScope.settings')

import django
django.setup()

from myapp.ai_service import ai_service

def test_sentiment_analysis():
    """Test sentiment analyzer with different types of content"""
    
    test_cases = [
        {
            'text': 'This is amazing! I love this fantastic product. It works perfectly and exceeded my expectations.',
            'expected': 'positive'
        },
        {
            'text': 'This is terrible. I hate this awful product. It failed completely and disappointed me.',
            'expected': 'negative'
        },
        {
            'text': 'The government announced new economic policies. Officials said the data shows market stability.',
            'expected': 'neutral'
        },
        {
            'text': 'The weather was okay today. Nothing special happened.',
            'expected': 'neutral'
        },
        {
            'text': 'The company reported strong profits and excellent growth this quarter. Investors are very happy.',
            'expected': 'positive'
        },
        {
            'text': 'The system crashed again. This is frustrating and causing major problems for users.',
            'expected': 'negative'
        }
    ]
    
    print("🔍 Testing Sentiment Analyzer")
    print("=" * 50)
    
    for i, case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {case['expected'].upper()}")
        print(f"Text: {case['text'][:60]}...")
        
        result = ai_service.sentiment_analyzer.analyze_sentiment(case['text'])
        
        print(f"Result: {result['label']} ({result['confidence']*100:.1f}% confidence)")
        print(f"Scores: Pos={result['scores']['positive']:.2f}, "
              f"Neg={result['scores']['negative']:.2f}, "
              f"Neu={result['scores']['neutral']:.2f}")
        
        # Check if prediction matches expected
        is_correct = result['label'] == case['expected']
        print(f"✅ CORRECT" if is_correct else "❌ INCORRECT")
    
    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == '__main__':
    test_sentiment_analysis()
