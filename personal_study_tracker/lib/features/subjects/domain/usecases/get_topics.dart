import '../entities/topic.dart';
import '../repositories/subject_repository.dart';

class GetTopics {
  final SubjectRepository repository;

  GetTopics(this.repository);

  Future<List<Topic>> call(String subjectId, {int page = 1, int size = 30}) => repository.listTopics(subjectId, page: page, size: size);
}
