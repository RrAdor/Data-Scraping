import 'package:flutter/material.dart';
import '../utils/constants.dart';
import '../services/auth_service.dart';
import '../models/user.dart';

class ProfileScreen extends StatefulWidget {
  @override
  _ProfileScreenState createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  User? _currentUser;
  List<Map<String, dynamic>> _analysisHistory = [];

  @override
  void initState() {
    super.initState();
    _loadUserData();
    _loadAnalysisHistory();
  }

  Future<void> _loadUserData() async {
    final user = await AuthService.getUser();
    setState(() {
      _currentUser = user;
    });
  }

  void _loadAnalysisHistory() {
    // Mock analysis history data
    setState(() {
      _analysisHistory = [
        {
          'title': "Japan's emperor expresses 'deep remorse'",
          'date': '2023-11-15',
          'sentiment': 'Positive',
          'summary': 'Reflecting on our past and bearing in mind the feelings of deep remorse...',
        },
        {
          'title': "Economic policy changes",
          'date': '2023-11-10',
          'sentiment': 'Neutral',
          'summary': 'The government announced new economic policies aimed at...',
        },
        {
          'title': "Climate change summit results",
          'date': '2023-11-05',
          'sentiment': 'Negative',
          'summary': 'World leaders failed to reach agreement on key climate change issues...',
        },
      ];
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Profile'),
        backgroundColor: AppColors.primary,
      ),
      body: _currentUser == null
          ? Center(child: CircularProgressIndicator())
          : SingleChildScrollView(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // User info section
            Card(
              child: Padding(
                padding: EdgeInsets.all(16),
                child: Column(
                  children: [
                    Container(
                      child: Center(
                        child: Column(
                          children: [
                            CircleAvatar(
                              radius: 40,
                              backgroundColor: AppColors.primary,
                              child: Icon(
                                Icons.person,
                                size: 40,
                                color: Colors.white,
                              ),
                            ),
                            SizedBox(height: 16),
                            Text(
                              _currentUser!.name,
                              style: TextStyle(
                                fontSize: 24,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            SizedBox(height: 8),
                            Text(
                              _currentUser!.email,
                              style: TextStyle(
                                fontSize: 16,
                                color: Colors.grey[600],
                              ),
                            ),
                            SizedBox(height: 16),
                            Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Icon(Icons.verified_user, color: Colors.green),
                                SizedBox(width: 8),
                                Text(
                                  'Logged In',
                                  style: TextStyle(
                                    color: Colors.green,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
            SizedBox(height: 20),

            // Analysis history section
            Text(
              'Analysis History',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
            SizedBox(height: 10),
            _analysisHistory.isEmpty
                ? Center(
              child: Text(
                'No analysis history yet',
                style: TextStyle(color: Colors.grey),
              ),
            )
                : ListView.builder(
              shrinkWrap: true,
              physics: NeverScrollableScrollPhysics(),
              itemCount: _analysisHistory.length,
              itemBuilder: (context, index) {
                final analysis = _analysisHistory[index];
                return Card(
                  margin: EdgeInsets.symmetric(vertical: 8),
                  child: ListTile(
                    title: Text(analysis['title']),
                    subtitle: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(analysis['date']),
                        SizedBox(height: 4),
                        Row(
                          children: [
                            Icon(
                              Icons.sentiment_satisfied,
                              color: _getSentimentColor(analysis['sentiment']),
                              size: 16,
                            ),
                            SizedBox(width: 4),
                            Text(
                              analysis['sentiment'],
                              style: TextStyle(
                                color: _getSentimentColor(analysis['sentiment']),
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                    trailing: Icon(Icons.arrow_forward_ios, size: 16),
                    onTap: () {
                      _showAnalysisDetails(analysis, context);
                    },
                  ),
                );
              },
            ),
          ],
        ),
      ),
    );
  }

  Color _getSentimentColor(String sentiment) {
    switch (sentiment.toLowerCase()) {
      case 'positive':
        return Colors.green;
      case 'negative':
        return Colors.red;
      default:
        return Colors.orange;
    }
  }

  void _showAnalysisDetails(Map<String, dynamic> analysis, BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Analysis Details'),
        content: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(
                analysis['title'],
                style: TextStyle(fontWeight: FontWeight.bold),
              ),
              SizedBox(height: 10),
              Text('Date: ${analysis['date']}'),
              SizedBox(height: 10),
              Row(
                children: [
                  Icon(
                    Icons.sentiment_satisfied,
                    color: _getSentimentColor(analysis['sentiment']),
                  ),
                  SizedBox(width: 5),
                  Text(
                    'Sentiment: ${analysis['sentiment']}',
                    style: TextStyle(
                      color: _getSentimentColor(analysis['sentiment']),
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ],
              ),
              SizedBox(height: 10),
              Text(
                'Summary:',
                style: TextStyle(fontWeight: FontWeight.bold),
              ),
              SizedBox(height: 5),
              Text(analysis['summary']),
            ],
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text('Close'),
          ),
        ],
      ),
    );
  }
}