import 'package:flutter/material.dart';
import '../utils/constants.dart';
import 'article_screen.dart';

class PortalScreen extends StatelessWidget {
  final List<String> headlines = [
    "Japan's emperor expresses 'deep remorse' 80 years after WWII",
    "A path to trauma healing for Milestone survivors",
    "Putin-Trump summit: What each side wants",
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: ListView.builder(
        itemCount: headlines.length,
        itemBuilder: (context, index) {
          return Card(
            margin: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            child: ListTile(
              title: Text(headlines[index]),
              trailing: Icon(Icons.arrow_forward_ios, size: 16),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => ArticleScreen(headline: headlines[index]),
                  ),
                );
              },
            ),
          );
        },
      ),
      appBar: AppBar(
        title: Text("Portal"),
        backgroundColor: AppColors.primary,
      ),
    );
  }
}