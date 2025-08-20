import 'package:flutter/material.dart';
class AppColors {
  static const primary = Color(0xFF4361EE);
  static const secondary = Color(0xFF3A56E6);
  static const background = Color(0xFFF8F9FA);
  static const text = Color(0xFF212529);
  static const textLight = Color(0xFF6C757D);
}

class AppStrings {
  static const appName = 'SentimentScope';
  static const slogan = 'Decipher News Sentiment with AI Precision';
  static const description = 'Our AI analyzes news articles and videos to provide accurate sentiment analysis and concise summaries.';
}

class ApiEndpoints {
  static const baseUrl = 'https://your-api-url.com';
  static const login = '$baseUrl/login';
  static const signup = '$baseUrl/signup';
  static const analyze = '$baseUrl/analyze';
}