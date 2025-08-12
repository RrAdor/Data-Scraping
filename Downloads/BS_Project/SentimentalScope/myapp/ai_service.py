"""
AI Service Module for SentimentalScope
Azure OpenAI integration for sentiment analysis and text summarization
"""

import requests
import json
from datetime import datetime

class AzureOpenAIService:
    """Azure OpenAI service for sentiment analysis and text summarization"""
    
    def __init__(self):
        # Azure OpenAI configuration
        self.api_key = "2wuCk4AZtNAflvsGfbHjThuF7PKySOnOtW7DzxmgFDLtO07liLBJJQQJ99BCACHYHv6XJ3w3AAAAACOGaBwr"
        self.endpoint = "https://ai-raiyanbinsarwar0112ai312258162978.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2025-01-01-preview"
        self.headers = {
            'Content-Type': 'application/json',
            'api-key': self.api_key
        }
        print("Azure OpenAI Service initialized successfully")
    
    def analyze_sentiment(self, text):
        """Analyze sentiment using Azure OpenAI"""
        try:
            print(f"DEBUG: Analyzing sentiment with Azure OpenAI for text: {text[:100]}...")
            
            prompt = f"""
            Analyze the sentiment of the following text and provide a detailed response in JSON format.
            
            Text: "{text}"
            
            Please respond with ONLY a JSON object in this exact format:
            {{
                "label": "positive" | "negative" | "neutral",
                "confidence": 0.85,
                "scores": {{
                    "positive": 0.15,
                    "negative": 0.05,
                    "neutral": 0.80
                }}
            }}
            
            Rules:
            - label should be the dominant sentiment
            - confidence should be between 0.0 and 1.0
            - scores should add up to 1.0
            - Consider the overall tone, context, and emotional indicators
            """
            
            payload = {
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert sentiment analysis AI. Respond only with valid JSON format as requested."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 200,
                "temperature": 0.1
            }
            
            response = requests.post(self.endpoint, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            ai_response = result['choices'][0]['message']['content'].strip()
            
            # Parse JSON response
            try:
                sentiment_data = json.loads(ai_response)
                print(f"DEBUG: Azure OpenAI sentiment result: {sentiment_data}")
                return sentiment_data
            except json.JSONDecodeError as e:
                print(f"DEBUG: Failed to parse JSON response: {ai_response}")
                # Fallback response
                return {
                    'label': 'neutral',
                    'confidence': 0.5,
                    'scores': {'positive': 0.33, 'negative': 0.33, 'neutral': 0.34}
                }
                
        except Exception as e:
            print(f"DEBUG: Azure OpenAI sentiment analysis error: {e}")
            # Fallback response
            return {
                'label': 'neutral',
                'confidence': 0.5,
                'scores': {'positive': 0.33, 'negative': 0.33, 'neutral': 0.34}
            }
    
    def summarize_text(self, text, max_sentences=3, min_sentences=1):
        """Generate summary using Azure OpenAI"""
        try:
            print(f"DEBUG: Summarizing text with Azure OpenAI: {len(text)} characters")
            
            if not text or len(text.strip()) < 50:
                return {
                    'summary': text.strip() if text else "No content to summarize.",
                    'original_length': len(text.split()) if text else 0,
                    'summary_length': len(text.split()) if text else 0,
                    'compression_ratio': 1.0
                }
            
            prompt = f"""
            Create a concise, informative summary of the following text. Extract the key points and main ideas.
            
            Text: "{text}"
            
            Requirements:
            - Keep the summary between {min_sentences}-{max_sentences} sentences
            - Focus on the most important information
            - Maintain the original context and meaning
            - Make it readable and coherent
            - Avoid redundancy
            
            Provide only the summary text, no additional formatting or explanation.
            """
            
            payload = {
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an expert text summarization AI. Create concise, accurate summaries that capture the key information."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 300,
                "temperature": 0.3
            }
            
            response = requests.post(self.endpoint, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            summary = result['choices'][0]['message']['content'].strip()
            
            # Calculate metrics
            original_words = len(text.split())
            summary_words = len(summary.split())
            compression_ratio = round(summary_words / original_words, 2) if original_words > 0 else 1.0
            
            summary_result = {
                'summary': summary,
                'original_length': original_words,
                'summary_length': summary_words,
                'compression_ratio': compression_ratio
            }
            
            print(f"DEBUG: Azure OpenAI summary result: {summary_result}")
            return summary_result
            
        except Exception as e:
            print(f"DEBUG: Azure OpenAI summarization error: {e}")
            # Fallback summary
            sentences = text.split('.')[:max_sentences]
            fallback_summary = '. '.join(s.strip() for s in sentences if s.strip()) + '.'
            
            return {
                'summary': fallback_summary,
                'original_length': len(text.split()),
                'summary_length': len(fallback_summary.split()),
                'compression_ratio': round(len(fallback_summary.split()) / len(text.split()), 2)
            }


class AIAnalysisService:
    """
    AI Analysis Service using Azure OpenAI
    Integrates sentiment analysis and text summarization
    """
    
    def __init__(self):
        print("Initializing Azure OpenAI Analysis Service...")
        self.azure_ai = AzureOpenAIService()
        # Keep old references for compatibility
        self.sentiment_analyzer = self
        self.text_summarizer = self
        print("Azure OpenAI Analysis Service initialized successfully")
    
    def analyze_sentiment(self, text):
        """Analyze sentiment using Azure OpenAI"""
        return self.azure_ai.analyze_sentiment(text)
    
    def summarize_text(self, text, max_sentences=3, min_sentences=1):
        """Summarize text using Azure OpenAI"""
        return self.azure_ai.summarize_text(text, max_sentences, min_sentences)
    
    def analyze_content(self, text, title="", include_summary=True, include_sentiment=True):
        """
        Perform comprehensive analysis on text content using Azure OpenAI
        
        Args:
            text (str): Text to analyze
            title (str): Optional title for context
            include_summary (bool): Whether to include summarization
            include_sentiment (bool): Whether to include sentiment analysis
            
        Returns:
            dict: Complete analysis results
        """
        if not text:
            return {
                'error': 'No content provided',
                'sentiment': None,
                'summary': None
            }
        
        # Combine title and text for analysis
        full_text = f"{title}. {text}" if title else text
        
        results = {
            'original_text_length': len(text.split()),
            'analysis_timestamp': datetime.now().isoformat(),
        }
        
        if include_sentiment:
            print("Performing Azure OpenAI sentiment analysis...")
            results['sentiment'] = self.analyze_sentiment(full_text)
        
        if include_summary:
            print("Performing Azure OpenAI text summarization...")
            results['summary'] = self.summarize_text(text)
        
        # Calculate content metrics
        word_count = len(text.split()) if text else 0
        char_count = len(text) if text else 0
        
        results['metrics'] = {
            'word_count': word_count,
            'character_count': char_count,
            'estimated_reading_time': max(1, word_count // 200)  # Average reading speed
        }
        
        return results
    
    def batch_analyze(self, content_list):
        """Analyze multiple pieces of content using Azure OpenAI"""
        results = []
        
        for content in content_list:
            if isinstance(content, dict):
                title = content.get('title', '')
                text = content.get('text', '')
            else:
                title = ''
                text = str(content)
            
            analysis = self.analyze_content(text, title)
            analysis['original_content'] = {
                'title': title,
                'text': text[:200] + '...' if len(text) > 200 else text
            }
            results.append(analysis)
        
        return results
    
    def get_model_info(self):
        """Get information about the AI service"""
        return {
            'sentiment_model': 'Azure OpenAI GPT-4o-mini',
            'summarization_model': 'Azure OpenAI GPT-4o-mini',
            'type': 'Cloud-based Azure OpenAI',
            'endpoint': 'https://ai-raiyanbinsarwar0112ai312258162978.openai.azure.com',
            'status': 'Ready'
        }

# Singleton instance
ai_service = AIAnalysisService()
