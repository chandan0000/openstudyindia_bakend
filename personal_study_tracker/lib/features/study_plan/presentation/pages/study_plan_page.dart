import 'package:flutter/material.dart';

class StudyPlanPage extends StatelessWidget {
  const StudyPlanPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Plans')),
      body: Center(child: Text('Daily plans and schedule will appear here.', style: Theme.of(context).textTheme.titleLarge)),
    );
  }
}
