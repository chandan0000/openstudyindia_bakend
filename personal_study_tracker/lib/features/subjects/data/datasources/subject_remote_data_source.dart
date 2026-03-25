import '../../../../core/network/api_client.dart';
import '../models/subject_model.dart';
import '../models/topic_model.dart';

abstract class SubjectRemoteDataSource {
  Future<List<SubjectModel>> getSubjects({int page = 1, int size = 30});
  Future<SubjectModel> createSubject(String name);
  Future<List<TopicModel>> getTopics(String subjectId, {int page = 1, int size = 30});
  Future<TopicModel> createTopic(String subjectId, String name);
}

class SubjectRemoteDataSourceImpl implements SubjectRemoteDataSource {
  final ApiClient apiClient;

  SubjectRemoteDataSourceImpl(this.apiClient);

  @override
  Future<List<SubjectModel>> getSubjects({int page = 1, int size = 30}) async {
    final resp = await apiClient.get('/subjects', queryParameters: {'page': page, 'size': size});
    final map = resp.data as Map<String, dynamic>? ?? {};
    final items = map['items'] as List<dynamic>? ?? [];
    return items.map((item) => SubjectModel.fromJson(item as Map<String, dynamic>)).toList();
  }

  @override
  Future<SubjectModel> createSubject(String name) async {
    final resp = await apiClient.post('/subjects', data: {'name': name});
    return SubjectModel.fromJson(resp.data as Map<String, dynamic>);
  }

  @override
  Future<List<TopicModel>> getTopics(String subjectId, {int page = 1, int size = 30}) async {
    final resp = await apiClient.get('/topics', queryParameters: {'subject_id': subjectId, 'page': page, 'size': size});
    final map = resp.data as Map<String, dynamic>? ?? {};
    final items = map['items'] as List<dynamic>? ?? [];
    return items.map((item) => TopicModel.fromJson(item as Map<String, dynamic>)).toList();
  }

  @override
  Future<TopicModel> createTopic(String subjectId, String name) async {
    final resp = await apiClient.post('/topics', data: {'subject_id': subjectId, 'name': name});
    return TopicModel.fromJson(resp.data as Map<String, dynamic>);
  }
}
