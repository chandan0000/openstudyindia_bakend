import '../../../../core/network/api_client.dart';
import '../models/study_session_model.dart';

abstract class SessionRemoteDataSource {
  Future<List<StudySessionModel>> getAllSessions();
  Future<StudySessionModel> startSession(String topicId);
  Future<StudySessionModel> endSession();
}

class SessionRemoteDataSourceImpl implements SessionRemoteDataSource {
  final ApiClient apiClient;

  SessionRemoteDataSourceImpl(this.apiClient);

  @override
  Future<List<StudySessionModel>> getAllSessions() async {
    final resp = await apiClient.get('/study_sessions');
    final data = resp.data as Map<String, dynamic>? ?? {};
    final items = data['items'] as List<dynamic>? ?? [];
    return items.map((item) => StudySessionModel.fromJson(item as Map<String, dynamic>)).toList();
  }

  @override
  Future<StudySessionModel> startSession(String topicId) async {
    final resp = await apiClient.post('/study_sessions/start', data: {'topic_id': topicId});
    return StudySessionModel.fromJson(resp.data as Map<String, dynamic>);
  }

  @override
  Future<StudySessionModel> endSession() async {
    final resp = await apiClient.post('/study_sessions/end');
    return StudySessionModel.fromJson(resp.data as Map<String, dynamic>);
  }
}
