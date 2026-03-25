import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../../domain/entities/study_session.dart';
import '../cubit/study_session_cubit.dart';
import '../cubit/study_session_state.dart';

class StudySessionsPage extends StatefulWidget {
  const StudySessionsPage({super.key});

  @override
  State<StudySessionsPage> createState() => _StudySessionsPageState();
}

class _StudySessionsPageState extends State<StudySessionsPage> {
  String selectedTopic = '00000000-0000-0000-0000-000000000000';

  @override
  void initState() {
    super.initState();
    context.read<StudySessionCubit>().loadSessions();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Study Sessions'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Card(
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
              elevation: 4,
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text('Select Topic', style: TextStyle(fontWeight: FontWeight.bold)),
                    DropdownButton<String>(
                      value: selectedTopic,
                      items: const [
                        DropdownMenuItem(value: '00000000-0000-0000-0000-000000000001', child: Text('Math - Algebra')),
                        DropdownMenuItem(value: '00000000-0000-0000-0000-000000000002', child: Text('Science - Physics')),
                        DropdownMenuItem(value: '00000000-0000-0000-0000-000000000003', child: Text('History - WWII')),
                      ],
                      onChanged: (value) {
                        if (value != null) {
                          setState(() => selectedTopic = value);
                        }
                      },
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),
            BlocConsumer<StudySessionCubit, StudySessionState>(
              listener: (context, state) {
                if (state is StudySessionError) {
                  ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(state.message)));
                }
              },
              builder: (context, state) {
                if (state is StudySessionLoading || state is StudySessionInitial) {
                  return const Center(child: CircularProgressIndicator());
                }

                if (state is StudySessionActive) {
                  return _buildActiveSession(context, state);
                }
                if (state is StudySessionLoaded) {
                  return Expanded(child: _buildSessionHistory(state.sessions));
                }

                if (state is StudySessionError) {
                  return Expanded(child: Center(child: Text('Error: ${state.message}')));
                }

                return const SizedBox.shrink();
              },
            ),
          ],
        ),
      ),
      floatingActionButton: _buildSessionButtons(context),
    );
  }

  Widget _buildActiveSession(BuildContext context, StudySessionActive state) {
    return Expanded(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Card(
            margin: EdgeInsets.zero,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Live Session', style: Theme.of(context).textTheme.titleLarge),
                  const SizedBox(height: 8),
                  Text('Topic: ${state.session.topicId}', style: Theme.of(context).textTheme.bodyLarge),
                  const SizedBox(height: 8),
                  Text('Elapsed: ${_formatDuration(state.elapsed)}', style: Theme.of(context).textTheme.headlineSmall),
                ],
              ),
            ),
          ),
          const SizedBox(height: 24),
          Expanded(child: _buildSessionHistory([state.session])),
        ],
      ),
    );
  }

  String _formatDuration(Duration duration) {
    final h = duration.inHours.toString().padLeft(2, '0');
    final m = (duration.inMinutes % 60).toString().padLeft(2, '0');
    final s = (duration.inSeconds % 60).toString().padLeft(2, '0');
    return '$h:$m:$s';
  }

  Widget _buildSessionHistory(List<StudySession> sessions) {
    if (sessions.isEmpty) {
      return const Center(child: Text('No sessions yet. Start your first session!'));
    }

    return ListView.separated(
      itemCount: sessions.length,
      separatorBuilder: (context, index) => const SizedBox(height: 10),
      itemBuilder: (context, index) {
        final session = sessions[index];
        final duration = session.endTime == null
            ? DateTime.now().difference(session.startTime)
            : session.endTime!.difference(session.startTime);

        return Card(
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
          elevation: 2,
          child: ListTile(
            title: Text('Session ${session.id}', style: const TextStyle(fontWeight: FontWeight.w600)),
            subtitle: Text('Topic: ${session.topicId}\nDuration: ${_formatDuration(duration)}'),
            trailing: session.isActive
                ? ElevatedButton(
                    onPressed: () => context.read<StudySessionCubit>().endSession(),
                    child: const Text('End'),
                  )
                : const Icon(Icons.check, color: Colors.green),
          ),
        );
      },
    );
  }

  Widget _buildSessionButtons(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        FloatingActionButton.extended(
          heroTag: 'start',
          onPressed: () => context.read<StudySessionCubit>().startSession(selectedTopic),
          icon: const Icon(Icons.play_arrow),
          label: const Text('Start'),
        ),
        const SizedBox(width: 12),
        FloatingActionButton.extended(
          heroTag: 'refresh',
          onPressed: () => context.read<StudySessionCubit>().loadSessions(),
          icon: const Icon(Icons.refresh),
          label: const Text('Refresh'),
        ),
      ],
    );
  }
}
