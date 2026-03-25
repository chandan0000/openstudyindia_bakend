import 'package:shared_preferences/shared_preferences.dart';

import '../../../../core/network/api_client.dart';
import '../../domain/entities/user.dart';
import '../../domain/repositories/auth_repository.dart';
import '../datasources/auth_remote_data_source.dart';

class AuthRepositoryImpl implements AuthRepository {
  final AuthRemoteDataSource remoteDataSource;
  final ApiClient apiClient;

  AuthRepositoryImpl(this.remoteDataSource, this.apiClient);

  @override
  Future<User> login(String email, String password) async {
    final json = await remoteDataSource.login(email, password);
    final token = json['access_token'] as String?;
    if (token == null || token.isEmpty) {
      throw Exception('Authentication token missing from response');
    }

    await saveToken(token);
    apiClient.setAccessToken(token);

    final profile = await getCurrentUser();
    return profile;
  }

  @override
  Future<User> register(String email, String password, {String? fullName}) async {
    final json = await remoteDataSource.register(email, password, fullName);
    // Assuming register returns user object without token, so login explicitly
    if (json['email'] == null) {
      throw Exception('Registration failed.');
    }
    // After successful register, login to get token and profile
    return await login(email, password);
  }

  @override
  Future<User> getCurrentUser() async {
    final data = await remoteDataSource.getProfile();
    return User(
      id: data['id']?.toString() ?? '',
      email: data['email']?.toString() ?? '',
      fullName: data['full_name']?.toString(),
      role: data['role']?.toString() ?? 'user',
      isActive: data['is_active'] as bool? ?? true,
      createdAt: data['created_at'] != null ? DateTime.parse(data['created_at'] as String) : null,
      updatedAt: data['updated_at'] != null ? DateTime.parse(data['updated_at'] as String) : null,
      token: apiClient.accessToken,
    );
  }

  @override
  Future<String?> getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('access_token');
  }

  @override
  Future<void> saveToken(String token) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('access_token', token);
    apiClient.setAccessToken(token);
  }

  @override
  Future<void> logout() async {
    await remoteDataSource.logout();
    apiClient.clearAccessToken();
  }
}
