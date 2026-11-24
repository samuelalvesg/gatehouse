# Profiles

A profile is a ready-made set of agents and skills for a kind of repository. Install one instead of the generic `template/`:

```bash
./install.sh /path/to/project --profile flutter-app
./install.sh /path/to/project --profile flutter-app --check   # lists what drifted
```

| Profile | Layers | For |
|---|---|---|
| `code-repo` | `code-common` | A code repository in any stack: the generic agents and skills |
| `dart-package` | `dart-base` | A Dart or Flutter package, with the team pointer in `.claude/TEAM.md` |
| `flutter-app` | `dart-base`, `flutter-ui` | A Flutter app: the Dart layer plus design-system, accessibility and UI handoff skills |

## How it is built

A profile is a folder with a `LAYERS` file that lists layer names in order, one per line. A layer is a folder with a `root/` that mirrors the target repository. Later layers win. To add a profile, add a folder with a `LAYERS` file, and a layer folder if you need new files.

`--check` copies nothing. It lists files that are missing or different in the target, and agents or skills in the target that the profile does not know, and exits 1 if there is any difference. `tests/validate.sh` runs it against every profile.
