import 'package:bloc/bloc.dart';
import '../../../../core/network/api_client.dart';
import '../../domain/repositories/auth_repository.dart';
import 'auth_state.dart';

class AuthCubit extends Cubit<AuthState> {
  final AuthRepository repository;
  final ApiClient apiClient;

  AuthCubit(this.repository, this.apiClient) : super(const AuthInitial());

  Future<void> checkAuth() async {
    emit(const AuthLoading());
    try {
      await apiClient.loadPersistedToken();
      final token = await repository.getToken();
      if (token != null && token.isNotEmpty) {
        apiClient.setAccessToken(token);
        try {
          final user = await repository.getCurrentUser();
          emit(AuthAuthenticated(user));
        } catch (e) {
          await repository.logout();
          emit(const AuthUnauthenticated());
        }
      } else {
        emit(const AuthUnauthenticated());
      }
    } catch (e) {
      emit(const AuthUnauthenticated());
    }
  }


  Future<void> login(String email, String password) async {
    emit(const AuthLoading());
    try {
      final user = await repository.login(email, password);
      emit(AuthAuthenticated(user));
    } catch (e) {
      emit(AuthError('Login Failed: ${e.toString()}'));
    }
  }

  Future<void> register(String email, String password, {String? fullName}) async {
    emit(const AuthLoading());
    try {
      final user = await repository.register(email, password, fullName: fullName);
      emit(AuthAuthenticated(user));
    } catch (e) {
      emit(AuthError('Registration Failed: ${e.toString()}'));
    }
  }

  Future<void> logout() async {
    try {
      await repository.logout();
    } catch (e) {
      // Ignore errors on logout
    }
    emit(const AuthUnauthenticated());
  }
}
