import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/user.dart';
import '../models/article.dart';
import '../models/analysis_result.dart';
import '../utils/constants.dart';

class ApiService {
  final String baseUrl;
  final http.Client client;

  ApiService({required this.baseUrl, required this.client});

  Future<User> login(String email, String password) async {
    final response = await client.post(
      Uri.parse('$baseUrl/login'),
      body: json.encode({'email': email, 'password': password}),
      headers: {'Content-Type': 'application/json'},
    );

    if (response.statusCode == 200) {
      return User.fromJson(json.decode(response.body));
    } else {
      throw Exception('Failed to login');
    }
  }

  Future<User> signup(String name, String email, String password) async {
    final response = await client.post(
      Uri.parse('$baseUrl/signup'),
      body: json.encode({'name': name, 'email': email, 'password': password}),
      headers: {'Content-Type': 'application/json'},
    );

    if (response.statusCode == 200) {
      return User.fromJson(json.decode(response.body));
    } else {
      throw Exception('Failed to sign up');
    }
  }

  Future<AnalysisResult> analyzeContent(String content) async {
    final response = await client.post(
      Uri.parse('$baseUrl/analyze'),
      body: json.encode({'content': content}),
      headers: {'Content-Type': 'application/json'},
    );

    if (response.statusCode == 200) {
      return AnalysisResult.fromJson(json.decode(response.body));
    } else {
      throw Exception('Failed to analyze content');
    }
  }
}