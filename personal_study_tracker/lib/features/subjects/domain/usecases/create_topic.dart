import '../entities/topic.dart';
import '../repositories/subject_repository.dart';

class CreateTopic {
  final SubjectRepository repository;

  CreateTopic(this.repository);

  Future<Topic> call(String subjectId, String name) => repository.createTopic(subjectId, name);
}
