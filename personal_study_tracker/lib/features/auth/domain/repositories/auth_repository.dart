import '../entities/user.dart';

abstract class AuthRepository {
  Future<User> login(String email, String password);
  Future<User> register(String email, String password, {String? fullName});
  Future<User> getCurrentUser();
  Future<void> saveToken(String token);
  Future<String?> getToken();
  Future<void> logout();
}
