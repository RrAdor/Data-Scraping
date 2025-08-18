import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

// Root App
class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'SentimentScope / News Summarizer Demo',
      theme: ThemeData(primarySwatch: Colors.indigo),
      home: HomePage(),
    );
  }
}

// Home Page with Hero & Navigation
class HomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("SentimentScope")),
      drawer: Drawer(
        child: ListView(
          children: [
            DrawerHeader(
              child: Text('SentimentScope', style: TextStyle(fontSize: 24)),
            ),
            ListTile(
              title: Text('Home'),
              onTap: () => Navigator.pop(context),
            ),
            ListTile(
              title: Text('About'),
              onTap: () => Navigator.push(
                  context, MaterialPageRoute(builder: (_) => AboutSection())),
            ),
            ListTile(
              title: Text('Team'),
              onTap: () => Navigator.push(
                  context, MaterialPageRoute(builder: (_) => TeamSection())),
            ),
            ListTile(
              title: Text('Login'),
              onTap: () => Navigator.push(
                  context, MaterialPageRoute(builder: (_) => LoginPage())),
            ),
            ListTile(
              title: Text('Sign Up'),
              onTap: () => Navigator.push(
                  context, MaterialPageRoute(builder: (_) => SignupPage())),
            ),
          ],
        ),
      ),
      body: SingleChildScrollView(
        child: Column(
          children: [
            // Hero Section
            Container(
              padding: EdgeInsets.all(20),
              color: Colors.indigo.shade100,
              child: Column(
                children: [
                  Text(
                    "Decipher News Sentiment with AI Precision",
                    style: TextStyle(
                        fontSize: 28,
                        fontWeight: FontWeight.bold,
                        color: Colors.indigo),
                    textAlign: TextAlign.center,
                  ),
                  SizedBox(height: 10),
                  Text(
                    "Our AI analyzes news articles and videos to provide accurate sentiment analysis and concise summaries.",
                    style: TextStyle(fontSize: 16),
                    textAlign: TextAlign.center,
                  ),
                  SizedBox(height: 20),
                  ElevatedButton(
                    onPressed: () {
                      Navigator.push(context,
                          MaterialPageRoute(builder: (_) => PortalPage()));
                    },
                    child: Text("Get Started for Free"),
                  ),
                ],
              ),
            ),
            // Footer Shortcut
            Container(
              color: Colors.indigo.shade200,
              padding: EdgeInsets.all(20),
              // child: Text(
              //   "Scroll drawer for About / Team / Login / Signup",
              //   style: TextStyle(color: Colors.white),
              // ),
            ),
          ],
        ),
      ),
    );
  }
}

// About Section Page
class AboutSection extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("About SentimentScope")),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text("About SentimentScope",
                style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
            SizedBox(height: 10),
            Text(
                "SentimentScope leverages AI to analyze news and videos, understanding the emotional tone beyond keywords."),
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
    );
  }
}

// Team Section Page
class TeamSection extends StatelessWidget {
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
      appBar: AppBar(title: Text("Team")),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(16),
        child: Wrap(
          spacing: 10,
          runSpacing: 10,
          children: teamMembers
              .map((member) =>
              MemberCard(name: member["name"]!, role: member["role"]!))
              .toList(),
        ),
      ),
    );
  }
}

// Feature Card Widget
class FeatureCard extends StatelessWidget {
  final IconData icon;
  final String title;
  final String description;

  FeatureCard(
      {required this.icon, required this.title, required this.description});

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

// Member Card Widget
class MemberCard extends StatelessWidget {
  final String name;
  final String role;

  MemberCard({required this.name, required this.role});

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

// Login Page
class LoginPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Login")),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(decoration: InputDecoration(labelText: "Email")),
            TextField(decoration: InputDecoration(labelText: "Password")),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                    context, MaterialPageRoute(builder: (_) => PortalPage()));
              },
              child: Text("Login"),
            ),
          ],
        ),
      ),
    );
  }
}

// Signup Page
class SignupPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Sign Up")),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(decoration: InputDecoration(labelText: "Name")),
            TextField(decoration: InputDecoration(labelText: "Email")),
            TextField(decoration: InputDecoration(labelText: "Password")),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                    context, MaterialPageRoute(builder: (_) => PortalPage()));
              },
              child: Text("Sign Up"),
            ),
          ],
        ),
      ),
    );
  }
}

// Portal Page (Mock News / Video Headlines)
class PortalPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    List<String> headlines = [
      "Japan's emperor expresses 'deep remorse' 80 years after WWII",
      "A path to trauma healing for Milestone survivors",
      "Putin-Trump summit: What each side wants",
    ];

    return Scaffold(
      appBar: AppBar(title: Text("Portal")),
      body: ListView.builder(
        itemCount: headlines.length,
        itemBuilder: (context, index) {
          return ListTile(
            title: Text(headlines[index]),
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => ArticlePage(headline: headlines[index]),
                ),
              );
            },
          );
        },
      ),
    );
  }
}

// Article Page + Analyze Button
class ArticlePage extends StatelessWidget {
  final String headline;
  ArticlePage({required this.headline});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(headline)),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              "Tens of thousands of people braved blazing heat to pay their respects at a controversial Japanese shrine on Friday, as Emperor Naruhito spoke of his deep remorse on the 80th anniversary of the nation's World War II surrender. '$headline'.",
              style: TextStyle(fontSize: 16),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                showDialog(
                  context: context,
                  builder: (context) => AlertDialog(
                    title: Text("Analysis"),
                    content: Text(
                        "Summary: Reflecting on our past and bearing in mind the feelings of deep remorse, I earnestly hope that the ravages of war will never again be repeated..\nSentiment: Positive"),
                    actions: [
                      TextButton(
                        onPressed: () => Navigator.pop(context),
                        child: Text("Close"),
                      ),
                    ],
                  ),
                );
              },
              child: Text("Analyze"),
            ),
          ],
        ),
      ),
    );
  }
}
