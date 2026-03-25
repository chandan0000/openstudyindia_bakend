/// Base exception class for all app errors
abstract class AppException implements Exception {
  final String message;
  final int? statusCode;

  const AppException(this.message, {this.statusCode});

  @override
  String toString() => message;
}

/// Network-related exceptions
class NetworkException extends AppException {
  const NetworkException(super.message);
}

/// Authentication exceptions
class UnauthorizedException extends AppException {
  const UnauthorizedException(super.message);
}

/// Resource not found
class NotFoundException extends AppException {
  const NotFoundException(super.message);
}

/// Conflict (duplicate, etc.)
class ConflictException extends AppException {
  const ConflictException(super.message);
}

/// Server error
class ServerException extends AppException {
  const ServerException(super.message);
}

/// API error with status code
class ApiException extends AppException {
  const ApiException(super.message, {super.statusCode});
}

/// Request cancelled
class CancelledException extends AppException {
  const CancelledException(super.message);
}

/// Unknown error
class UnknownException extends AppException {
  const UnknownException(super.message);
}

/// Validation error
class ValidationException extends AppException {
  final Map<String, dynamic>? errors;

  const ValidationException(super.message, {this.errors});
}
