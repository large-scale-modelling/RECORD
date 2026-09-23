# TinkerPop Installation (Debian)

This is for installing TinkerPop's Gremlin Server yourself. The cluster sysadmin is the person to ask about this on the cluster. If you are doing this then, minimally, you will need the ability to stop and start the Gremlin Server (`gremlin-server.sh stop` / `start`, or `systemctl` if you set up the service in step 8). You also need the ability to remove the saved graph file.

By default Gremlin Server uses **TinkerGraph**, an in-memory graph. Step 3 makes it save to disk; skip it if you're happy for the graph to be wiped on every restart.

## 1. Install Java

Gremlin Server supports Java 11 and 17:

```bash
sudo apt update
sudo apt install -y openjdk-17-jre-headless
java -version
```

If `openjdk-17-jre-headless` isn't available (e.g. on Debian 13), install Temurin 17 from the Adoptium repo instead:

```bash
sudo apt install -y wget gpg
wget -qO - https://packages.adoptium.net/artifactory/api/gpg/key/public | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/adoptium.gpg > /dev/null
echo "deb https://packages.adoptium.net/artifactory/deb $(awk -F= '/^VERSION_CODENAME/{print$2}' /etc/os-release) main" | sudo tee /etc/apt/sources.list.d/adoptium.list
sudo apt update
sudo apt install -y temurin-17-jre
```

## 2. Download and install Gremlin Server

3.8.2 is the current stable release; check <https://tinkerpop.apache.org/download.html> for newer ones.

```bash
sudo apt install -y unzip
cd /opt
sudo wget https://archive.apache.org/dist/tinkerpop/3.8.2/apache-tinkerpop-gremlin-server-3.8.2-bin.zip
sudo unzip apache-tinkerpop-gremlin-server-3.8.2-bin.zip
sudo mv apache-tinkerpop-gremlin-server-3.8.2 gremlin-server
sudo chown -R $USER:$USER /opt/gremlin-server
```

## 3. Make the graph persistent (optional)

```bash
sudo mkdir -p /var/lib/tinkerpop
sudo chown $USER:$USER /var/lib/tinkerpop
```

Edit `/opt/gremlin-server/conf/tinkergraph-empty.properties` and add:

```properties
gremlin.tinkergraph.graphLocation=/var/lib/tinkerpop/graph.json
gremlin.tinkergraph.graphFormat=graphson
```

**Important:** TinkerGraph only writes this file when the server shuts down cleanly (`gremlin-server.sh stop`, Ctrl+C or `systemctl stop`). If the process is killed or the machine crashes, changes since the last clean shutdown are lost.

## 4. Allow remote connections (optional)

The default config only listens on `localhost`. To connect from other machines, edit `/opt/gremlin-server/conf/gremlin-server.yaml` and change:

```yaml
host: 0.0.0.0
```

## 5. Start Gremlin Server

```bash
/opt/gremlin-server/bin/gremlin-server.sh start
```

Check it's running on port 8182:

```bash
ss -tlnp | grep 8182
```

The server asks for up to 4 GB of heap by default. To change it, set `JAVA_OPTIONS` before starting, e.g. `export JAVA_OPTIONS="-Xms512m -Xmx2g"`. Logs are in `/opt/gremlin-server/logs/`.

## 6. Update your Python connection

Install the driver if you haven't already (`pip install gremlinpython`). The default config exposes the traversal source as `g`:

```python
from gremlin_python.driver import client
conn = client.Client('ws://localhost:8182/gremlin', 'g')
```

## 7. Verify with Gremlin console

The console is a separate download:

```bash
cd /opt
sudo wget https://archive.apache.org/dist/tinkerpop/3.8.2/apache-tinkerpop-gremlin-console-3.8.2-bin.zip
sudo unzip apache-tinkerpop-gremlin-console-3.8.2-bin.zip
sudo mv apache-tinkerpop-gremlin-console-3.8.2 gremlin-console
sudo chown -R $USER:$USER /opt/gremlin-console
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
/opt/gremlin-server/bin/gremlin-server.sh start
/opt/gremlin-server/bin/gremlin-server.sh stop
/opt/gremlin-server/bin/gremlin-server.sh status
/opt/gremlin-server/bin/gremlin-server.sh restart
```

## 8. Run as a systemd service (optional)

To manage it with `systemctl` like the JanusGraph install, create `/etc/systemd/system/gremlin-server.service` (replace `youruser` with the account that owns `/opt/gremlin-server`):

```ini
[Unit]
Description=TinkerPop Gremlin Server
After=network.target

[Service]
Type=simple
User=youruser
ExecStart=/opt/gremlin-server/bin/gremlin-server.sh console
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Then:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now gremlin-server.service
sudo systemctl status gremlin-server.service
```

Use either `systemctl` or `gremlin-server.sh start/stop`, not both.

# To reset the saved graph

Stop the server first (otherwise it rewrites the file on shutdown), then delete the file and start it again:

```bash
/opt/gremlin-server/bin/gremlin-server.sh stop
rm -f /var/lib/tinkerpop/graph.json
/opt/gremlin-server/bin/gremlin-server.sh start
```
