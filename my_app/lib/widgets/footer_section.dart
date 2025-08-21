import 'package:flutter/material.dart';
import '../utils/constants.dart';

class FooterSection extends StatelessWidget {
  final String title;
  final String? content;
  final List<String>? links;

  const FooterSection({
    Key? key,
    required this.title,
    this.content,
    this.links,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 105,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title,
              style: TextStyle(fontWeight: FontWeight.bold, color: Colors.white)),
          SizedBox(height: 10),
          if (content != null)
            Text(content!,
                style: TextStyle(color: Colors.white70, fontSize: 12)),
          if (links != null)
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: links!.map((link) =>
                  Padding(
                    padding: EdgeInsets.only(bottom: 5),
                    child: Text(link,
                        style: TextStyle(color: Colors.white70, fontSize: 12)),
                  )).toList(),
            ),
        ],
      ),
    );
  }
}