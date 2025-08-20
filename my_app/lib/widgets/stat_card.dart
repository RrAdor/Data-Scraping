import 'package:flutter/material.dart';
import '../utils/constants.dart';

class StatCard extends StatelessWidget {
  final String number;
  final String label;

  const StatCard({
    Key? key,
    required this.number,
    required this.label,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 100,
      padding: EdgeInsets.all(10),
      child: Column(
        children: [
          Text(number,
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: AppColors.primary)),
          SizedBox(height: 5),
          Text(label,
              style: TextStyle(fontSize: 12),
              textAlign: TextAlign.center),
        ],
      ),
    );
  }
}