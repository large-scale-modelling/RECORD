# Janus Installation (OSX)

This is for installing JanusGraph yourself on a Mac. Our cluster sysadmin is the person to ask about this on the cluster. If you are doing this then, minimally, you will need the ability to stop and start the JanusGraph server (done with `janusgraph-server.sh stop` / `start`, see the end of this note). You also need the ability to remove the files for the Berkeley database.

## 1. Install Java

JanusGraph needs Java. The easiest route is Homebrew (install it from <https://brew.sh> if you don't have it):

```bash
brew install --cask temurin@17
java -version
```

## 2. Download and install JanusGraph

```bash
sudo mkdir -p /opt
cd /opt
sudo curl -LO https://github.com/JanusGraph/janusgraph/releases/download/v1.1.0/janusgraph-1.1.0.zip
sudo unzip janusgraph-1.1.0.zip
sudo mv janusgraph-1.1.0 janusgraph
sudo chown -R $USER:staff /opt/janusgraph
```

Optionally, add the scripts to your PATH so you can run them from anywhere:

```bash
echo 'export PATH="/opt/janusgraph/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

## 3. Configure BerkeleyDB backend

Edit the server config to use BerkeleyDB instead of the in-memory graph:

```bash
cp /opt/janusgraph/conf/janusgraph-berkeleyje.properties \
   /opt/janusgraph/conf/janusgraph-server.properties
```

Edit `/opt/janusgraph/conf/gremlin-server/gremlin-server.yaml` and change the graphs section:

```yaml
graphs: {
  graph: conf/janusgraph-server.properties
}
```

## 4. Create the data directory

```bash
sudo mkdir -p /opt/janusgraph-data
sudo chown $USER:staff /opt/janusgraph-data
```

Edit `/opt/janusgraph/conf/janusgraph-server.properties` and set:

```properties
storage.backend=berkeleyje
storage.directory=/opt/janusgraph-data
```

## 5. Start JanusGraph

```bash
/opt/janusgraph/bin/janusgraph-server.sh start
```

Check it's running on port 8182 (macOS has no `ss`, so use `lsof`):

```bash
lsof -iTCP:8182 -sTCP:LISTEN
```

The server asks for a 4 GB heap by default. On a Mac with limited memory, lower `-Xms` and `-Xmx` in `/opt/janusgraph/conf/jvm-11.options` (e.g. `-Xms1g` / `-Xmx2g`) and restart. Logs are in `/opt/janusgraph/logs/`.

## 6. Verify with Gremlin console

```bash
cd /opt/janusgraph
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
janusgraph-server.sh start
janusgraph-server.sh stop
janusgraph-server.sh status
```

(Use the full path `/opt/janusgraph/bin/janusgraph-server.sh` if you didn't add it to your PATH.)

# To reset the Berkeley database

Stop the server first, then delete the data files and start it again:

```bash
janusgraph-server.sh stop
rm -rf /opt/janusgraph-data/*
janusgraph-server.sh start
```
