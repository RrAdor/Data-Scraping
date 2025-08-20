import 'package:flutter/material.dart';
import '../utils/constants.dart';

class ArticleScreen extends StatelessWidget {
  final String headline;

  ArticleScreen({Key? key, required this.headline}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(headline),
        backgroundColor: AppColors.primary,
      ),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              "Tens of thousands of people braved blazing heat to pay their respects at a controversial Japanese shrine on Friday, as Emperor Naruhito spoke of his deep remorse on the 80th anniversary of the nation's World War II surrender. '$headline'.",
              style: TextStyle(fontSize: 16),
            ),
            SizedBox(height: 20),
            Center(
              child: ElevatedButton(
                onPressed: () {
                  showDialog(
                    context: context,
                    builder: (context) => AlertDialog(
                      title: Text("Analysis Results"),
                      content: Column(
                        mainAxisSize: MainAxisSize.min,
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text("Summary:", style: TextStyle(fontWeight: FontWeight.bold)),
                          Text("Reflecting on our past and bearing in mind the feelings of deep remorse, I earnestly hope that the ravages of war will never again be repeated."),
                          SizedBox(height: 10),
                          Text("Sentiment: Positive", style: TextStyle(fontWeight: FontWeight.bold)),
                          SizedBox(height: 10),
                          Text("Confidence: 92%", style: TextStyle(fontSize: 12)),
                        ],
                      ),
                      actions: [
                        TextButton(
                          onPressed: () => Navigator.pop(context),
                          child: Text("Close"),
                        ),
                      ],
                    ),
                  );
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.primary,
                  foregroundColor: Colors.white,
                  padding: EdgeInsets.symmetric(horizontal: 30, vertical: 15),
                ),
                child: Text("Analyze Article"),
              ),
            ),
          ],
        ),
      ),
    );
  }
}