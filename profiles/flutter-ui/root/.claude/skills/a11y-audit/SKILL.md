---
name: a11y-audit
description: Accessibility audit (WCAG 2.1/2.2 AA) for Flutter/Web screens. Use before delivering new screens or during UI reviews.
---
# Criteria (verify against official WCAG text when reporting)
- Contrast: text >= 4.5:1 (large >= 3:1); component/graphics >= 3:1 (1.4.3, 1.4.11).
- Keyboard: fully operable, logical focus order, visible focus indicator, no focus traps (2.1.1, 2.4.3, 2.4.7).
- Touch target: 2.5.8 (AA, WCAG 2.2) requires >= 24x24 px; platform guidelines recommend 48 dp (Android) / 44 pt (iOS). 2.5.5 (44 px) is AAA level, not AA.
- Names/roles: every control must have an accessible label (4.1.2); error described in text, not color alone (3.3.1, 1.4.1).
- Zoom/font 200%: layout does not break; no truncated text.
- Motion: respect "reduce motion" preferences.

# Flutter
- Use `Semantics(label:, button:, ...)` where the widget is not natively semantic; use `ExcludeSemantics` only for decorative elements.
- Tests: `await expectLater(tester, meetsGuideline(androidTapTargetGuideline))`, `iOSTapTargetGuideline`, `labeledTapTargetGuideline`, `textContrastGuideline`.
- Test with screen readers (TalkBack / VoiceOver) whenever possible; automated checks catch only a subset of issues.

# Output (<= 20 lines)
`# | issue | criterion | severity (critical/major/minor) | remediation`. For untested items in screen readers: note "not verified".

# WCAG 2.1 AA quick reference
- Perceivable: text alternatives; captions; contrast at least 4.5:1 for text and 3:1 for large text and UI components; content usable without colour alone.
- Operable: every function reachable by keyboard; no keyboard trap; enough time; no content that flashes more than three times per second.
- Understandable: readable language; predictable navigation; clear error messages with a suggested fix.
- Robust: valid, named controls with a role and state exposed to assistive technology.

# Testing approach
- Check contrast with a tool and by eye; walk the screen with the keyboard only; read it with a screen reader once; check zoom at 200%.
- Report each failure with the criterion number, the element, and the fix.

# Common issues
- Images without text alternatives; icon buttons without a name; low contrast on text and on focus rings; forms without labels or error text; focus lost after a dialog closes.

# Priority fixes
- Order findings by who they block: anything that stops a keyboard or screen reader user from finishing a task comes first.
