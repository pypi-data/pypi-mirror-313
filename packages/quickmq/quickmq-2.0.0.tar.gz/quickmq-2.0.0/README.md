# QuickMQ

[![pipeline status](https://gitlab.ssec.wisc.edu/mdrexler/ssec_amqp/badges/main/pipeline.svg)](https://gitlab.ssec.wisc.edu/mdrexler/ssec_amqp/-/commits/main) [![coverage report](https://gitlab.ssec.wisc.edu/mdrexler/ssec_amqp/badges/main/coverage.svg)](https://gitlab.ssec.wisc.edu/mdrexler/ssec_amqp/-/commits/main) [![PyPI version shields.io](https://img.shields.io/pypi/v/quickmq.svg)](https://pypi.python.org/pypi/quickmq/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/quickmq.svg)](https://pypi.python.org/pypi/quickmq/)

An easy-to-use AMQP/RabbitMQ publisher created for use at the SSEC.

## Description

QuickMQ provides a high-level API to simplify common publishing patterns, which allows event processors at SDS to focus on processing events instead of handling network problems.

- Automatically reconnect and handle errors.
- Publishing to multiple servers at once.
- Guaranteeing message delivery.
- Publishing messages to a RabbitMQ cluster.

To see the requirements of this project check out the [reqs and specs doc](/docs/reqs-and-specs.md).

Please note that QuickMQ cannot currently do the following.

- Declare AMQP 0-9-1 topology (exchanges, queues).
- Consume messages from a server.

## Installation

### Requirements

- Python >= 3.6

> Note: QuickMQ has only been tested on OSX and RHEL systems.

To install the latest stable version use `pip`.

```bash
pip install --upgrade quickmq
```

In addition to being on [PyPi](https://pypi.org/project/quickmq/), QuickMQ is also deployed to the SSEC's GitLab package registry.

```bash
pip install --upgrade --index-url https://gitlab.ssec.wisc.edu/api/v4/projects/2625/packages/pypi/simple quickmq
```

To install the latest (possibly unstable) developer version use `git`.

```bash
git clone https://gitlab.ssec.wisc.edu/mdrexler/ssec_amqp.git
cd ssec_amqp
pip install .
```

## Usage

### API

The easiest way to use QuickMQ is with the API at `ssec_amqp.api`.

```python3
import ssec_amqp.api as mq

# Connect to multiple servers at once
mq.connect('server1', 'server2', user='username', password='password', exchange='satellite')

# Additionally, connect to a RabbitMQ cluster
mq.connect('cluster1', 'cluster2', 'cluster3', user='user', password='pass', exchange='satellite', cluster=True)
```

QuickMQ will now manage the connections to 'server1', 'server2', and the cluster servers until `mq.disconnect()` is called or the program exits. This means that if a connection to a server is interrupted, QuickMQ will automatically retry connecting to that server without interrupting connections to other servers or blocking the calling script.

```python3
# ...continued from above
# Now when we publish messages they'll get delivered to 'server1', 'server2', and one of the cluster servers.
import logging

try:
    while True:
        deliv_status = mq.publish({'msg': 'Hi from QuickMQ!'}, route_key='my.custom.topic')
        for con, stat in deliv_status.items():
            if stat != "DELIVERED":
                logging.warning("Couldn't deliver message to %s!", con)
except KeyboardInterrupt:
    logging.info("goodbye!")
```

`mq.publish` will return a dictionary that contains the status of the message delivery to each server.

- `"DELIVERED"` means that the message was successfully delivered and acknowledged by the server.
- `"DROPPED"` means that the message wasn't sent to the server (because the connection is actively reconnecting).
- `"REJECTED"` means that the message was [nacked](https://www.rabbitmq.com/docs/confirms#server-sent-nacks) by the server.

> Note: QuickMQ will JSON-serialize messages passed to `mq.publish`, so make sure to pass the Python object itself and not a JSON string.

It's possible to see the current connection status for each server using `mq.status`.

```python3
# ...continued from above

con_status = mq.status()
for con, status in con_status.items():
    if status != "CONNECTED":
        logging.warning("Not currently connected to %s!", con)
```

`mq.status` will return a dictionary that contains the connection status to each server. The values are pretty self-explanatory; `"CONNECTED"`, `"RECONNECTING"`, and `"DISCONNECTED"`. Something to keep in mind is `mq.status` won't actively check the connection, so a server with a `"CONNECTED"` status could still fail to publish and then be shown as `"RECONNECTING"`.

### Classes

If the API doesn't provide enough flexibility, it's also possible to use the classes that drive it directly.

```python3
# Recreate the code blocks above without using the API.

import logging

from ssec_amqp import AmqpClient, AmqpConnection, ClusteredConnection

client = AmqpClient(name='my_client') # Optionally give it a name for logging.

servers = ['server1', 'server2']

for server in servers:
    client.connect(AmqpConnection(server, user='user', password='pass', exchange='satellite'))

cluster_servers = ['cluster1', 'cluster2', 'cluster3']

client.connect(ClusteredConnection([AmqpConnection(server, user='user', password='pass') for server in cluster_servers]))

try:
    while True:
        deliv_status = client.publish({'msg': "hi from QuickMQ!'}, route_key='my.custom.topic')
        for con, stat in deliv_status.items():
            if stat != "DELIVERED":
                logging.warning("Couldn't deliver message to %s!", con)
except KeyboardInterrupt:
    pass

con_status = client.connections
for con, status in con_status.items():
    if status != "CONNECTED":
        logging.warning("Not connected to %s!", con)

# Connections won't automatically disconnect when using a custom client
client.disconnect()
```

For more information, see the source code for [the client](/src/ssec_amqp/client.py) and [the connections](/src/ssec_amqp/amqp.py).

## Author

Created/Maintained by [Max Drexler](mailto:mndrexler@wisc.edu).

## License

MIT License. See [LICENSE](/LICENSE) for more information.
