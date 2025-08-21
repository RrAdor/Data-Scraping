import 'package:flutter/material.dart';
import '../utils/constants.dart';
import '../services/auth_service.dart';
import '../models/user.dart';
import 'portal_screen.dart';

class UrlAnalysisScreen extends StatefulWidget {
  @override
  _UrlAnalysisScreenState createState() => _UrlAnalysisScreenState();
}

class _UrlAnalysisScreenState extends State<UrlAnalysisScreen> {
  final _formKey = GlobalKey<FormState>();
  final _urlController = TextEditingController();
  bool _isLoading = false;
  User? _currentUser;

  @override
  void initState() {
    super.initState();
    _loadUserData();
  }

  Future<void> _loadUserData() async {
    final user = await AuthService.getUser();
    setState(() {
      _currentUser = user;
    });
  }

  Future<void> _analyzeUrl() async {
    if (_formKey.currentState!.validate()) {
      setState(() {
        _isLoading = true;
      });

      try {
        // Simulate API call
        await Future.delayed(Duration(seconds: 2));

        // Navigate to PortalScreen after analysis
        Navigator.pushReplacement(
            context,
            MaterialPageRoute(builder: (_) => PortalScreen())
        );

      } catch (e) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Error analyzing URL'),
            backgroundColor: Colors.red,
          ),
        );
      } finally {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  void _useExample() {
    setState(() {
      _urlController.text = 'https://example.com/news/economic-policy-article';
    });
  }

  @override
  void dispose() {
    _urlController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Row(
          children: [
            Icon(Icons.analytics, color: Colors.white),
            SizedBox(width: 8),
            Text("URL Analysis", style: TextStyle(color: Colors.white)),
          ],
        ),
        backgroundColor: AppColors.primary,
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // User welcome section
            if (_currentUser != null)
              Padding(
                padding: EdgeInsets.only(bottom: 20),
                child: Text(
                  'Hello ${_currentUser!.name}!',
                  style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                ),
              ),

            // Analysis card
            Card(
              elevation: 4,
              child: Padding(
                padding: EdgeInsets.all(20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Analyze Article Sentiment',
                      style: TextStyle(
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                        color: AppColors.primary,
                      ),
                    ),
                    SizedBox(height: 20),

                    // URL input form
                    Form(
                      key: _formKey,
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Paste article URL to analyze:',
                            style: TextStyle(
                              fontWeight: FontWeight.bold,
                              fontSize: 16,
                            ),
                          ),
                          SizedBox(height: 10),
                          TextFormField(
                            controller: _urlController,
                            decoration: InputDecoration(
                              hintText: 'https://example.com/news/article',
                              border: OutlineInputBorder(),
                              prefixIcon: Icon(Icons.link),
                            ),
                            keyboardType: TextInputType.url,
                            validator: (value) {
                              if (value == null || value.isEmpty) {
                                return 'Please enter a URL';
                              }
                              if (!value.startsWith('http://') &&
                                  !value.startsWith('https://')) {
                                return 'Please enter a valid URL';
                              }
                              return null;
                            },
                          ),
                        ],
                      ),
                    ),
                    SizedBox(height: 20),

                    // Analyze button
                    SizedBox(
                      width: double.infinity,
                      child: ElevatedButton(
                        onPressed: _isLoading ? null : _analyzeUrl,
                        style: ElevatedButton.styleFrom(
                          backgroundColor: AppColors.primary,
                          foregroundColor: Colors.white,
                          padding: EdgeInsets.symmetric(vertical: 15),
                        ),
                        child: _isLoading
                            ? CircularProgressIndicator(color: Colors.white)
                            : Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(Icons.analytics),
                            SizedBox(width: 10),
                            Text('Analyze Now'),
                          ],
                        ),
                      ),
                    ),
                    SizedBox(height: 20),

                    // Example link
                    GestureDetector(
                      onTap: _useExample,
                      child: Text.rich(
                        TextSpan(
                          text: 'Try example: ',
                          children: [
                            TextSpan(
                              text: 'Economic policy article',
                              style: TextStyle(
                                color: AppColors.primary,
                                decoration: TextDecoration.underline,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                    SizedBox(height: 20),

                    // Features section
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      children: [
                        _buildFeature(
                          icon: Icons.flash_on,
                          text: 'Instant Analysis',
                        ),
                        _buildFeature(
                          icon: Icons.bar_chart,
                          text: 'Detailed Insights',
                        ),
                        _buildFeature(
                          icon: Icons.picture_as_pdf,
                          text: 'PDF Reports',
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
    );
  }

  Widget _buildFeature({required IconData icon, required String text}) {
    return Column(
      children: [
        Icon(icon, color: AppColors.primary, size: 24),
        SizedBox(height: 5),
        Text(
          text,
          style: TextStyle(fontSize: 12),
          textAlign: TextAlign.center,
        ),
      ],
    );
  }
}