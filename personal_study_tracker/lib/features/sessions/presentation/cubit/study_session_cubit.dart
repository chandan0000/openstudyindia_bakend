import 'dart:async';

import 'package:bloc/bloc.dart';

import '../../domain/entities/study_session.dart';
import '../../domain/usecases/end_session.dart';
import '../../domain/usecases/get_sessions.dart';
import '../../domain/usecases/start_session.dart';
import 'study_session_state.dart';

class StudySessionCubit extends Cubit<StudySessionState> {
  final GetSessions getSessions;
  final StartSession startSessionUseCase;
  final EndSession endSessionUseCase;

  Timer? _timer;

  StudySessionCubit({
    required this.getSessions,
    required this.startSessionUseCase,
    required this.endSessionUseCase,
  }) : super(const StudySessionInitial());

  Future<void> loadSessions() async {
    emit(const StudySessionLoading());
    try {
      final sessions = await getSessions();
      emit(StudySessionLoaded(sessions));
    } catch (e) {
      emit(StudySessionError('Could not load sessions. ${e.toString()}'));
    }
  }

  Future<void> startSession(String subjectId) async {
    emit(const StudySessionLoading());
    try {
      final session = await startSessionUseCase(subjectId);
      _startTimer(session);
      emit(StudySessionActive(session, Duration.zero));
    } catch (e) {
      emit(StudySessionError('Could not start session. ${e.toString()}'));
    }
  }

  Future<void> endSession() async {
    try {
      final session = await endSessionUseCase();
      _timer?.cancel();
      await loadSessions();
      emit(StudySessionLoaded([session]));
    } catch (e) {
      emit(StudySessionError('Could not end session. ${e.toString()}'));
    }
  }

  void _startTimer(StudySession session) {
    _timer?.cancel();
    _timer = Timer.periodic(const Duration(seconds: 1), (_) {
      final now = DateTime.now();
      final elapsed = now.difference(session.startTime);
      emit(StudySessionActive(session, elapsed));
    });
  }

  @override
  Future<void> close() {
    _timer?.cancel();
    return super.close();
  }
}
