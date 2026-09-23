# Installing PostgreSQL (OSX)

## 1. Install Homebrew (if you don't have it)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
Then check it works:
```bash
brew --version
```

## 2. Install PostgreSQL
Homebrew ships versioned formulae. See what's available, then install the one you want:
```bash
brew update
brew search postgresql
brew install postgresql@18   # swap 18 for the version you need
```

## 3. Add it to your PATH
Versioned formulae are "keg-only", so the binaries aren't linked automatically.

**Apple Silicon (M-series):**
```bash
echo 'export PATH="/opt/homebrew/opt/postgresql@18/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**Intel Mac:**
```bash
echo 'export PATH="/usr/local/opt/postgresql@18/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

## 4. Start the service
```bash
brew services start postgresql@18   # start now and on login
brew services list                  # check status
```
To stop or restart:
```bash
brew services stop postgresql@18
brew services restart postgresql@18
```

## 5. Verify the installation
```bash
psql --version
psql postgres
```
Homebrew creates a superuser matching your **macOS username** with no password. At the `postgres=#` prompt:
```sql
SELECT version();
\q
```

## 6. Optional setup
Create a database named after your user, so plain `psql` connects without arguments:
```bash
createdb
```
Create a `postgres` superuser role (many tools and tutorials expect it):
```bash
createuser -s postgres
```

## 7. Create the `ssrepi` user and database
Connect as your superuser (your macOS username):
```bash
psql postgres
```
Create the user with a password and permission to create databases, then create the `ssrepi` database owned by that user:
```sql
CREATE ROLE ssrepi WITH LOGIN PASSWORD 'choose-a-strong-password' CREATEDB;
CREATE DATABASE ssrepi OWNER ssrepi;
\q
```
Because `ssrepi` owns the database, it can alter and drop it, and create tables in its `public` schema. `CREATEDB` also lets it create new databases (and drop any it owns).

Test the new login:
```bash
psql -U ssrepi -d ssrepi
```
Note that Homebrew's default setup uses **trust** authentication for local connections, so you won't be asked for the password. To require it, edit `pg_hba.conf` in the data directory (`/opt/homebrew/var/postgresql@18` on Apple Silicon, `/usr/local/var/postgresql@18` on Intel), change `trust` to `scram-sha-256`, then run `brew services restart postgresql@18`. Set a password for your own superuser first, or you'll lock yourself out.

To delete and recreate the database as `ssrepi`, connect to a different database first (you can't drop the one you're connected to):
```bash
psql -U ssrepi -d postgres
```
```sql
DROP DATABASE ssrepi;
CREATE DATABASE ssrepi;
```
To change the password later: `psql postgres -c "ALTER ROLE ssrepi WITH PASSWORD 'new-password';"`

## Quick troubleshooting
- **`psql: command not found`** → PATH not set, or open a new terminal.
- **`database "<username>" does not exist`** → run `createdb` or connect with `psql postgres`.
- **Connection refused** → service not running; check `brew services list`.
- **Port 5432 in use** → another Postgres (e.g. Postgres.app) is running; stop it first.
- **See logs / install notes** → `brew info postgresql@18`
- **GUI preferred?** → `brew install --cask pgadmin4`
