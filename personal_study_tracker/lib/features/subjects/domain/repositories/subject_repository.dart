import '../entities/subject.dart';
import '../entities/topic.dart';

abstract class SubjectRepository {
  Future<List<Subject>> listSubjects({int page = 1, int size = 30});
  Future<Subject> createSubject(String name);
  Future<List<Topic>> listTopics(String subjectId, {int page = 1, int size = 30});
  Future<Topic> createTopic(String subjectId, String name);
}
