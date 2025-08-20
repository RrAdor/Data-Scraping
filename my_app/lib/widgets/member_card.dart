import 'package:flutter/material.dart';

class MemberCard extends StatelessWidget {
  final String name;
  final String role;

  const MemberCard({
    Key? key,
    required this.name,
    required this.role,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 150,
      padding: EdgeInsets.all(10),
      decoration: BoxDecoration(
        color: Colors.indigo.shade100,
        borderRadius: BorderRadius.circular(8),
      ),
      child: Column(
        children: [
          CircleAvatar(radius: 30, child: Icon(Icons.person)),
          SizedBox(height: 8),
          Text(name,
              style: TextStyle(fontWeight: FontWeight.bold),
              textAlign: TextAlign.center),
          SizedBox(height: 4),
          Text(role, style: TextStyle(fontSize: 12), textAlign: TextAlign.center),
        ],
      ),
    );
  }
}