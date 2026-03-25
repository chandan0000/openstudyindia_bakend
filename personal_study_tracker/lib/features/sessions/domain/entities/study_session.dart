class StudySession {
  final String id;
  final String topicId;
  final DateTime startTime;
  final DateTime? endTime;
  final int durationMinutes;

  StudySession({
    required this.id,
    required this.topicId,
    required this.startTime,
    this.endTime,
    this.durationMinutes = 0,
  });

  bool get isActive => endTime == null;
}
