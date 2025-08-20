import 'package:flutter/material.dart';
import '../widgets/feature_card.dart';
import '../widgets/member_card.dart';
import '../widgets/stat_card.dart';
import '../widgets/footer_section.dart';
import '../widgets/sentiment_chart.dart';
import '../utils/constants.dart';
import 'about_screen.dart';
import 'team_screen.dart';
import 'login_screen.dart';
import 'signup_screen.dart';
import 'portal_screen.dart';
import 'contact_screen.dart';

class HomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Row(
            children: [
            Icon(Icons.analytics, color: Colors.white),
            SizedBox(width: 8),
            Text(AppStrings.appName, style: TextStyle(color: Colors.white)),
          ],
        ),
        backgroundColor: AppColors.primary,
        elevation: 0,
      ),
      drawer: Drawer(
        child: ListView(
          children: [
            const DrawerHeader(
              decoration: BoxDecoration(
                color: AppColors.primary,
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Icon(Icons.analytics, size: 40, color: Colors.white),
                  SizedBox(height: 10),
                  Text(AppStrings.appName,
                      style: TextStyle(fontSize: 24, color: Colors.white)),
                ],
              ),
            ),
            ListTile(
              leading: const Icon(Icons.home),
              title: const Text('Home'),
              onTap: () => Navigator.pop(context),
            ),
            ListTile(
              leading: Icon(Icons.info),
              title: Text('About'),
              onTap: () => Navigator.push(
                  context, MaterialPageRoute(builder: (_) => AboutScreen())),
            ),
            ListTile(
              leading: Icon(Icons.people),
              title: Text('Team'),
              onTap: () => Navigator.push(
                  context, MaterialPageRoute(builder: (_) => TeamScreen())),
            ),
            ListTile(
              leading: Icon(Icons.contact_page),
              title: Text('Contact'),
              onTap: () => Navigator.push(
                  context, MaterialPageRoute(builder: (_) => ContactScreen())),
            ),
            Divider(),
            ListTile(
              leading: Icon(Icons.login),
              title: Text('Login'),
              onTap: () => Navigator.push(
                  context, MaterialPageRoute(builder: (_) => LoginScreen())),
            ),
            ListTile(
              leading: Icon(Icons.person_add),
              title: Text('Sign Up'),
              onTap: () => Navigator.push(
                  context, MaterialPageRoute(builder: (_) => SignupScreen())),
            ),
          ],
        ),
      ),
      body: SingleChildScrollView(
        child: Column(
          children: [
            // Enhanced Hero Section
            Container(
              padding: EdgeInsets.all(20),
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  colors: [
                    AppColors.primary,
                    AppColors.secondary,
                  ],
                ),
              ),
              child: Column(
                children: [
                  Text(
                    AppStrings.slogan,
                    style: TextStyle(
                        fontSize: 28,
                        fontWeight: FontWeight.bold,
                        color: Colors.white),
                    textAlign: TextAlign.center,
                  ),
                  SizedBox(height:20),
                  Text(
                    AppStrings.description,
                    style: TextStyle(fontSize: 16, color: Colors.white70),
                    textAlign: TextAlign.center,
                  ),
                  SizedBox(height: 20),
                  ElevatedButton(
                    onPressed: () {
                      Navigator.push(context,
                          MaterialPageRoute(builder: (_) => PortalScreen()));
                    },
                    style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.white,
                        foregroundColor: AppColors.primary),
                    child: Text("Get Started for Free"),
                  ),
                  SizedBox(height: 20),
                  // Floating elements (simplified)
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    children: [
                      FloatingElement(icon: Icons.circle, delay: 0),
                      FloatingElement(icon: Icons.square, delay: 2),
                      FloatingElement(icon: Icons.change_history, delay: 4),
                    ],
                  ),
                ],
              ),
            ),

            // About Section
            Container(
              padding: EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text("About SentimentScope",
                      style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
                  SizedBox(height: 10),
                  Text(
                      "SentimentScope is an innovative platform that leverages cutting-edge artificial intelligence to analyze news articles and video content."),
                  SizedBox(height: 20),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      FeatureCard(
                          icon: Icons.memory,
                          title: "Advanced AI",
                          description: "Continuous learning for accurate sentiment analysis."),
                      FeatureCard(
                          icon: Icons.access_time,
                          title: "Real-time Analysis",
                          description: "Process thousands of news sources instantly."),
                      FeatureCard(
                          icon: Icons.shield,
                          title: "Bias Detection",
                          description: "Identify potential biases in reporting."),
                    ],
                  ),
                ],
              ),
            ),

            // Stats Section
            Container(
              padding: EdgeInsets.all(20),
              color: Colors.grey[100],
              child: Column(
                children: [
                  Text("Our Impact in Numbers",
                      style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
                  SizedBox(height: 10),
                  Text("Quantifying our success and reliability"),
                  SizedBox(height: 20),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      StatCard(number: "5K+", label: "Articles Analyzed"),
                      StatCard(number: "99.9%", label: "System Uptime"),
                      StatCard(number: "98%", label: "Accuracy Rate"),
                    ],
                  ),
                ],
              ),
            ),

            // Team Section Preview
            Container(
              padding: EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text("Our Expert Team",
                      style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
                  SizedBox(height: 10),
                  Text("The brilliant minds behind SentimentScope's innovative technology"),
                  SizedBox(height: 20),
                  // Show only 3 team members in preview
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      MemberCard(name: "Israt Tabassum Kochy", role: "Data Analyst"),
                      MemberCard(name: "Ariyana Rubaiaya", role: "AI Specialist"),
                      MemberCard(name: "Faizah Mehnaz", role: "Frontend Developer"),
                    ],
                  ),
                  SizedBox(height: 20),
                  Center(
                    child: TextButton(
                      onPressed: () {
                        Navigator.push(context,
                            MaterialPageRoute(builder: (_) => TeamScreen()));
                      },
                      child: Text("View Full Team →"),
                    ),
                  ),
                ],
              ),
            ),

            // Footer
            Container(
              padding: EdgeInsets.all(20),
              color: AppColors.primary,
              child: Column(
                children: [
                  Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      FooterSection(
                        title: AppStrings.appName,
                        content: "Harnessing the power of AI to analyze news sentiment and provide actionable insights.",
                      ),
                      FooterSection(
                        title: "Quick Links",
                        links: ["Home", "About", "Team", "How It Works", "Contact"],
                      ),
                      FooterSection(
                        title: "Resources",
                        links: ["Blog", "Documentation", "API Reference", "Case Studies", "Help Center"],
                      ),
                      FooterSection(
                        title: "Contact Us",
                        content: "Dhaka, Bangladesh\n+91 9876543210\ncontact@sentimentscope.com",
                      ),
                    ],
                  ),
                  Divider(color: Colors.white54),
                  Text(
                    "© 2025 SentimentScope. All rights reserved.",
                    style: TextStyle(color: Colors.white70, fontSize: 12),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class FloatingElement extends StatelessWidget {
  final IconData icon;
  final int delay;

  const FloatingElement({Key? key, required this.icon, required this.delay}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 40,
      height: 40,
      child: Icon(icon, color: Colors.white.withOpacity(0.3)),
    );
  }
}