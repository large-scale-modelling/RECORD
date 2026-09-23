# Installing PostgreSQL (Linux)

## 1. Choose your source
- **Debian's own repo**: simplest; gives you the version bundled with your Debian release.
- **PostgreSQL's official apt repo (PGDG)**: gives you the latest major versions. Use this if you need a newer release.

## 2a. Install from Debian's repo
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

## 2b. Or install the latest version from the PGDG repo
```bash
sudo apt install -y postgresql-common
sudo /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh
sudo apt update
sudo apt install postgresql        # or a specific version, e.g. postgresql-18
```

## 3. Check the service
The installer creates a cluster and starts it automatically:
```bash
sudo systemctl status postgresql
sudo systemctl enable postgresql    # start on boot (usually already enabled)
pg_lsclusters                       # shows version, port and status
```
Other controls: `sudo systemctl start|stop|restart postgresql`

## 4. Verify the installation
On Debian, the `postgres` superuser uses **peer authentication** (it trusts the Linux `postgres` account), so no password is needed:
```bash
sudo -u postgres psql
```
At the `postgres=#` prompt:
```sql
SELECT version();
\q
```

## 5. Create the `ssrepi` user and database
Connect as the superuser:
```bash
sudo -u postgres psql
```
Create the user with a password and permission to create databases, then create the `ssrepi` database owned by that user:
```sql
CREATE ROLE ssrepi WITH LOGIN PASSWORD 'choose-a-strong-password' CREATEDB;
CREATE DATABASE ssrepi OWNER ssrepi;
\q
```
Because `ssrepi` owns the database, it can alter and drop it, and create tables in its `public` schema. `CREATEDB` also lets it create new databases (and drop any it owns).

Test the new login. Use `-h localhost` so it connects over TCP with password auth (a plain local socket connection would try peer auth and fail unless a Linux user called `ssrepi` exists):
```bash
psql -h localhost -U ssrepi -d ssrepi
```
To delete and recreate the database as `ssrepi`, connect to a different database first (you can't drop the one you're connected to):
```bash
psql -h localhost -U ssrepi -d postgres
```
```sql
DROP DATABASE ssrepi;
CREATE DATABASE ssrepi;
```
To change the password later: `sudo -u postgres psql -c "ALTER ROLE ssrepi WITH PASSWORD 'new-password';"`

## 6. Config file locations (optional)
Config lives in `/etc/postgresql/<version>/main/`:
- `postgresql.conf`: settings such as `listen_addresses` and `port`
- `pg_hba.conf`: who can connect and how they authenticate

For remote access, set `listen_addresses = '*'` in `postgresql.conf`, add a `host` line for your network in `pg_hba.conf`, then `sudo systemctl restart postgresql`. Open port 5432 in your firewall only if you need it.

## Quick troubleshooting
- **`Peer authentication failed for user "ssrepi"`** → add `-h localhost` to use password auth.
- **`psql: command not found`** → install the client: `sudo apt install postgresql-client`.
- **Connection refused** → service not running; check `sudo systemctl status postgresql` and `pg_lsclusters`.
- **Port 5432 in use** → another cluster is running; `pg_lsclusters` shows each cluster's port.
- **Logs** → `/var/log/postgresql/`
