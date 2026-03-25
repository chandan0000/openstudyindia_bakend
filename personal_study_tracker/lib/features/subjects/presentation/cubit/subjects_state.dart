import '../../domain/entities/subject.dart';
import '../../domain/entities/topic.dart';

abstract class SubjectsState {
  const SubjectsState();
}

class SubjectsInitial extends SubjectsState {
  const SubjectsInitial();
}

class SubjectsLoading extends SubjectsState {
  const SubjectsLoading();
}

class SubjectsLoaded extends SubjectsState {
  final List<Subject> subjects;
  const SubjectsLoaded(this.subjects);
}

class TopicsLoaded extends SubjectsState {
  final List<Topic> topics;
  const TopicsLoaded(this.topics);
}

class SubjectsError extends SubjectsState {
  final String message;
  const SubjectsError(this.message);
}
