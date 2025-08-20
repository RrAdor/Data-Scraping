import 'package:flutter/material.dart';
import '../utils/constants.dart';

class ContactInfo extends StatelessWidget {
  final IconData icon;
  final String text;

  const ContactInfo({
    Key? key,
    required this.icon,
    required this.text,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(bottom: 16),
      child: Row(
        children: [
          Icon(icon, color: AppColors.primary),
          SizedBox(width: 16),
          Text(text),
        ],
      ),
    );
  }
}