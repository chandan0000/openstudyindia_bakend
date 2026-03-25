import '../../domain/entities/study_session.dart';
import '../../domain/repositories/study_session_repository.dart';
import '../datasources/session_remote_data_source.dart';

class StudySessionRepositoryImpl implements StudySessionRepository {
  final SessionRemoteDataSource remoteDataSource;

  StudySessionRepositoryImpl(this.remoteDataSource);

  @override
  Future<List<StudySession>> fetchSessions() async {
    return await remoteDataSource.getAllSessions();
  }

  @override
  Future<StudySession> startSession(String topicId) async {
    return await remoteDataSource.startSession(topicId);
  }

  @override
  Future<StudySession> endSession() async {
    return await remoteDataSource.endSession();
  }
}
