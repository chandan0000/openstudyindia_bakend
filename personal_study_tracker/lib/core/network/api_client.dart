import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../config/app_config.dart';
import '../errors/app_exception.dart';

class ApiClient {
  static final ApiClient _instance = ApiClient._internal();
  factory ApiClient() => _instance;

  final Dio dio;
  String? _accessToken;

  ApiClient._internal()
      : dio = Dio(BaseOptions(
          baseUrl: AppConfig.baseUrl,
          connectTimeout: const Duration(milliseconds: AppConfig.connectTimeoutMs),
          receiveTimeout: const Duration(milliseconds: AppConfig.receiveTimeoutMs),
          contentType: 'application/json',
          responseType: ResponseType.json,
        )) {
    _setupInterceptors();
  }

  void _setupInterceptors() {
    // Request interceptor - add auth token
    dio.interceptors.add(InterceptorsWrapper(
      onRequest: (options, handler) async {
        if (_accessToken != null) {
          options.headers['Authorization'] = 'Bearer $_accessToken';
        }
        if (kDebugMode) {
          print('Request: ${options.method} ${options.path}');
        }
        handler.next(options);
      },
      onResponse: (response, handler) {
        if (kDebugMode) {
          print('Response: ${response.statusCode} ${response.requestOptions.path}');
        }
        handler.next(response);
      },
      onError: (DioException error, handler) {
        if (kDebugMode) {
          print('Error: ${error.response?.statusCode} ${error.message}');
        }
        handler.next(error);
      },
    ));

    // Logging interceptor for debug mode
    dio.interceptors.add(LogInterceptor(
      request: kDebugMode,
      responseBody: kDebugMode,
      requestBody: kDebugMode,
      error: kDebugMode,
      requestHeader: kDebugMode,
      responseHeader: kDebugMode,
    ));
  }

  // Token management
  void setAccessToken(String token) {
    _accessToken = token;
  }

  void clearAccessToken() {
    _accessToken = null;
  }

  String? get accessToken => _accessToken;

  Future<void> persistToken(String token) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('access_token', token);
  }

  Future<void> persistRefreshToken(String token) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('refresh_token', token);
  }

  Future<void> loadPersistedToken() async {
    final prefs = await SharedPreferences.getInstance();
    _accessToken = prefs.getString('access_token');
  }

  Future<void> clearPersistedTokens() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('access_token');
    await prefs.remove('refresh_token');
    _accessToken = null;
  }

  // HTTP methods with error handling
  Future<Response<T>> get<T>(String path, {Map<String, dynamic>? queryParameters}) async {
    try {
      return await dio.get<T>(path, queryParameters: queryParameters);
    } on DioException catch (e) {
      throw _handleDioError(e);
    }
  }

  Future<Response<T>> post<T>(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) async {
    try {
      return await dio.post<T>(
        path,
        data: data,
        queryParameters: queryParameters,
        options: options,
      );
    } on DioException catch (e) {
      throw _handleDioError(e);
    }
  }

  Future<Response<T>> put<T>(String path, {dynamic data}) async {
    try {
      return await dio.put<T>(path, data: data);
    } on DioException catch (e) {
      throw _handleDioError(e);
    }
  }

  Future<Response<T>> patch<T>(String path, {dynamic data}) async {
    try {
      return await dio.patch<T>(path, data: data);
    } on DioException catch (e) {
      throw _handleDioError(e);
    }
  }

  Future<Response<T>> delete<T>(String path, {dynamic data}) async {
    try {
      return await dio.delete<T>(path, data: data);
    } on DioException catch (e) {
      throw _handleDioError(e);
    }
  }

  AppException _handleDioError(DioException error) {
    switch (error.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.sendTimeout:
      case DioExceptionType.receiveTimeout:
        return const NetworkException('Connection timeout. Please try again.');
      case DioExceptionType.badResponse:
        final statusCode = error.response?.statusCode;
        final data = error.response?.data;
        final message = data is Map<String, dynamic> ? data['message'] : null;

        if (statusCode == 401) {
          return UnauthorizedException(message ?? 'Session expired. Please login again.');
        } else if (statusCode == 404) {
          return NotFoundException(message ?? 'Resource not found.');
        } else if (statusCode == 409) {
          return ConflictException(message ?? 'Resource already exists.');
        } else if (statusCode != null && statusCode >= 500) {
          return ServerException(message ?? 'Server error. Please try again later.');
        }
        return ApiException(message ?? 'An error occurred.', statusCode: statusCode);
      case DioExceptionType.cancel:
        return const CancelledException('Request cancelled.');
      case DioExceptionType.connectionError:
        return const NetworkException('No internet connection.');
      default:
        return const UnknownException('An unexpected error occurred.');
    }
  }
}
