import '../../domain/entities/subject.dart';
import '../../domain/entities/topic.dart';
import '../../domain/repositories/subject_repository.dart';
import '../datasources/subject_remote_data_source.dart';

class SubjectRepositoryImpl implements SubjectRepository {
  final SubjectRemoteDataSource remoteDataSource;

  SubjectRepositoryImpl(this.remoteDataSource);

  @override
  Future<List<Subject>> listSubjects({int page = 1, int size = 30}) async {
    return await remoteDataSource.getSubjects(page: page, size: size);
  }

  @override
  Future<Subject> createSubject(String name) async {
    return await remoteDataSource.createSubject(name);
  }

  @override
  Future<List<Topic>> listTopics(String subjectId, {int page = 1, int size = 30}) async {
    return await remoteDataSource.getTopics(subjectId, page: page, size: size);
  }

  @override
  Future<Topic> createTopic(String subjectId, String name) async {
    return await remoteDataSource.createTopic(subjectId, name);
  }
}
