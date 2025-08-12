#!/usr/bin/env python3
"""
Test script for Azure OpenAI integration
"""

import sys
import os
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SentimentalScope.settings')

import django
django.setup()

from myapp.ai_service import ai_service

def test_azure_openai():
    """Test Azure OpenAI integration"""
    
    test_cases = [
        {
            'text': 'This is an amazing product! I love how it works perfectly and exceeded all my expectations. Highly recommended!',
            'expected': 'positive'
        },
        {
            'text': 'This is terrible. The product failed completely and was a huge disappointment. Waste of money.',
            'expected': 'negative'
        },
        {
            'text': 'The company announced new quarterly results. Officials reported market data and economic indicators.',
            'expected': 'neutral'
        }
    ]
    
    print("🚀 Testing Azure OpenAI Integration")
    print("=" * 60)
    
    # Test sentiment analysis
    print("\n📊 SENTIMENT ANALYSIS TESTS")
    print("-" * 40)
    
    for i, case in enumerate(test_cases, 1):
        print(f"\nTest {i}: Expected {case['expected'].upper()}")
        print(f"Text: {case['text'][:50]}...")
        
        try:
            result = ai_service.analyze_sentiment(case['text'])
            print(f"Result: {result['label']} ({result['confidence']*100:.1f}% confidence)")
            print(f"Scores: Pos={result['scores']['positive']:.2f}, "
                  f"Neg={result['scores']['negative']:.2f}, "
                  f"Neu={result['scores']['neutral']:.2f}")
            
            # Check if prediction is reasonable
            is_correct = result['label'] == case['expected']
            print(f"✅ CORRECT" if is_correct else f"⚠️  Got {result['label']} instead")
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
    
    # Test text summarization
    print("\n📝 TEXT SUMMARIZATION TESTS")
    print("-" * 40)
    
    long_text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to natural intelligence displayed by animals and humans. Leading AI textbooks define the field as the study of "intelligent agents": any system that perceives its environment and takes actions that maximize its chance of achieving its goals. Some popular accounts use the term "artificial intelligence" to describe machines that mimic "cognitive" functions that humans associate with the human mind, such as "learning" and "problem solving".
    
    The scope of AI is disputed: as machines become increasingly capable, tasks considered to require "intelligence" are often removed from the definition of AI, a phenomenon known as the AI effect. A quip in Tesler's Theorem says "AI is whatever hasn't been done yet." For instance, optical character recognition is frequently excluded from things considered to be AI, having become a routine technology.
    
    Modern machine learning techniques are highly effective at perceiving patterns and making predictions. Many AI applications involve machine learning algorithms that can learn from data. Deep learning, a subset of machine learning, uses artificial neural networks with multiple layers to model and understand complex patterns in data.
    """
    
    print(f"\nSummarizing text ({len(long_text.split())} words)...")
    
    try:
        summary_result = ai_service.summarize_text(long_text)
        print(f"\n📋 SUMMARY:")
        print(f"'{summary_result['summary']}'")
        print(f"\n📈 METRICS:")
        print(f"Original: {summary_result['original_length']} words")
        print(f"Summary: {summary_result['summary_length']} words")
        print(f"Compression: {summary_result['compression_ratio']*100:.1f}%")
        
    except Exception as e:
        print(f"❌ SUMMARIZATION ERROR: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 Azure OpenAI Integration Test Completed!")
    
    # Test model info
    model_info = ai_service.get_model_info()
    print(f"\n🤖 AI SERVICE INFO:")
    for key, value in model_info.items():
        print(f"  {key}: {value}")

if __name__ == '__main__':
    test_azure_openai()
