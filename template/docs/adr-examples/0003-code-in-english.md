# 0003 - New code and comments are in English

**Status:** Example

## Context

The team works in one language and the code is read by people and by AI agents who work better in English. Existing code in another language is large, and renaming it all at once would bury real changes in noise.

## Decision

1. New code is written in English: names of classes, functions and variables, comments, doc comments, test names and descriptions. This applies to people and to agents.
2. These stay in the user's language: text the user sees (UI and error messages), Markdown documents, commit messages, and public identifiers that other systems rely on (package names, routes, configuration keys).
3. Existing code is not translated in passing. It is translated in its own change, reviewed on its own.
4. Comments say why, not what. History ("this used to be...") belongs in the commit message.

## Consequences

- New code reads the same for everyone and for agents.
- Mixed-language files exist during the migration. Each change that touches one stays small and reviewable.
- The migration needs its own backlog item and its own reviews.
