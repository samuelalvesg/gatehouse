---
name: ux-copy-ptbr
description: UI copy guidelines for Brazilian Portuguese (pt-BR): buttons, errors, empty states, confirmation dialogs, capitalization, punctuation and a human tone. Use when writing or reviewing user-facing text in pt-BR.
---
# Process

1. Load the locale file for the text's language (for pt-BR: `locales/pt-BR.md`).
2. Review each text against the locale rules and against its component type (button, error, empty state, confirmation).
3. Return the result in the output format below.

# Code
- Identifiers and localization keys stay in English (`user_profile.save_changes_button`).
- Visible values go in the locale language, in the project's localization files.
- Before creating a text file, check the mechanism the package already uses (`intl`, a strings file).

# Output format
`ELEMENT | text | note`

Give at most three alternatives, and only when tone is the user's decision.
