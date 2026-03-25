import '../../domain/entities/study_session.dart';

abstract class StudySessionState {
  const StudySessionState();
}

class StudySessionInitial extends StudySessionState {
  const StudySessionInitial();
}

class StudySessionLoading extends StudySessionState {
  const StudySessionLoading();
}

class StudySessionLoaded extends StudySessionState {
  final List<StudySession> sessions;

  const StudySessionLoaded(this.sessions);
}

class StudySessionActive extends StudySessionState {
  final StudySession session;
  final Duration elapsed;

  const StudySessionActive(this.session, this.elapsed);
}

class StudySessionError extends StudySessionState {
  final String message;

  const StudySessionError(this.message);
}
