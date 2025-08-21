import 'package:flutter/material.dart';
import '../widgets/feature_card.dart';
import '../widgets/member_card.dart';
import '../widgets/stat_card.dart';
import '../widgets/footer_section.dart';
import '../utils/constants.dart';
import 'about_screen.dart';
import 'team_screen.dart';
import 'login_screen.dart';
import 'signup_screen.dart';
import 'portal_screen.dart';
import 'contact_screen.dart';
import 'url_analysis_screen.dart';
import 'profile_screen.dart';

class HomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Row(
          children: [
            Icon(Icons.analytics, color: Colors.white),
            SizedBox(width: 8),
            Text(AppStrings.appName, style: TextStyle(color: Colors.white)),
          ],
        ),
        backgroundColor: AppColors.primary,
        elevation: 0,
        actions: [
          // Add user icon that navigates to profile
          IconButton(
            icon: Icon(Icons.person, color: Colors.white),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => ProfileScreen()),
              );
            },
          ),
        ],
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
            ListTile(
              leading: Icon(Icons.person),
              title: Text('Profile'),
              onTap: () => Navigator.push(
                  context, MaterialPageRoute(builder: (_) => ProfileScreen())),
            ),
            // // Add this to your drawer ListView children
            // ListTile(
            //   leading: Icon(Icons.link),
            //   title: Text('URL Analysis'),
            //   onTap: () => Navigator.push(
            //       context, MaterialPageRoute(builder: (_) => UrlAnalysisScreen())),
            // ),
          ],
        ),
      ),
      body: LayoutBuilder(
        builder: (context, constraints) {
          final bool isLargeScreen = constraints.maxWidth > 600;

          return SingleChildScrollView(
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
                            fontSize: isLargeScreen ? 32 : 24,
                            fontWeight: FontWeight.bold,
                            color: Colors.white),
                        textAlign: TextAlign.center,
                      ),
                      SizedBox(height: 20),
                      Text(
                        AppStrings.description,
                        style: TextStyle(
                            fontSize: isLargeScreen ? 18 : 14,
                            color: Colors.white70),
                        textAlign: TextAlign.center,
                      ),
                      SizedBox(height: 20),
                      // Replace the existing ElevatedButton in the Hero section
                      ElevatedButton(
                        onPressed: () {
                          Navigator.push(context,
                              MaterialPageRoute(builder: (_) => UrlAnalysisScreen())); // Changed to UrlAnalysisScreen
                        },
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.white,
                          foregroundColor: AppColors.primary,
                        ),
                        child: Text("Get Started for Free"),
                      ),
                      SizedBox(height: 20),
                      // Floating elements
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
                          style: TextStyle(
                              fontSize: isLargeScreen ? 28 : 22,
                              fontWeight: FontWeight.bold)),
                      SizedBox(height: 10),
                      Text(
                          "SentimentScope is an innovative platform that leverages cutting-edge artificial intelligence to analyze news articles and video content.",
                          style: TextStyle(fontSize: isLargeScreen ? 16 : 14)),
                      SizedBox(height: 20),
                      // FIXED: Use Wrap instead of Row for responsive layout
                      Wrap(
                        alignment: WrapAlignment.spaceEvenly,
                        spacing: 16,
                        runSpacing: 16,
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
                              description: "Identify potential biases in reporting and journalism."),
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
                          style: TextStyle(
                              fontSize: isLargeScreen ? 28 : 22,
                              fontWeight: FontWeight.bold)),
                      SizedBox(height: 10),
                      Text("Quantifying our success and reliability",
                          style: TextStyle(fontSize: isLargeScreen ? 16 : 14)),
                      SizedBox(height: 20),
                      // FIXED: Use Wrap instead of Row for responsive layout
                      Wrap(
                        alignment: WrapAlignment.spaceEvenly,
                        spacing: 16,
                        runSpacing: 16,
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
                          style: TextStyle(
                              fontSize: isLargeScreen ? 28 : 22,
                              fontWeight: FontWeight.bold)),
                      SizedBox(height: 10),
                      Text("The brilliant minds behind SentimentScope's innovative technology",
                          style: TextStyle(fontSize: isLargeScreen ? 16 : 14)),
                      SizedBox(height: 20),
                      // FIXED: Use Wrap instead of Row for responsive layout
                      Wrap(
                        alignment: WrapAlignment.spaceEvenly,
                        spacing: 16,
                        runSpacing: 16,
                        children: [
                          MemberCard(name: "Israt Tabassum Kochy", role: "Data Analyst"),
                          MemberCard(name: "Ariyana Rubaiaya Chowdhury", role: "AI Specialist"),
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
                          child: Text("View Full Team →",
                              style: TextStyle(
                                  color: AppColors.primary,
                                  fontWeight: FontWeight.bold)),
                        ),
                      ),
                    ],
                  ),
                ),

                // Footer
                Container(
                  padding: EdgeInsets.all(10),
                  color: AppColors.primary,
                  child: Column(
                    children: [
                      // FIXED: Use Wrap instead of Row for responsive layout
                      Wrap(
                        alignment: WrapAlignment.spaceEvenly,
                        spacing: 20,
                        runSpacing: 20,
                        children: [
                          FooterSection(
                            title: "SentimentScop",
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
          );
        },
      ),
    );
  }
}

class FloatingElement extends StatefulWidget {
  final IconData icon;
  final int delay;

  const FloatingElement({Key? key, required this.icon, required this.delay}) : super(key: key);

  @override
  _FloatingElementState createState() => _FloatingElementState();
}

class _FloatingElementState extends State<FloatingElement>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: Duration(seconds: 3),
      vsync: this,
    )..repeat(reverse: true);

    _animation = Tween<double>(begin: -10, end: 10).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeInOut),
    );

    Future.delayed(Duration(seconds: widget.delay), () {
      if (mounted) _controller.forward();
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _animation,
      builder: (context, child) {
        return Transform.translate(
          offset: Offset(0, _animation.value),
          child: Container(
            width: 40,
            height: 40,
            child: Icon(widget.icon, color: Colors.white.withOpacity(0.3)),
          ),
        );
      },
    );
  }
}