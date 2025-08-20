import 'dart:math';
import 'package:flutter/material.dart';

class SentimentChart extends StatelessWidget {
  final double positive;
  final double neutral;
  final double negative;

  const SentimentChart({
    Key? key,
    this.positive = 72,
    this.neutral = 18,
    this.negative = 10,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 200,
      child: CustomPaint(
        painter: PieChartPainter(
          positive: positive,
          neutral: neutral,
          negative: negative,
        ),
      ),
    );
  }
}

class PieChartPainter extends CustomPainter {
  final double positive;
  final double neutral;
  final double negative;

  PieChartPainter({
    required this.positive,
    required this.neutral,
    required this.negative,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final radius = size.width / 2.5;

    final total = positive + neutral + negative;
    final positiveAngle = (positive / total) * 2 * 3.14159;
    final neutralAngle = (neutral / total) * 2 * 3.14159;
    final negativeAngle = (negative / total) * 2 * 3.14159;

    // Draw positive segment
    final positivePaint = Paint()
      ..color = Color(0xFF4CAF50)
      ..style = PaintingStyle.fill;
    canvas.drawArc(
      Rect.fromCircle(center: center, radius: radius),
      0,
      positiveAngle,
      true,
      positivePaint,
    );

    // Draw neutral segment
    final neutralPaint = Paint()
      ..color = Color(0xFF9E9E9E)
      ..style = PaintingStyle.fill;
    canvas.drawArc(
      Rect.fromCircle(center: center, radius: radius),
      positiveAngle,
      neutralAngle,
      true,
      neutralPaint,
    );

    // Draw negative segment
    final negativePaint = Paint()
      ..color = Color(0xFFF44336)
      ..style = PaintingStyle.fill;
    canvas.drawArc(
      Rect.fromCircle(center: center, radius: radius),
      positiveAngle + neutralAngle,
      negativeAngle,
      true,
      negativePaint,
    );

    // Draw center circle
    final centerPaint = Paint()
      ..color = Colors.white
      ..style = PaintingStyle.fill;
    canvas.drawCircle(center, radius / 2, centerPaint);

    // Draw labels
    _drawLabel(canvas, center, radius, 'Positive', positiveAngle / 2, Color(0xFF4CAF50));
    _drawLabel(canvas, center, radius, 'Neutral', positiveAngle + neutralAngle / 2, Color(0xFF9E9E9E));
    _drawLabel(canvas, center, radius, 'Negative', positiveAngle + neutralAngle + negativeAngle / 2, Color(0xFFF44336));
  }

  void _drawLabel(Canvas canvas, Offset center, double radius, String text, double angle, Color color) {
    final textPainter = TextPainter(
      text: TextSpan(
        text: text,
        style: TextStyle(color: color, fontSize: 10, fontWeight: FontWeight.bold),
      ),
      textDirection: TextDirection.ltr,
    )..layout();

    final dx = center.dx + (radius * 0.7) * cos(angle);
    final dy = center.dy + (radius * 0.7) * sin(angle);
    final offset = Offset(dx - textPainter.width / 2, dy - textPainter.height / 2);

    textPainter.paint(canvas, offset);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) {
    return false;
  }
}