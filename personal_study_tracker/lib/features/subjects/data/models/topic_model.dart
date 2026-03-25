import '../../domain/entities/topic.dart';

class TopicModel extends Topic {
  TopicModel({required String id, required String name, required String subjectId})
      : super(id: id, name: name, subjectId: subjectId);

  factory TopicModel.fromJson(Map<String, dynamic> json) {
    return TopicModel(
      id: json['id']?.toString() ?? '',
      name: json['name']?.toString() ?? '',
      subjectId: json['subject_id']?.toString() ?? '',
    );
  }
}
