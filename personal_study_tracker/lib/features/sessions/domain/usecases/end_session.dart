import '../entities/study_session.dart';
import '../repositories/study_session_repository.dart';

class EndSession {
  final StudySessionRepository repository;

  EndSession(this.repository);

  Future<StudySession> call() => repository.endSession();
}
