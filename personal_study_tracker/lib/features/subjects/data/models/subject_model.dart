import '../../domain/entities/subject.dart';

class SubjectModel extends Subject {
  SubjectModel({required String id, required String name}) : super(id: id, name: name);

  factory SubjectModel.fromJson(Map<String, dynamic> json) {
    return SubjectModel(
      id: json['id']?.toString() ?? '',
      name: json['name']?.toString() ?? '',
    );
  }
}
