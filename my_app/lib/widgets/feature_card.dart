import 'package:flutter/material.dart';

class FeatureCard extends StatelessWidget {
  final IconData icon;
  final String title;
  final String description;

  const FeatureCard({
    Key? key,
    required this.icon,
    required this.title,
    required this.description,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 110,
      padding: EdgeInsets.all(10),
      decoration: BoxDecoration(
        color: Colors.indigo.shade100,
        borderRadius: BorderRadius.circular(8),
      ),
      child: Column(
        children: [
          Icon(icon, size: 36, color: Colors.indigo),
          SizedBox(height: 8),
          Text(title,
              style: TextStyle(fontWeight: FontWeight.bold),
              textAlign: TextAlign.center),
          SizedBox(height: 4),
          Text(description, style: TextStyle(fontSize: 12), textAlign: TextAlign.center),
        ],
      ),
    );
  }
}