class AnalysisResult {
  final String summary;
  final String sentiment;
  final double positiveScore;
  final double neutralScore;
  final double negativeScore;
  final List<String> keywords;
  final List<String> insights;

  AnalysisResult({
    required this.summary,
    required this.sentiment,
    required this.positiveScore,
    required this.neutralScore,
    required this.negativeScore,
    required this.keywords,
    required this.insights,
  });

  factory AnalysisResult.fromJson(Map<String, dynamic> json) {
    return AnalysisResult(
      summary: json['summary'],
      sentiment: json['sentiment'],
      positiveScore: json['positive_score']?.toDouble() ?? 0.0,
      neutralScore: json['neutral_score']?.toDouble() ?? 0.0,
      negativeScore: json['negative_score']?.toDouble() ?? 0.0,
      keywords: List<String>.from(json['keywords'] ?? []),
      insights: List<String>.from(json['insights'] ?? []),
    );
  }
}