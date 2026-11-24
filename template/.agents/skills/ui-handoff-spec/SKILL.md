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

# States and edge cases
- For every interactive element: default, hover or focus, pressed, disabled, loading, error, empty.
- Edge cases: very long text, no data, offline, slow network, permission denied, right-to-left layout.

# Responsive behaviour
- Breakpoints the layout changes at, and what collapses, stacks or hides at each one.

# Motion
- Duration, easing, and the behaviour when the user has reduced motion enabled.

# Content specifications
- Real text for every label, empty state and error, with its length limits and the translation space it needs.
