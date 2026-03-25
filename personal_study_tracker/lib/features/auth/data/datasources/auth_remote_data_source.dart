import 'package:dio/dio.dart';
import '../../../../core/network/api_client.dart';

abstract class AuthRemoteDataSource {
  Future<Map<String, dynamic>> login(String email, String password);
  Future<Map<String, dynamic>> register(String email, String password, String? fullName);
  Future<Map<String, dynamic>> getProfile();
  Future<void> logout();
}

class AuthRemoteDataSourceImpl implements AuthRemoteDataSource {
  final ApiClient apiClient;

  AuthRemoteDataSourceImpl(this.apiClient);

  @override
  Future<Map<String, dynamic>> login(String email, String password) async {
    // OAuth2 form format for backend
    final formData = {
      'username': email,
      'password': password,
    };
    final resp = await apiClient.post(
      '/auth/login',
      data: FormData.fromMap(formData),
      options: Options(contentType: Headers.formUrlEncodedContentType),
    );

    final data = Map<String, dynamic>.from(resp.data as Map);

    // Store tokens in ApiClient for subsequent requests
    if (data['access_token'] != null) {
      apiClient.setAccessToken(data['access_token'] as String);
      await apiClient.persistToken(data['access_token'] as String);
    }
    if (data['refresh_token'] != null) {
      await apiClient.persistRefreshToken(data['refresh_token'] as String);
    }

    return data;
  }

  @override
  Future<Map<String, dynamic>> register(String email, String password, String? fullName) async {
    final resp = await apiClient.post('/auth/register', data: {
      'email': email,
      'password': password,
      'full_name': fullName,
      'role': 'user',
    });
    return Map<String, dynamic>.from(resp.data as Map);
  }

  @override
  Future<Map<String, dynamic>> getProfile() async {
    final resp = await apiClient.get('/auth/me');
    return Map<String, dynamic>.from(resp.data as Map);
  }

  @override
  Future<void> logout() async {
    await apiClient.clearPersistedTokens();
  }
}
