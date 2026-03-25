import '../entities/study_session.dart';
import '../repositories/study_session_repository.dart';

class GetSessions {
  final StudySessionRepository repository;

  GetSessions(this.repository);

  Future<List<StudySession>> call() => repository.fetchSessions();
}
