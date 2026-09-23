# Installing SQLite on Windows

Windows doesn't include the `sqlite3` command-line tool, so you'll need to install it. Pick one of the two options below.

## Option A: install via winget (quickest)
```powershell
winget search SQLite
winget install SQLite.SQLite
```
Open a new terminal window afterwards so the PATH change takes effect.

## Option B: manual install from sqlite.org
1. Go to <https://www.sqlite.org/download.html>.
2. Under **Precompiled Binaries for Windows**, download the **sqlite-tools-win-x64** zip.
3. Create a folder such as `C:\sqlite` and extract the zip into it (you should see `sqlite3.exe`).
4. Add the folder to your PATH:
   - Open **Start → "Edit the system environment variables" → Environment Variables**.
   - Under **System variables**, edit `Path` and add `C:\sqlite`.
5. Open a new terminal window.

## Verify the installation
```powershell
where.exe sqlite3
sqlite3 --version
```

## Try it out
SQLite has no server or service to start. A database is just a file:
```powershell
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
- **`sqlite3` not recognized** → PATH not set, or terminal not restarted.
- **Blocked download or "Windows protected your PC"** → the file came from the internet; right-click the zip → **Properties** → **Unblock** before extracting.
- **Upgrade later** → `winget upgrade SQLite.SQLite`, or replace the files in `C:\sqlite` with a newer download.
- **GUI preferred?** → install DB Browser for SQLite (`winget search "DB Browser for SQLite"`) or download it from <https://sqlitebrowser.org>.
