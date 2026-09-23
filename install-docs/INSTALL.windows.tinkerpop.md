# TinkerPop Installation (Windows)

This is for installing TinkerPop's Gremlin Server yourself on Windows. Our cluster sysadmin is the person to ask about this on the cluster. If you are doing this then, minimally, you will need the ability to stop and start the Gremlin Server. You also need the ability to remove the saved graph file.

Unlike JanusGraph, TinkerPop ships a Windows script for the server (`gremlin-server.bat`), so this runs natively with no WSL needed. The script runs the server in the foreground: it has no `start/stop/status` commands.

By default Gremlin Server uses **TinkerGraph**, an in-memory graph. Step 3 makes it save to disk; skip it if you're happy for the graph to be wiped on every restart.

## 1. Install Java

Gremlin Server supports Java 11 and 17:

```powershell
winget install EclipseAdoptium.Temurin.17.JRE
```

Open a new PowerShell window, then check:

```powershell
java -version
```

## 2. Download and install Gremlin Server

3.8.2 is the current stable release; check <https://tinkerpop.apache.org/download.html> for newer ones.

```powershell
cd C:\
Invoke-WebRequest -Uri https://archive.apache.org/dist/tinkerpop/3.8.2/apache-tinkerpop-gremlin-server-3.8.2-bin.zip -OutFile gremlin-server.zip
Expand-Archive gremlin-server.zip -DestinationPath C:\
Rename-Item C:\apache-tinkerpop-gremlin-server-3.8.2 C:\gremlin-server
```

## 3. Make the graph persistent (optional)

```powershell
New-Item -ItemType Directory -Force C:\tinkerpop-data
```

Edit `C:\gremlin-server\conf\tinkergraph-empty.properties` and add (use forward slashes):

```properties
gremlin.tinkergraph.graphLocation=C:/tinkerpop-data/graph.json
gremlin.tinkergraph.graphFormat=graphson
```

**Important:** TinkerGraph only writes this file when the server shuts down cleanly (Ctrl+C in the server window). If you close the window with the X, end the process in Task Manager, or Windows crashes, changes since the last clean shutdown are lost.

## 4. Start Gremlin Server

```powershell
cd C:\gremlin-server
bin\gremlin-server.bat conf\gremlin-server.yaml
```

Leave this window open; the server runs in the foreground.

The Windows script uses only 512 MB of heap by default. To give it more, set `JAVA_ARGS` in the same window before starting:

```powershell
$env:JAVA_ARGS = "-Xmx2g"
```

In a second PowerShell window, check it's running on port 8182:

```powershell
Get-NetTCPConnection -LocalPort 8182 -State Listen
```

Windows Firewall may prompt you to allow Java network access the first time; allowing private networks is enough for local use.

## 5. Verify with Gremlin console

The console is a separate download:

```powershell
cd C:\
Invoke-WebRequest -Uri https://archive.apache.org/dist/tinkerpop/3.8.2/apache-tinkerpop-gremlin-console-3.8.2-bin.zip -OutFile gremlin-console.zip
Expand-Archive gremlin-console.zip -DestinationPath C:\
Rename-Item C:\apache-tinkerpop-gremlin-console-3.8.2 C:\gremlin-console
```

# To access the console

```powershell
cd C:\gremlin-console
bin\gremlin.bat
```

and at the prompt

```groovy
:remote connect tinkerpop.server conf/remote.yaml
:remote console
g.V().count()  // should return 0 on a fresh install
```

# To start/stop the service

- **Start:** `cd C:\gremlin-server` then `bin\gremlin-server.bat conf\gremlin-server.yaml`
- **Stop:** press `Ctrl+C` in the server window.
- **Status:** `Get-NetTCPConnection -LocalPort 8182 -State Listen`

# To reset the saved graph

Stop the server first with `Ctrl+C` (otherwise it rewrites the file on shutdown), then delete the file and start it again:

```powershell
Remove-Item C:\tinkerpop-data\graph.json
```
