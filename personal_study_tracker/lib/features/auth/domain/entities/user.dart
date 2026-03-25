class User {
  final String id;
  final String email;
  final String? fullName;
  final String? token;
  final String role;
  final bool isActive;
  final DateTime? createdAt;
  final DateTime? updatedAt;

  User({
    required this.id,
    required this.email,
    this.fullName,
    this.token,
    this.role = 'user',
    this.isActive = true,
    this.createdAt,
    this.updatedAt,
  });
}
