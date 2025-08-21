import 'package:flutter/material.dart';
import '../widgets/feature_card.dart';
import '../widgets/sentiment_chart.dart';
import '../widgets/stat_item.dart';
import '../utils/constants.dart';

class AboutScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("About SentimentScope"),
        backgroundColor: AppColors.primary,
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text("About SentimentScope",
                style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
            SizedBox(height: 10),
            Text(
                "SentimentScope is an innovative platform that leverages cutting-edge artificial intelligence to analyze news articles and video content. Our technology goes beyond simple keyword analysis to understand the nuanced emotional tones in media content."),
            SizedBox(height: 10),
            Text(
                "By providing accurate sentiment scores and concise summaries, we help businesses, researchers, and curious individuals cut through the noise and understand the true sentiment behind news stories."),
            SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                FeatureCard(
                    icon: Icons.memory,
                    title: "Advanced AI",
                    description: "Continuous learning for accurate sentiment analysis."),
                FeatureCard(
                    icon: Icons.access_time,
                    title: "Real-time Analysis",
                    description: "Process thousands of news sources instantly."),
                FeatureCard(
                    icon: Icons.shield,
                    title: "Bias Detection",
                    description: "Identify potential biases in reporting and journalism."),
              ],
            ),
            SizedBox(height: 20),
            // Sentiment Distribution Chart
            // Container(
            //   padding: EdgeInsets.all(16),
            //   decoration: BoxDecoration(
            //     border: Border.all(color: Colors.grey[300]!),
            //     borderRadius: BorderRadius.circular(8),
            //   ),
            //   child: Column(
            //     crossAxisAlignment: CrossAxisAlignment.start,
            //     children: [
            //       Text("Sentiment Distribution",
            //           style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
            //       Text("Analysis of 10,000 recent news articles"),
            //       SizedBox(height: 10),
            //       Container(
            //         height: 200,
            //         child: SentimentChart(),
            //       ),
            //       SizedBox(height: 10),
            //       Row(
            //         mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            //         children: [
            //           StatItem(number: "72%", label: "Positive"),
            //           StatItem(number: "18%", label: "Neutral"),
            //           StatItem(number: "10%", label: "Negative"),
            //         ],
            //       ),
            //     ],
            //   ),
            // ),
          ],
        ),
      ),
    );
  }
}