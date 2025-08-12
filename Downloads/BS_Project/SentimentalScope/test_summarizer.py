#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SentimentalScope.settings')
django.setup()

from myapp.ai_service import ai_service

# Test text for summarization
test_text = """
Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to natural intelligence displayed by animals and humans. Leading AI textbooks define the field as the study of "intelligent agents": any system that perceives its environment and takes actions that maximize its chance of achieving its goals. Some popular accounts use the term "artificial intelligence" to describe machines that mimic "cognitive" functions that humans associate with the human mind, such as "learning" and "problem solving".

The scope of AI is disputed: as machines become increasingly capable, tasks considered to require "intelligence" are often removed from the definition of AI, a phenomenon known as the AI effect. For instance, optical character recognition is frequently excluded from things considered to be AI, having become a routine technology. Artificial intelligence was founded as an academic discipline in 1956, and in the years since has experienced several waves of optimism, followed by disappointment and the loss of funding (known as an "AI winter"), followed by new approaches, success and renewed funding.

Machine learning, a subset of artificial intelligence, is the study of computer algorithms that improve automatically through experience and by the use of data. It is seen as a part of artificial intelligence. Machine learning algorithms build a model based on training data, known as a "training set", in order to make predictions or decisions without being explicitly programmed to do so. Machine learning algorithms are used in a wide variety of applications, such as in medicine, email filtering, speech recognition, and computer vision, where it is difficult or unfeasible to develop conventional algorithms to perform the needed tasks.
"""

def test_summarizer():
    print("Testing AI Summarizer...")
    print("=" * 50)
    
    try:
        # Test the summarizer directly
        print("1. Testing text summarizer directly:")
        summary_result = ai_service.text_summarizer.summarize_text(test_text)
        print(f"Summary: {summary_result['summary']}")
        print(f"Original length: {summary_result['original_length']} words")
        print(f"Summary length: {summary_result['summary_length']} words")
        print(f"Compression ratio: {summary_result['compression_ratio']}")
        print()
        
        # Test the complete AI service
        print("2. Testing complete AI analysis:")
        full_analysis = ai_service.analyze_content(test_text, include_summary=True, include_sentiment=False)
        print(f"Full analysis summary: {full_analysis.get('summary', 'NO SUMMARY')}")
        print()
        
        # Test individual components
        print("3. Testing individual components:")
        sentences = ai_service.text_summarizer.preprocess_text(test_text)
        print(f"Number of sentences: {len(sentences)}")
        print("First 3 sentences:")
        for i, sentence in enumerate(sentences[:3]):
            print(f"  {i+1}. {sentence}")
        print()
        
        # Test word frequency
        word_freq = ai_service.text_summarizer.calculate_word_frequency(sentences)
        print(f"Word frequency calculated: {len(word_freq)} unique words")
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        print("Top 10 words:", [f"{word}({freq:.2f})" for word, freq in top_words])
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_summarizer()
