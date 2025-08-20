import 'package:flutter/material.dart';
import '../widgets/contact_info.dart';
import '../utils/constants.dart';

class ContactScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Contact Us"),
        backgroundColor: AppColors.primary,
      ),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text("Contact Us",
                style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
            SizedBox(height: 20),
            ContactInfo(icon: Icons.location_on, text: "Dhaka, Bangladesh"),
            ContactInfo(icon: Icons.phone, text: "+91 9876543210"),
            ContactInfo(icon: Icons.email, text: "contact@sentimentscope.com"),
            SizedBox(height: 30),
            Text("Send us a message",
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            SizedBox(height: 10),
            TextField(decoration: InputDecoration(labelText: "Your Name")),
            TextField(decoration: InputDecoration(labelText: "Your Email")),
            TextField(
              decoration: InputDecoration(labelText: "Message"),
              maxLines: 5,
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {},
              style: ElevatedButton.styleFrom(
                backgroundColor: AppColors.primary,
                foregroundColor: Colors.white,
              ),
              child: Text("Send Message"),
            ),
          ],
        ),
      ),
    );
  }
}