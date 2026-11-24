---
name: ux-copy-ptbr
description: Brazilian Portuguese (pt-BR) interface copy guidelines (buttons, errors, empty states, confirmation dialogs). Use when writing or reviewing user-facing UI strings for pt-BR locales.
---
# Rules
- Brazilian Portuguese (pt-BR) with full diacritics and correct spelling; never ASCII substitutions ("nao", "acao").
- Consistent terminology: maintain domain vocabulary throughout screens.
- Action-oriented buttons: use clear infinitive verbs ("Salvar alterações", "Criar equipe", not vague "OK", "Enviar").
- Errors: what happened + why (if helpful) + what to do next. Never display raw technical stack traces or internal exception classes to users.
- Empty states: identify what the view represents + explain why it is empty + explain how to begin.
- Confirmations: clearly name the action and its consequences ("Excluir 3 arquivos? Essa ação não pode ser desfeita.").
- Loading states: convey realistic expectations without promising exact seconds.
- Tone: professional, respectful, concise, and helpful.

# Code Convention
- Code identifiers and localization keys MUST be in English (e.g. `user_profile.save_changes_button`).
- User-facing values in pt-BR localization files.

# Output Format
`ELEMENT | localized_copy | notes`

# Additional guidance
- Locale text with **all diacritics** and correct spelling; never ASCII ("nao", "acao"). One term per concept: use `the glossary` and the vocabulary already on the screen.
- Button = verb + clear result ("Salvar alterações", "Criar equipe", not "OK"). **Error** = what happened + why (if useful) + what to do, no technical code/stack. **Empty** = what it is + why empty + how to start. **Confirmation** names the action and the consequence ("Excluir 3 arquivos? Não dá para desfazer." with "Excluir arquivos" / "Manter"). Loading: set expectation, promise no time. Tone neutral and courteous. pt-BR runs ~20–30% longer than English: plan line breaks. Never reveal whether an e-mail exists or internal detail.
- Code: key/identifier in English; visible string in Portuguese; use the app's text mechanism (check for `intl`/strings file in the package before creating one). Output: `ELEMENTO | texto | observação`; ≤3 alternatives only when tone is the user's decision.
