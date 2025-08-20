import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:sentimentscope/main.dart';

void main() {
  testWidgets('App starts with home screen', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(MyApp());

    // Verify that our app starts with the home screen
    expect(find.text('SentimentScope'), findsOneWidget);
    expect(find.text('Decipher News Sentiment with AI Precision'), findsOneWidget);
  });

  testWidgets('Navigation drawer works', (WidgetTester tester) async {
    await tester.pumpWidget(MyApp());

    // Open the drawer
    await tester.tap(find.byIcon(Icons.menu));
    await tester.pumpAndSettle();

    // Verify drawer items are present
    expect(find.text('Home'), findsOneWidget);
    expect(find.text('About'), findsOneWidget);
    expect(find.text('Team'), findsOneWidget);
    expect(find.text('Contact'), findsOneWidget);
    expect(find.text('Login'), findsOneWidget);
    expect(find.text('Sign Up'), findsOneWidget);
  });

  testWidgets('Navigation to about screen works', (WidgetTester tester) async {
    await tester.pumpWidget(MyApp());

    // Open the drawer
    await tester.tap(find.byIcon(Icons.menu));
    await tester.pumpAndSettle();

    // Tap on About
    await tester.tap(find.text('About'));
    await tester.pumpAndSettle();

    // Verify we're on the about screen
    expect(find.text('About SentimentScope'), findsOneWidget);
  });
}