import 'package:flutter_test/flutter_test.dart';
import 'package:personal_study_tracker/core/service_locator.dart';
import 'package:personal_study_tracker/features/auth/presentation/screens/login_screen.dart';
import 'package:personal_study_tracker/main.dart';

void main() {
  setUp(() {
    initServiceLocator();
  });

  testWidgets('App widget builds without errors', (WidgetTester tester) async {
    await tester.pumpWidget(const PersonalStudyTrackerApp());
    await tester.pump(const Duration(milliseconds: 500));

    expect(tester.takeException(), isNull);
  });
}
