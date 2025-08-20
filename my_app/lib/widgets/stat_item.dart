import 'package:flutter/material.dart';

class StatItem extends StatelessWidget {
  final String number;
  final String label;

  const StatItem({
    Key? key,
    required this.number,
    required this.label,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text(number,
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        Text(label,
            style: TextStyle(fontSize: 12)),
      ],
    );
  }
}