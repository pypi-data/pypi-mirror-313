# TTXT_V2
**Mission**: Enable clients to effortless connect and interact with crypto exchanges
while not compromising on performance and cutomizability for experienced users. 
**Goals**: Some of our goal are:
1. To provide a library with solid defaults on which people can rely to run application 
writing minimal amount of code. 
2. To create a declarative style of configuration and computation to allow for complex 
data pipelines or strategies to be created using the library as a base.
3. To provide customizable message passing interface to which clients can extend.
4. To provide a standardized APIs to handle different types of `market` and `private` data.

## High-Level System Design
The high-level design has 2 important components.
1. Connector - This is developed and managed by the library.
2. Message Queue - Interfaces are provided by the library and a useful default `async queue`.
3. Client - This is the user code `NOT` managed by the library.
![High-Level Design](./images/ttxt_v2_design.svg)

### Connector Component
The connector is the gateway to exchanges. It gives the users the ability to collect
market data via `WebSocket API` and `REST API`. It is also extensible and users and
create their custom connectors if needed. The connector is responsible for providing
the client standardized messages. So when a messaage is received via any protocol the
connector will parse it and standardize it. On error a descriptive error will be returned
to the client.

### Message Queue Component
This is an extensible inteface that allows users of the library to specify how they want
to pass and receive their messages. We provide a **high-performance** asynchronous queue
using `asyncio`. Clients can customize the Queue interface and hook their custom pubsubs
like `Kafka`, `Redis`, etc. The library also provides abstraction for: `IQueueConsumer`,
`IQueuePublisher`, and `IQueueActor` which combines the before mentioned concepts. These
are other customization points for the user. We as library authors have provided default
implementations using the **async queue**.

### Client
This is the code that is managed by `you` the user. We have provided example clients
using the library bootstrapper to showcase how the library and events can be used.


## Architecture
Here is a simplified view of the different interfaces, customization points and events 
in the library.
![High-Level Design](./images/ttxt_v2_architecture.svg)

### Events
This is the standardized format that connectors forward events to clients and how clients
can communicate with connectors.

Here is a list of the `public market data` events the connector provides.
1. `Orderbook` - standardized format for snapshots and deltas. We provide APIs that allow you to
maintain active orderbook with a single `update` call.
2. `Kline` - standardized format for candle data.
3. `MarketTrades` - standard format for recent market trades event.

Here is a list of the `client communication` events which the clients can send to the connector.
The connector will automatically translate each event into the standardized format into the exchange
specific format.
1. `CreateOrder` - message to either `buy/sell` from the exchange in a standardized format.
2. `CancelOrder` - message to cancel an `active` order.
3. `AmendOrder` - message to modify an `active` order.

Here is a list of other `utlity`, `private`, and `trade events`.
1. `ConnectorStatus` - message to inform the user of the connection status of the connector on the different websockets.
2. `OrderAck` - standardized order acknowledgment event
3. `Wallet` - standardized wallet update event sent over the private API
4. `OrderUpdate` - standardized order update event sent over the private API

It is important to mention that the event system is designed in such a way where users can easily add new custom event.
All they need to do is the following:
- Define the event type and add it to the generic types of `Event`, and `EventLike` in the `event.py` folder.
- Extend the `NormalizerBase`, `IEventHandler` and `DenormalizedBase` interfaces to accomodate for your event type.
- Implement the extended interfaces in the connectors that you use.
- In `BaseClient` check for your new event type and call the event handler.




### Queue Interfaces
The queue interfaces are public and allow users to extend them for their custom message queue where the connectors will
send the messages to.
1. `IQueue` - This is the interface for queue implementation. `AsyncioQueue` is th default that we provide for the users but **do not enforce**.
2. `IQueueConsumer` - This interface specifies how clients should consume from an `IQueue`.
3. `IQueuePublisher` - This interface specifies how clients should publish to an `IQueue`.
4. `IQueueActor` - This interface is a composite interface that represent a client that both `publishes` and `consumes` from an `IQueue`.
Connectors can be **optionally** supplied an implementations of the `IQueue` interface for communication with clients.

### Client Interfaces
The client interfaces are meant for building **event-driven** clients that leverage the websocket functionality of the connectors.
1. `IEventHandler` - This interface outlines what events should be hanlded by the client to fully interact with the connectors.
The client may choose which methods to override if they will not use any.
2. `BaseClient` - This is an abstract base class which provides some helper bootstrapping functionality for any event handler.
Particularly reading from an `IQueue` an automatically calling the correct event handler methods.

