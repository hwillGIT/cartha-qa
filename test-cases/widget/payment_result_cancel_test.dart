import 'package:carthaai/screens/payment_result_screen.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

/// Exception-flow coverage for the Stripe-redirect payment cancel/decline paths.
///
/// Gap source: docs/EXCEPTION_FLOW_GAP_MATRIX.md — "Payment fail / cancel"
/// had ZERO Maestro flows and ZERO widget tests. This test family covers the
/// dead-end state when a user cancels or fails to complete a Stripe payment,
/// ensuring:
///   1. The cancel state is explicitly communicated (not hidden or falsely positive)
///   2. The recovery affordance (Continue button) actually works
///   3. A cancelled tier purchase never falsely claims "activated"
///
/// Preconditions:
///   - Cold app start (PaymentResultScreen mounted with success=false)
///   - No authentication required (sync UI state)
void main() {
  group('PaymentResultScreen - cancel path', () {
    testWidgets(
      'cancel shows "Payment Cancelled" message',
      (WidgetTester tester) async {
        const success = false;
        const productId = 'test-product-id';
        const tier = 'PREMIUM';

        await tester.pumpWidget(
          MaterialApp(
            home: PaymentResultScreen(
              success: success,
              productId: productId,
              tier: tier,
            ),
            // Provide the '/' route the Continue button pushes to via
            // onGenerateRoute (cannot use a routes['/'] entry alongside `home`).
            onGenerateRoute: (settings) => MaterialPageRoute(
              builder: (_) => const Scaffold(body: Text('ROOT_SPLASH_STUB')),
              settings: settings,
            ),
          ),
        );
        await tester.pump();

        // The cancel message must be explicit — never falsely positive or hidden.
        expect(
          find.text('Payment Cancelled'),
          findsOneWidget,
          reason: 'Cancel state must show explicit "Payment Cancelled" message',
        );

        // Secondary confirmation text
        expect(
          find.text('Payment was cancelled. No charges were made.'),
          findsOneWidget,
          reason: 'Must reassure user no charges occurred',
        );
      },
    );

    testWidgets(
      'continue button escapes to root',
      (WidgetTester tester) async {
        const success = false;
        const productId = 'test-product-id';
        const tier = 'PREMIUM';

        await tester.pumpWidget(
          MaterialApp(
            home: PaymentResultScreen(
              success: success,
              productId: productId,
              tier: tier,
            ),
            onGenerateRoute: (settings) => MaterialPageRoute(
              builder: (_) => const Scaffold(body: Text('ROOT_SPLASH_STUB')),
              settings: settings,
            ),
          ),
        );
        await tester.pump();

        // Tap the Continue button (the sole recovery affordance from cancel)
        await tester.tap(find.byType(ElevatedButton));
        await tester.pump();

        // The button should navigate to '/', escaping the dead-end.
        // Verify by checking that ROOT_SPLASH_STUB is now visible (i.e., nav succeeded).
        expect(
          find.text('ROOT_SPLASH_STUB'),
          findsOneWidget,
          reason: 'Continue button must navigate away from cancel dead-end',
        );
      },
    );

    testWidgets(
      'cancel path never shows success-only chrome for a tier purchase',
      (WidgetTester tester) async {
        const success = false;
        const productId = 'test-product-id';
        const tier = 'PREMIUM';

        await tester.pumpWidget(
          MaterialApp(
            home: PaymentResultScreen(
              success: success,
              productId: productId,
              tier: tier,
            ),
            onGenerateRoute: (settings) => MaterialPageRoute(
              builder: (_) => const Scaffold(body: Text('ROOT_SPLASH_STUB')),
              settings: settings,
            ),
          ),
        );
        await tester.pump();

        // The cancel state must never claim success (e.g., "Subscription Activated").
        // This is a critical UX dead-end: if a tier purchase is cancelled, the user
        // must not be falsely reassured they now have the tier.
        expect(
          find.text('Subscription Activated'),
          findsNothing,
          reason: 'Cancelled payment must never falsely claim tier activation',
        );

        // Verify cancel-specific messaging is present instead
        expect(
          find.text('Payment Cancelled'),
          findsOneWidget,
          reason: 'Must explicitly say "Cancelled", not "Success"',
        );
      },
    );
  });
}
