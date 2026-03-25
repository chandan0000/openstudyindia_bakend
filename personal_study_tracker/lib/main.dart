import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import 'core/service_locator.dart';
import 'features/auth/presentation/cubit/auth_cubit.dart';
import 'features/auth/presentation/cubit/auth_state.dart';
import 'features/auth/presentation/screens/login_screen.dart';
import 'features/home/presentation/pages/home_page.dart';
import 'features/profile/presentation/pages/profile_page.dart';
import 'features/subjects/presentation/pages/subjects_page.dart';
import 'features/sessions/presentation/cubit/study_session_cubit.dart';
import 'features/sessions/presentation/pages/study_sessions_page.dart';
import 'features/sessions/domain/usecases/end_session.dart';
import 'features/sessions/domain/usecases/get_sessions.dart';
import 'features/sessions/domain/usecases/start_session.dart';

void main() {
  initServiceLocator();
  runApp(const PersonalStudyTrackerApp());
}

class PersonalStudyTrackerApp extends StatelessWidget {
  const PersonalStudyTrackerApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiBlocProvider(
      providers: [
        BlocProvider<AuthCubit>(
          create: (_) => locator<AuthCubit>()..checkAuth(),
        ),
      ],
      child: MaterialApp(
        title: 'Personal Study Tracker',
        theme: ThemeData(
          useMaterial3: true,
          colorScheme: ColorScheme.fromSeed(seedColor: Colors.indigo),
        ),
        home: const AuthGate(),
      ),
    );
  }
}

class AuthGate extends StatelessWidget {
  const AuthGate({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocBuilder<AuthCubit, AuthState>(
      builder: (context, state) {
        if (state is AuthAuthenticated) {
          return const AppShell();
        }
        if (state is AuthLoading) {
          return const Scaffold(body: Center(child: CircularProgressIndicator()));
        }
        return const LoginScreen();
      },
    );
  }
}

class AppShell extends StatefulWidget {
  const AppShell({super.key});

  @override
  State<AppShell> createState() => _AppShellState();
}

class _AppShellState extends State<AppShell> {
  int _selectedIndex = 0;

  static late final List<Widget> _pageOptions;

  @override
  void initState() {
    super.initState();
    _pageOptions = <Widget>[
      const HomePage(),
      const SubjectsPage(),
      BlocProvider(
        create: (_) => StudySessionCubit(
          getSessions: locator<GetSessions>(),
          startSessionUseCase: locator<StartSession>(),
          endSessionUseCase: locator<EndSession>(),
        ),
        child: const StudySessionsPage(),
      ),
      const ProfilePage(),
    ];
  }

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _pageOptions[_selectedIndex],
      bottomNavigationBar: NavigationBar(
        selectedIndex: _selectedIndex,
        onDestinationSelected: _onItemTapped,
        destinations: const [
          NavigationDestination(icon: Icon(Icons.home), label: 'Home'),
          NavigationDestination(icon: Icon(Icons.book), label: 'Subjects'),
          NavigationDestination(icon: Icon(Icons.timer), label: 'Sessions'),
          NavigationDestination(icon: Icon(Icons.person), label: 'Profile'),
        ],
      ),
    );
  }
}
