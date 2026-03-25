import '../../domain/entities/study_session.dart';

class StudySessionModel extends StudySession {
  StudySessionModel({
    required String id,
    required String topicId,
    required DateTime startTime,
    DateTime? endTime,
    int durationMinutes = 0,
  }) : super(
          id: id,
          topicId: topicId,
          startTime: startTime,
          endTime: endTime,
          durationMinutes: durationMinutes,
        );

  factory StudySessionModel.fromJson(Map<String, dynamic> json) {
    return StudySessionModel(
      id: json['id'] as String,
      topicId: json['topic_id'] as String,
      startTime: DateTime.parse(json['start_time'] as String),
      endTime: json['end_time'] != null ? DateTime.parse(json['end_time'] as String) : null,
      durationMinutes: json['duration_minutes'] as int? ?? 0,
    );
  }

  Map<String, dynamic> toJson() => {
        'id': id,
        'topic_id': topicId,
        'start_time': startTime.toIso8601String(),
        'end_time': endTime?.toIso8601String(),
        'duration_minutes': durationMinutes,
      };
}
