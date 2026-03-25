import 'package:get_it/get_it.dart';

import '../core/network/api_client.dart';
import '../features/auth/data/datasources/auth_remote_data_source.dart';
import '../features/auth/data/repositories/auth_repository_impl.dart';
import '../features/auth/domain/repositories/auth_repository.dart';
import '../features/auth/presentation/cubit/auth_cubit.dart';
import '../features/sessions/data/datasources/session_remote_data_source.dart';
import '../features/sessions/data/repositories/study_session_repository_impl.dart';
import '../features/sessions/domain/repositories/study_session_repository.dart';
import '../features/sessions/domain/usecases/end_session.dart';
import '../features/sessions/domain/usecases/get_sessions.dart';
import '../features/sessions/domain/usecases/start_session.dart';
import '../features/subjects/data/datasources/subject_remote_data_source.dart';
import '../features/subjects/data/repositories/subject_repository_impl.dart';
import '../features/subjects/domain/repositories/subject_repository.dart';
import '../features/subjects/domain/usecases/create_subject.dart';
import '../features/subjects/domain/usecases/create_topic.dart';
import '../features/subjects/domain/usecases/get_subjects.dart';
import '../features/subjects/domain/usecases/get_topics.dart';

final locator = GetIt.instance;

void initServiceLocator() {
  locator.registerLazySingleton(() => ApiClient());

  locator.registerLazySingleton<SessionRemoteDataSource>(() => SessionRemoteDataSourceImpl(locator()));
  locator.registerLazySingleton<StudySessionRepository>(() => StudySessionRepositoryImpl(locator()));

  locator.registerFactory(() => GetSessions(locator()));
  locator.registerFactory(() => StartSession(locator()));
  locator.registerFactory(() => EndSession(locator()));

  // Subjects
  locator.registerLazySingleton<SubjectRemoteDataSource>(() => SubjectRemoteDataSourceImpl(locator()));
  locator.registerLazySingleton<SubjectRepository>(() => SubjectRepositoryImpl(locator()));
  locator.registerFactory(() => GetSubjects(locator()));
  locator.registerFactory(() => CreateSubject(locator()));
  locator.registerFactory(() => GetTopics(locator()));
  locator.registerFactory(() => CreateTopic(locator()));

  // Auth
  locator.registerLazySingleton<AuthRemoteDataSource>(() => AuthRemoteDataSourceImpl(locator()));
  locator.registerLazySingleton<AuthRepository>(() => AuthRepositoryImpl(locator(), locator()));
  locator.registerFactory(() => AuthCubit(locator(), locator()));
}
