import 'package:flutter/material.dart';
import '../utils/constants.dart';
import 'portal_screen.dart';
import 'login_screen.dart';

class SignupScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Sign Up"),
        backgroundColor: AppColors.primary,
      ),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              decoration: InputDecoration(
                  labelText: "Full Name",
                  prefixIcon: Icon(Icons.person)),
            ),
            TextField(
              decoration: InputDecoration(
                  labelText: "Email",
                  prefixIcon: Icon(Icons.email)),
            ),
            TextField(
              decoration: InputDecoration(
                  labelText: "Password",
                  prefixIcon: Icon(Icons.lock)),
              obscureText: true,
            ),
            TextField(
              decoration: InputDecoration(
                  labelText: "Confirm Password",
                  prefixIcon: Icon(Icons.lock)),
              obscureText: true,
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                    context, MaterialPageRoute(builder: (_) => PortalScreen()));
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: AppColors.primary,
                foregroundColor: Colors.white,
                minimumSize: Size(double.infinity, 50),
              ),
              child: Text("Create Account"),
            ),
            SizedBox(height: 20),
            Text("Or sign up with"),
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
                Text("Already have an account?"),
                TextButton(
                  onPressed: () {
                    Navigator.pushReplacement(context,
                        MaterialPageRoute(builder: (_) => LoginScreen()));
                  },
                  child: Text("Sign In"),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}