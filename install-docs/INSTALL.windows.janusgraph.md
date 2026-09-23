# Janus Installation (Windows)

This is for installing JanusGraph yourself on Windows. The cluster sysadmin is the person to ask about this on the cluster. If you are doing this then, minimally, you will need the ability to stop and start the JanusGraph server. You also need the ability to remove the files for the Berkeley database.

**Important:** JanusGraph 1.1.0 ships its server start/stop script (`janusgraph-server.sh`) only as a bash script; there is no Windows `.bat` equivalent for the server. You have two options:

- **Option A (recommended): WSL2.** Run Debian inside Windows and follow the Linux instructions unchanged. This is the setup the official scripts support.
- **Option B: native Windows.** Start the server directly with `java` from PowerShell. This works but is less tested, and you lose the `start/stop/status` script.

---

# Option A: WSL2 (recommended)

## 1. Install WSL with Debian

In an **administrator** PowerShell:

```powershell
wsl --install -d Debian
```

Restart if prompted, then open **Debian** from the Start menu and create your Linux user.

## 2. Follow the Linux instructions

Inside the Debian terminal, follow `INSTALL_linux_janusgraph.md` from the Java step onwards.

Notes for WSL:
- `localhost:8182` inside WSL is reachable from Windows as `localhost:8182`, so the Python code in step 6 works from either side.
- If `systemctl` isn't available in WSL, just use `janusgraph-server.sh start/stop/status`, which works without systemd.
- Keep the Berkeley data directory (`/var/lib/janusgraph`) inside the Linux filesystem, not under `/mnt/c/`, for performance and file-locking reliability.

---

# Option B: native Windows

## 1. Install Java

```powershell
winget install EclipseAdoptium.Temurin.17.JRE
```

Open a new PowerShell window, then check:

```powershell
java -version
```

## 2. Download and install JanusGraph

```powershell
cd C:\
Invoke-WebRequest -Uri https://github.com/JanusGraph/janusgraph/releases/download/v1.1.0/janusgraph-1.1.0.zip -OutFile janusgraph-1.1.0.zip
Expand-Archive janusgraph-1.1.0.zip -DestinationPath C:\
Rename-Item C:\janusgraph-1.1.0 C:\janusgraph
```

## 3. Configure BerkeleyDB backend

Edit the server config to use BerkeleyDB instead of the in-memory graph:

```powershell
Copy-Item C:\janusgraph\conf\janusgraph-berkeleyje.properties `
          C:\janusgraph\conf\janusgraph-server.properties
```

Edit `C:\janusgraph\conf\gremlin-server\gremlin-server.yaml` and change the graphs section:

```yaml
graphs: {
  graph: conf/janusgraph-server.properties
}
```

## 4. Create the data directory

```powershell
New-Item -ItemType Directory -Force C:\janusgraph-data
```

Edit `C:\janusgraph\conf\janusgraph-server.properties` and set (use forward slashes):

```properties
storage.backend=berkeleyje
storage.directory=C:/janusgraph-data
```

## 5. Start JanusGraph

From PowerShell, run the server directly with Java (this is what `janusgraph-server.sh` does under the hood):

```powershell
cd C:\janusgraph
java "-Dlog4j2.configurationFile=file:conf/log4j2-server.xml" -Xms1g -Xmx4g `
     "-javaagent:lib/jamm-0.3.3.jar" `
     -cp "conf;lib/*" `
     org.janusgraph.graphdb.server.JanusGraphServer conf/gremlin-server/gremlin-server.yaml
```

Leave this window open; the server runs in the foreground. Lower `-Xmx` if your machine is short on memory.

In a second PowerShell window, check it's running on port 8182:

```powershell
Get-NetTCPConnection -LocalPort 8182 -State Listen
```

Windows Firewall may prompt you to allow Java network access the first time; allowing private networks is enough for local use.

## 6. Verify with Gremlin console

The console does have a Windows script:

```powershell
cd C:\janusgraph
bin\gremlin.bat
```

and at the prompt

```groovy
:remote connect tinkerpop.server conf/remote.yaml
:remote console
g.V().count()  // should return 0 on a fresh install
```

# To start/stop the service (native Windows)

- **Start:** run the `java` command from step 5.
- **Stop:** press `Ctrl+C` in the server window.
- **Status:** `Get-NetTCPConnection -LocalPort 8182 -State Listen`

# To reset the Berkeley database (native Windows)

Stop the server first, then delete the data files and start it again:

```powershell
Remove-Item C:\janusgraph-data\* -Recurse -Force
```
