import '../entities/study_session.dart';
import '../repositories/study_session_repository.dart';

class StartSession {
  final StudySessionRepository repository;

  StartSession(this.repository);

  Future<StudySession> call(String subjectId) => repository.startSession(subjectId);
}
