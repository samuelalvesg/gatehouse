---
name: ui-handoff-spec
description: Generates UI/UX handoff specifications for frontend developers, mapping components, interaction states, responsive layouts, design tokens, and error handling.
---
# Specification Checklist
1. **Component Hierarchy**: Breakdown of layout widgets, atomic components, and reusable UI elements.
2. **Design Tokens & Theme**: Colors, typography scales, spacing units (margins, paddings), and border radii.
3. **Component States**:
   - Default / Idle
   - Hover / Focus / Pressed
   - Loading / Skeleton
   - Error (inline validation + toast/banner)
   - Empty state
4. **Responsive Layout & Adaptability**:
   - Breakpoints (mobile, tablet, desktop).
   - Overflow and text wrapping behaviors.
5. **Accessibility (a11y)**:
   - Tap target sizes, contrast ratios, semantics labels, and focus traversal.

# Output Format
Structured markdown specification with component diagrams and property mappings ready for implementation.

# Additional guidance
- Use the app's tokens/theme, not loose values (`grep` the package theme first; do not create a parallel token).
- Screen checklist: states (loading · empty · error · offline · no permission · partial/ok · disabled); content (character limits, truncation, missing data, long pt-BR text, numbers/dates/time zone); responsive (phone, tablet, desktop/web); interaction (touch/click, focus/keyboard, gesture, shortcuts, feedback, animation respecting reduced motion); data (which provider/endpoint; offline and sync conflict); permission (roles from the glossary); a11y → `a11y-audit`; text → `ux-copy-ptbr`; reuse (existing widgets it uses vs. what is really new).
- Output: `## Spec` section (Gherkin from `bdd-spec-writer`) + table `element | state | behavior | token/widget`. No invented mockups: if the design is missing, ask the user.
