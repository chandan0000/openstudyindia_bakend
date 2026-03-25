import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../cubit/subjects_cubit.dart';
import '../cubit/subjects_state.dart';

class SubjectsPage extends StatefulWidget {
  const SubjectsPage({super.key});

  @override
  State<SubjectsPage> createState() => _SubjectsPageState();
}

class _SubjectsPageState extends State<SubjectsPage> {
  final _subjectController = TextEditingController();
  final _topicController = TextEditingController();
  String? selectedSubjectId;

  @override
  void initState() {
    super.initState();
    context.read<SubjectsCubit>().loadSubjects();
  }

  @override
  void dispose() {
    _subjectController.dispose();
    _topicController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Subjects & Topics')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _subjectController,
                    decoration: const InputDecoration(labelText: 'New subject'),
                  ),
                ),
                const SizedBox(width: 8),
                ElevatedButton(
                  onPressed: () {
                    final value = _subjectController.text.trim();
                    if (value.isNotEmpty) {
                      context.read<SubjectsCubit>().addSubject(value);
                      _subjectController.clear();
                    }
                  },
                  child: const Text('Add'),
                ),
              ],
            ),
            const SizedBox(height: 16),
            Expanded(
              child: BlocConsumer<SubjectsCubit, SubjectsState>(
                listener: (context, state) {
                  if (state is SubjectsError) {
                    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(state.message)));
                  }
                },
                builder: (context, state) {
                  if (state is SubjectsLoading || state is SubjectsInitial) {
                    return const Center(child: CircularProgressIndicator());
                  }

                  if (state is SubjectsLoaded) {
                    final items = state.subjects;
                    if (items.isEmpty) {
                      return const Center(child: Text('No subjects yet'));
                    }
                    return ListView.builder(
                      itemCount: items.length,
                      itemBuilder: (context, index) {
                        final subject = items[index];
                        final selected = selectedSubjectId == subject.id;
                        return ListTile(
                          title: Text(subject.name),
                          selected: selected,
                          onTap: () {
                            setState(() {
                              selectedSubjectId = subject.id;
                            });
                            context.read<SubjectsCubit>().loadTopics(subject.id);
                          },
                        );
                      },
                    );
                  }

                  if (state is TopicsLoaded) {
                    final topics = state.topics;
                    return Column(
                      children: [
                        Expanded(
                          child: ListView.builder(
                            itemCount: topics.length,
                            itemBuilder: (context, index) => ListTile(
                              title: Text(topics[index].name),
                            ),
                          ),
                        ),
                        Row(
                          children: [
                            Expanded(
                              child: TextField(
                                controller: _topicController,
                                decoration: const InputDecoration(labelText: 'New topic'),
                              ),
                            ),
                            const SizedBox(width: 8),
                            ElevatedButton(
                              onPressed: selectedSubjectId == null
                                  ? null
                                  : () {
                                      final value = _topicController.text.trim();
                                      if (value.isNotEmpty && selectedSubjectId != null) {
                                        context.read<SubjectsCubit>().addTopic(selectedSubjectId!, value);
                                        _topicController.clear();
                                      }
                                    },
                              child: const Text('Add'),
                            )
                          ],
                        ),
                      ],
                    );
                  }

                  if (state is SubjectsError) {
                    return Center(child: Text(state.message));
                  }

                  return const SizedBox.shrink();
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
