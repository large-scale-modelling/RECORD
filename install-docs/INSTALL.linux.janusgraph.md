# Janus Installation (Linux)

This is for installing Janusgraph yourself. Our linux sysadmin is the person to ask about this on the cluster. If you are doing this then, minimally you will need the ability to stop and start the janusgraph server, normally done with `systemctl stop janusgraph.service`. You also need the ability to remove the files for the Berkeley database.

JanusGraph needs Java:

```bash
sudo apt update
sudo apt install -y openjdk-23-jre-headless
java -version
```

2. Download and install JanusGraph

```bash
cd /opt
sudo wget https://github.com/JanusGraph/janusgraph/releases/download/v1.1.0/janusgraph-1.1.0.zip
sudo unzip janusgraph-1.1.0.zip
sudo mv janusgraph-1.1.0 janusgraph
sudo chown -R $USER:$USER /opt/janusgraph
```

3. Configure BerkeleyDB backend

Edit the server config to use BerkeleyDB instead of TinkerGraph:

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

4. 

```bash
sudo mkdir -p /var/lib/janusgraph
sudo chown $USER:$USER /var/lib/janusgraph
```

Edit `/opt/janusgraph/conf/janusgraph-server.properties` and set:

```properties
storage.backend=berkeleyje
storage.directory=/var/lib/janusgraph
```

5. Start JanusGraph
```bash
/opt/janusgraph/bin/janusgraph-server.sh start
```

Check it's running on port 8182:
```bash
ss -tlnp | grep 8182
```

6. Verify with Gremlin console


# To access the console

```bash
/opt/janusgraph/bin/gremlin.sh
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



