import 'package:flutter/material.dart';
import '../utils/constants.dart';

class TeamMemberCard extends StatelessWidget {
  final String name;
  final String role;

  const TeamMemberCard({
    Key? key,
    required this.name,
    required this.role,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 3,
      child: Padding(
        padding: EdgeInsets.all(8),
        child: Column(
          children: [
            CircleAvatar(
              radius: 40,
              backgroundColor: AppColors.primary,
              child: Icon(Icons.person, size: 40, color: Colors.white),
            ),
            SizedBox(height: 16),
            Text(name,
                style: TextStyle(fontWeight: FontWeight.bold),
                textAlign: TextAlign.center),
            SizedBox(height: 8),
            Text(role,
                style: TextStyle(fontSize: 12, color: Colors.indigoAccent,fontWeight: FontWeight.bold),
                textAlign: TextAlign.center),
            SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                IconButton(
                  icon: Icon(Icons.link, size: 16),
                  onPressed: () {},
                ),
                IconButton(
                  icon: Icon(Icons.chat, size: 16),
                  onPressed: () {},
                ),
                IconButton(
                  icon: Icon(Icons.code, size: 16),
                  onPressed: () {},
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}