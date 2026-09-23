# Installing PostgreSQL on Windows

## 1. Download the installer
- Go to <https://www.postgresql.org/download/windows/>
- Click **Download the installer** (hosted by EDB) and pick the latest version for **Windows x86-64**.

## 2. Run the installer
Accept the defaults unless you have a reason not to:

| Step | Recommendation |
|------|----------------|
| Install directory | `C:\Program Files\PostgreSQL\<version>` |
| Components | PostgreSQL Server, pgAdmin 4, Command Line Tools (Stack Builder is optional) |
| Data directory | Default is fine |
| Superuser password | Set one for the `postgres` user and **write it down** |
| Port | `5432` (default) |
| Locale | Default |

Finish the install. You can skip Stack Builder at the end.

## 3. Add `psql` to your PATH (optional but handy)
1. Open **Start → "Edit the system environment variables" → Environment Variables**.
2. Under **System variables**, edit `Path` and add:
   `C:\Program Files\PostgreSQL\<version>\bin`
3. Open a new terminal window.

## 4. Verify the installation
```powershell
psql --version
psql -U postgres
```
Enter your superuser password. At the `postgres=#` prompt, try:
```sql
SELECT version();
\q
```

## 5. Check the service
PostgreSQL runs as a Windows service and starts automatically.
- Open **services.msc** and look for `postgresql-x64-<version>`, or
- In PowerShell: `Get-Service postgresql*`

## 6. Create the `ssrepi` user and database
Connect as the superuser:
```powershell
psql -U postgres
```
Create the user with a password and permission to create databases, then create the `ssrepi` database owned by that user:
```sql
CREATE ROLE ssrepi WITH LOGIN PASSWORD 'choose-a-strong-password' CREATEDB;
CREATE DATABASE ssrepi OWNER ssrepi;
\q
```
Because `ssrepi` owns the database, it can alter and drop it, and create tables in its `public` schema. `CREATEDB` also lets it create new databases (and drop any it owns).

Test the new login:
```powershell
psql -U ssrepi -d ssrepi
```
To delete and recreate the database as `ssrepi`, connect to a different database first (you can't drop the one you're connected to):
```powershell
psql -U ssrepi -d postgres
```
```sql
DROP DATABASE ssrepi;
CREATE DATABASE ssrepi;
```
To change the password later (as `postgres`): `ALTER ROLE ssrepi WITH PASSWORD 'new-password';`

## Alternative: install via winget
```powershell
winget search PostgreSQL
winget install PostgreSQL.PostgreSQL.<version>
```

## Quick troubleshooting
- **`psql` not recognized** → PATH not set, or terminal not restarted.
- **Password authentication failed** → wrong password for `postgres`; reset via `pg_hba.conf` if forgotten.
- **Port 5432 in use** → another Postgres instance is running; stop it or pick a different port.
- **GUI preferred?** → use **pgAdmin 4** from the Start menu.
