import 'package:bloc/bloc.dart';

import '../../domain/usecases/get_subjects.dart';
import '../../domain/usecases/create_subject.dart';
import '../../domain/usecases/get_topics.dart';
import '../../domain/usecases/create_topic.dart';
import 'subjects_state.dart';

class SubjectsCubit extends Cubit<SubjectsState> {
  final GetSubjects getSubjects;
  final CreateSubject createSubject;
  final GetTopics getTopics;
  final CreateTopic createTopic;

  SubjectsCubit({
    required this.getSubjects,
    required this.createSubject,
    required this.getTopics,
    required this.createTopic,
  }) : super(const SubjectsInitial());

  Future<void> loadSubjects() async {
    emit(const SubjectsLoading());
    try {
      final subjects = await getSubjects();
      emit(SubjectsLoaded(subjects));
    } catch (e) {
      emit(SubjectsError('Failed to load subjects: $e'));
    }
  }

  Future<void> addSubject(String name) async {
    emit(const SubjectsLoading());
    try {
      await createSubject(name);
      final subjects = await getSubjects();
      emit(SubjectsLoaded(subjects));
    } catch (e) {
      emit(SubjectsError('Failed to create subject: $e'));
    }
  }

  Future<void> loadTopics(String subjectId) async {
    emit(const SubjectsLoading());
    try {
      final topics = await getTopics(subjectId);
      emit(TopicsLoaded(topics));
    } catch (e) {
      emit(SubjectsError('Failed to load topics: $e'));
    }
  }

  Future<void> addTopic(String subjectId, String name) async {
    emit(const SubjectsLoading());
    try {
      await createTopic(subjectId, name);
      final topics = await getTopics(subjectId);
      emit(TopicsLoaded(topics));
    } catch (e) {
      emit(SubjectsError('Failed to create topic: $e'));
    }
  }
}
