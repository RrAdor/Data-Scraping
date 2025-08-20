import 'package:flutter/material.dart';
import '../widgets/team_member_card.dart';
import '../utils/constants.dart';

class TeamScreen extends StatelessWidget {
  final List<Map<String, String>> teamMembers = [
    {"name": "Israt Tabassum Kochy", "role": "Data Analyst"},
    {"name": "Ariyana Rubaiaya", "role": "AI Specialist"},
    {"name": "Faizah Mehnaz", "role": "Frontend Developer"},
    {"name": "Rifah Zakiah", "role": "Backend Developer"},
    {"name": "Raiyan Sarwar", "role": "Lead Developer"},
    {"name": "Rajaya Rabby Ador", "role": "Project Leader"},
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Team"),
        backgroundColor: AppColors.primary,
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text("Our Expert Team",
                style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
            SizedBox(height: 10),
            Text("The brilliant minds behind SentimentScope's innovative technology"),
            SizedBox(height: 20),
            GridView.builder(
              shrinkWrap: true,
              physics: NeverScrollableScrollPhysics(),
              gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 2,
                crossAxisSpacing: 10,
                mainAxisSpacing: 10,
                childAspectRatio: 0.8,
              ),
              itemCount: teamMembers.length,
              itemBuilder: (context, index) => TeamMemberCard(
                name: teamMembers[index]["name"]!,
                role: teamMembers[index]["role"]!,
              ),
            ),
          ],
        ),
      ),
    );
  }
}