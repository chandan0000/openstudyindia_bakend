import '../entities/study_session.dart';

abstract class StudySessionRepository {
  Future<List<StudySession>> fetchSessions();
  Future<StudySession> startSession(String topicId);
  Future<StudySession> endSession();
}
