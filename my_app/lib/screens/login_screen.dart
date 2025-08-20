import 'package:flutter/material.dart';
import '../utils/constants.dart';
import 'portal_screen.dart';
import 'signup_screen.dart'; // Add this import

class LoginScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Login"),
        backgroundColor: AppColors.primary,
      ),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          children: [
            TextField( // Fixed: Added closing parenthesis for this TextField
              decoration: InputDecoration(
                labelText: "Email",
                prefixIcon: Icon(Icons.email),
              ), // Added this closing parenthesis
            ), // Added this closing parenthesis
            TextField(
              decoration: InputDecoration(
                labelText: "Password",
                prefixIcon: Icon(Icons.lock),
              ),
              obscureText: true,
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => PortalScreen()),
                );
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: AppColors.primary,
                foregroundColor: Colors.white,
                minimumSize: Size(double.infinity, 50),
              ),
              child: Text("Login"),
            ),
            SizedBox(height: 10),
            TextButton(
              onPressed: () {},
              child: Text("Forgot Password?"),
            ),
            SizedBox(height: 20),
            Text("Or continue with"),
            SizedBox(height: 10),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                IconButton(
                  icon: Icon(Icons.g_mobiledata, size: 30),
                  onPressed: () {},
                ),
                IconButton(
                  icon: Icon(Icons.facebook, size: 30),
                  onPressed: () {},
                ),
                IconButton(
                  icon: Icon(Icons.link, size: 30),
                  onPressed: () {},
                ),
              ],
            ),
            SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text("Don't have an account?"),
                TextButton(
                  onPressed: () {
                    Navigator.pushReplacement(
                      context,
                      MaterialPageRoute(builder: (_) => SignupScreen()),
                    );
                  },
                  child: Text("Sign Up"),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}