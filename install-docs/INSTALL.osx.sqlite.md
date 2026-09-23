# Installing SQLite (OSX)

## 1. Check the built-in version first
macOS ships with SQLite, so you may not need to install anything:
```bash
which sqlite3
sqlite3 --version
```
The system copy is often older than the latest release. Install via Homebrew if you want a newer version or specific features.

## 2. Install Homebrew (if you don't have it)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

## 3. Install SQLite

```bash
brew update
brew install sqlite
```

## 4. Add it to your PATH

The Homebrew formula is "keg-only" because macOS already provides SQLite. Your shell will keep using the system version until you put Homebrew's version first in your PATH.

```bash
echo 'export PATH="/opt/homebrew/opt/sqlite/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

## 5. Verify the installation

```bash
which sqlite3      # should point to the Homebrew path
sqlite3 --version
```

## 6. Try it out

SQLite has no server or service to start. A database is just a file:
```bash
sqlite3 test.db
```
At the `sqlite>` prompt:
```sql
CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT);
INSERT INTO users (name) VALUES ('Alice');
SELECT * FROM users;
.tables
.quit
```

Useful dot-commands: `.help`, `.schema`, `.headers on`, `.mode column`.

## Quick troubleshooting

- **Still seeing the old version** → PATH not updated, or open a new terminal; check with `which sqlite3`.
- **Compiling against SQLite** (e.g. Python or C extensions) → run `brew info sqlite` for the `LDFLAGS`/`CPPFLAGS` to set.
- **Upgrade later** → `brew upgrade sqlite`
- **GUI preferred?** → `brew install --cask db-browser-for-sqlite`
