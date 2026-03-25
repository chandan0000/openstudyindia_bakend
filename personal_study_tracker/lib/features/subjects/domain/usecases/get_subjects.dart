import '../entities/subject.dart';
import '../repositories/subject_repository.dart';

class GetSubjects {
  final SubjectRepository repository;

  GetSubjects(this.repository);

  Future<List<Subject>> call({int page = 1, int size = 30}) => repository.listSubjects(page: page, size: size);
}
