# Installing SQLite on Linux

## 1. Check whether it's already installed
```bash
which sqlite3
sqlite3 --version
```

## 2. Install SQLite
SQLite is in Debian's standard repositories:
```bash
sudo apt update
sudo apt install sqlite3
```

## 3. Install development headers (optional)
Needed only if you're compiling software against SQLite, such as C extensions or building Python from source:
```bash
sudo apt install libsqlite3-dev
```

## 4. Verify the installation
```bash
which sqlite3      # /usr/bin/sqlite3
sqlite3 --version
```

## 5. Try it out
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

## Note on versions
Debian stable pins SQLite to the version that was current when the release came out, so it can lag behind the latest. This rarely matters. If you need a newer version, check Debian backports or build from source (<https://www.sqlite.org/download.html>).

## Quick troubleshooting
- **`sqlite3: command not found`** → the package isn't installed; run `sudo apt install sqlite3`.
- **`Unable to open database file`** → check you have write permission for the directory the file is in.
- **`sqlite3.h: No such file or directory` when compiling** → install `libsqlite3-dev`.
- **Upgrade later** → `sudo apt update && sudo apt upgrade sqlite3`
- **GUI preferred?** → `sudo apt install sqlitebrowser`
