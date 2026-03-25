class AppConfig {
  const AppConfig._();

  // Backend running on local machine. Update to deployed URL as needed.
  // For Android emulator: use 10.0.2.2 instead of localhost.
  // For iOS simulator: keep localhost.
  // For web: use http://localhost:8000 and ensure backend CORS allows origin.
  static const String baseUrl = 'http://localhost:8000/api/v1';
  static const int connectTimeoutMs = 10000;
  static const int receiveTimeoutMs = 10000;
}
