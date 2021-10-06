# Contributing

## Git

### Commit messages
```
type(scope): Message

details
```

- Example:
```
feat(unpacker): Support for pkg archive

Added support for firmwares that are archived in pkg format
```

The first line should be <= 72 chars long, since after 72 chars GitHub breaks the line and puts a `...` button on the side. For messages longer you add a `\n` and write more details on the next line after that.

Preferably first line should be <= 50 chars for readability purposes, but that’s not required at this time.

#### Types
- `build`: Changes that affect the build system or external dependencies.
- `chore`: Other changes that don’t modify src or test files.
- `ci`: Changes to our CI configuration files and scripts.
- `copy`: Copy update.
- `docs`: Documentation only changes.
- `feat`: A new feature. Can of course also contain tests for the feature.
- `fix`: Bug fixes. Can of course also contain tests for the feature.
- `log`: Add logging if we want to gather some insights.
- `perf`: A code change that improves performance.
- `refactor`: A code change that neither fixes a bug nor adds a feature.
- `revert`: Reverts a previous commit.
- `style`: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc).
- `test`: Adding missing tests or correcting existing tests.

