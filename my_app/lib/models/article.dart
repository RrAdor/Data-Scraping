class Article {
  final String id;
  final String headline;
  final String content;
  final String sourceUrl;
  final String contentType;
  final DateTime scrapedAt;

  Article({
    required this.id,
    required this.headline,
    required this.content,
    required this.sourceUrl,
    required this.contentType,
    required this.scrapedAt,
  });

  factory Article.fromJson(Map<String, dynamic> json) {
    return Article(
      id: json['id'],
      headline: json['headline'],
      content: json['content'],
      sourceUrl: json['source_url'],
      contentType: json['content_type'],
      scrapedAt: DateTime.parse(json['scraped_at']),
    );
  }
}