### Connector Interfaces
1. `NormalizerBase` - This interface specifies how a connector will convert exchange data to standardized event format
2. `DenormalizerBase` - This inteface specified how connectot will convert from standardized event format to exchange format.
3. `ConnectorBase` - This interface implements the `IQueueActor`, `NormalizerBase` and `Denormalizer` base. The abstract class
add more methods for concete connectors to implement but crucially handles all common operations such as: connecting/reconnecting
on every websocket stream. Provides the fluent APIs for: `listening_market_stream`,`listening_private_stream`, and trading.

Each **ConcreteConnector** implement the **ConnectorBase**. The concrete connnectors are usually only data trasnaltors. They do
not perform any functionality apart from getting the data in the correct format either for sending it to the client
or to the exchange itself. The specify how to authenticate, how to preprocess requests, etc.

## Web Internals
Classes for handling network protocols are abstracted wayt from the client code. The low-level details
of parsing JSON framing messages, headers, maintaining a pool of connection, and destroying the connection it done by the library.
The user is supplied with `factory` classes to create and `assitant` classes to access a clean API.

![WebInternals](./images/web_internals.svg)
### WebAssistantFactory
Manages the `Connection Factory` and instantiates the proper assitants for the users.

### ConnectionFactory
Manages the underlying connections and pool for the user. It manages both `websockets` and `http` connection.

### WSAssistant
Provides the user interfacing APIs for interacting with the underlying with the `WebSocketConnetion`.

### WSConnection
Handles all the low-level interactions. Performs message cleanup and build up `WSResponses`. It handles
connections, errors, different frames on the websocket layer and cleanup.

### WSRequest
A generic base class the specifies how a request should be handled by a particular connection. I have 3 concrete classes.
1. `WSJSONRequest` - A request in JSON format.
2. `WSPlainTextRequest` - A request in a plain-text `(string)` format
3. `WSBinaryRequest` - A request in binary `(bytesarray)` format.

### WSResponse
Represents a generic response with a `data` field. The data can be any of the 3 types specified by the `WebSocket Protocol` as in the RFC.

## Market Data Recoder
This is an opt-in feature where clients can enable and all public market data will automatically be recorder for them. Here is
a high-level overview of the design.
![High-Level Design](./images/market_recorder.svg)
As you can see the recorder again communicates with the connector via a message queue. All events are streamed to the recorder
which then batches them into chunks and `appends` them to a file for **each ticker**. To showcase it a bit better I will explain the
following scenrio. The user runs the connector trading `BTC/USDT`. Every market event such as: `Orderbook Snapshot`, `Orderbook delta`,
`Recent trades`, `Klines` will be binary serialized and batched usually into chunks of `150` events. These chunks will then be written
at a location specified by the user which is upplied to the `MarketDataRecorder`. For each ticker the recorder will create (if the file
does not exist) / append to a file called: `<EXCHANGE>_<BASE>_<QUOTE>.bin`. As of right now we have simply a recorder which operates on
files in the local system. In the future this system will be abstracted to allow users to develop and `S3` or even `Hadoop` recorder.

## Market Data Replayer
This is another opt-in feature that will enable users of the library build more complex data simulation pipelines to analyze and replay
the whole or sub-history of the market.
![High-Level Design](./images/market_replayer.svg)
The replayer connects to the location in which the `Recorder` saved the market files. It then reads big chunks of the files into a local
memory buffer to drastically increase performance. The binary data is then deserialized into the normalized events API which the users
should already be accustomed to. The deserialized data is then sent over an abstract queue from which `Consumers` can consume from.
In the future we will try to provide a simple `ExchangeSimulator` class to showcase how backtesting can be done leveraging the
`MarketDataRecorder` and `MarketDataReplayer`. For now you can see a very minimal example in the `exmaples.replayer.replayer.py` file.


## Running the project
This project uses poetry for packaging and environment management.

### Installing Dependencies
```bash
    poetry shell
    poetry install
```

### Running clients
This is how you can run one of our example clients:
```bash
    # python -m example.<client_name> [--c=<config_file>]?
    python -m examples.dummy.dummy_client_example
    # Here is an exmaple with a custom file-path
    python -m examples.dummy.dummy_client_example --c=config.json
```

### Running the tests
This will run all the test note that in order for some of the to pass you need to set proper API_KEY and API_SECRET env variables
for each connector you test.
```bash
    pytest -v tests
```

You can always run a subset of the test using:
```bash
    pytest -v tests/test_bybit_conversion.py
```

