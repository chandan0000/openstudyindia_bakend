import '../entities/subject.dart';
import '../repositories/subject_repository.dart';

class CreateSubject {
  final SubjectRepository repository;

  CreateSubject(this.repository);

  Future<Subject> call(String name) => repository.createSubject(name);
}
