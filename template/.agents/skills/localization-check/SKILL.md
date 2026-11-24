---
name: localization-check
description: Keep translation files complete and consistent with the reference language, add new strings in the right order, and review machine drafts before they ship. Use when a change adds or edits user-facing text, or before a release that ships translations.
---

# Localization check

The reference language file is the source of truth. A string that exists only in a translation is a defect.

## Procedure

1. **Add the string in the reference first.** Every new key is created in the reference file (for example `app_en.arb`), with its description for translators.
2. **Run the check.** `python3 scripts/i18n/check_l10n_completeness.py --dir <folder> --reference <file> --pattern "<pattern>"`. Exit 0 is required before release. A missing key blocks the release; an extra key is removed or justified.
3. **Keep placeholders identical.** Every placeholder (`{name}`, `%s`, plural forms) in a translation appears in the reference with the same name and count. A translation that changes them is a defect.
4. **Machine drafts.** A draft produced by a model or a tool is marked as a draft and reviewed by a person who reads the language before it ships. A draft is never shipped silently.

## Rules

- Do not translate on behalf of the reference: a missing translation is reported, not invented in the code.
- User-facing text keeps the language the product uses; code comments follow the repository's code-language rule.
- When the check cannot run (no reference file, no translation folder), the result is `NOT VERIFIED`, not a pass.
