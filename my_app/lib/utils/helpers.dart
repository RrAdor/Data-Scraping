import 'package:flutter/material.dart';

// Helper functions for the app

String formatDate(DateTime date) {
  return "${date.day}/${date.month}/${date.year}";
}

String formatDateTime(DateTime date) {
  return "${date.day}/${date.month}/${date.year} ${date.hour}:${date.minute.toString().padLeft(2, '0')}";
}

String truncateText(String text, int maxLength) {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
}

void showSnackBar(BuildContext context, String message, {bool isError = false}) {
  ScaffoldMessenger.of(context).showSnackBar(
    SnackBar(
      content: Text(message),
      backgroundColor: isError ? Colors.red : Colors.green,
      duration: Duration(seconds: 3),
    ),
  );
}

Future<void> showLoadingDialog(BuildContext context, String message) async {
  return showDialog(
    context: context,
    barrierDismissible: false,
    builder: (BuildContext context) {
      return AlertDialog(
        content: Row(
          children: [
            CircularProgressIndicator(),
            SizedBox(width: 20),
            Text(message),
          ],
        ),
      );
    },
  );
}