# TinkerPop Installation (OSX)

This is for installing TinkerPop's Gremlin Server yourself on a Mac. Our cluster sysadmin is the person to ask about this on the cluster. If you are doing this then, minimally, you will need the ability to stop and start the Gremlin Server (`gremlin-server.sh stop` / `start`, see the end of this note). You also need the ability to remove the saved graph file.

By default Gremlin Server uses **TinkerGraph**, an in-memory graph. Step 3 makes it save to disk; skip it if you're happy for the graph to be wiped on every restart.

## 1. Install Java

Gremlin Server supports Java 11 and 17. The easiest route is Homebrew (install it from <https://brew.sh> if you don't have it):

```bash
brew install --cask temurin@17
java -version
```

## 2. Download and install Gremlin Server

3.8.2 is the current stable release; check <https://tinkerpop.apache.org/download.html> for newer ones.

```bash
sudo mkdir -p /opt
cd /opt
sudo curl -LO https://archive.apache.org/dist/tinkerpop/3.8.2/apache-tinkerpop-gremlin-server-3.8.2-bin.zip
sudo unzip apache-tinkerpop-gremlin-server-3.8.2-bin.zip
sudo mv apache-tinkerpop-gremlin-server-3.8.2 gremlin-server
sudo chown -R $USER:staff /opt/gremlin-server
```

Optionally, add the scripts to your PATH so you can run them from anywhere:

```bash
echo 'export PATH="/opt/gremlin-server/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

## 3. Make the graph persistent (optional)

```bash
sudo mkdir -p /opt/tinkerpop-data
sudo chown $USER:staff /opt/tinkerpop-data
```

Edit `/opt/gremlin-server/conf/tinkergraph-empty.properties` and add:

```properties
gremlin.tinkergraph.graphLocation=/opt/tinkerpop-data/graph.json
gremlin.tinkergraph.graphFormat=graphson
```

**Important:** TinkerGraph only writes this file when the server shuts down cleanly (`gremlin-server.sh stop` or Ctrl+C). If the process is killed or your Mac crashes, changes since the last clean shutdown are lost.

## 4. Start Gremlin Server

```bash
/opt/gremlin-server/bin/gremlin-server.sh start
```

Check it's running on port 8182 (macOS has no `ss`, so use `lsof`):

```bash
lsof -iTCP:8182 -sTCP:LISTEN
```

The server asks for up to 4 GB of heap by default. To change it, set `JAVA_OPTIONS` before starting, e.g. `export JAVA_OPTIONS="-Xms512m -Xmx2g"`. Logs are in `/opt/gremlin-server/logs/`.

## 5. Verify with Gremlin console

The console is a separate download:

```bash
cd /opt
sudo curl -LO https://archive.apache.org/dist/tinkerpop/3.8.2/apache-tinkerpop-gremlin-console-3.8.2-bin.zip
sudo unzip apache-tinkerpop-gremlin-console-3.8.2-bin.zip
sudo mv apache-tinkerpop-gremlin-console-3.8.2 gremlin-console
sudo chown -R $USER:staff /opt/gremlin-console
```

# To access the console

```bash
cd /opt/gremlin-console
bin/gremlin.sh
```

and at the prompt

```groovy
:remote connect tinkerpop.server conf/remote.yaml
:remote console
g.V().count()  // should return 0 on a fresh install
```

# To start/stop the service

```bash
gremlin-server.sh start
gremlin-server.sh stop
gremlin-server.sh status
gremlin-server.sh restart
```

(Use the full path `/opt/gremlin-server/bin/gremlin-server.sh` if you didn't add it to your PATH.)

# To reset the saved graph

Stop the server first (otherwise it rewrites the file on shutdown), then delete the file and start it again:

```bash
gremlin-server.sh stop
rm -f /opt/tinkerpop-data/graph.json
gremlin-server.sh start
```
