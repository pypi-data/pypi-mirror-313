
# Huddle01 Python SDK

## Overview

The Huddle01 Python SDK provides a comprehensive solution for interacting with Huddle01's infrastructure. It enables developers to build real-time communication systems with support for rooms, peers, active speakers, permissions, and WebSocket-based connections.

## Features

- **Access Token Management**: Generate and manage access tokens for secure communication.
- **Room Management**: Create and manage rooms with various permissions and roles.
- **Local and Remote Peers**: Define and manage local and remote peers, including their producers and roles.
- **WebSocket Communication**: Connect to Huddle01's WebSocket server for real-time data exchange.
- **Enhanced Event Handling**: Utilize `EnhancedEventEmitter` for subscribing and handling events seamlessly.
- **Active Speaker Tracking**: Manage active speakers within a room.
- **Produce and Consume Media**: Produce and consume media tracks like video, audio, and screen sharing.

## Installation

To use the SDK, install it via pip:

```bash
pip install huddle01
```

## Getting Started

Here's a quick example to get started:

### 1. Create an Access Token
Generate an access token using your API key and room ID.

```python
from huddle01.access_token import AccessToken, AccessTokenData, Role

data = AccessTokenData(
    api_key="your_api_key",
    room_id="room_id",
    role=Role.HOST
)
token = AccessToken(data)

jwt_token = await token.to_jwt()
```

### 2. Initialize the Huddle Client
Connect to a room using the generated token.

```python
from huddle01.huddle_client import HuddleClient, HuddleClientOptions

options = HuddleClientOptions(autoConsume=True)
client = HuddleClient(project_id="project_id", options=options)

room = await client.create(room_id="room_id", token=jwt_token)
```

### 3. Work with Peers and Rooms
Manage peers, producers, and permissions.

```python
# Example: Access the local peer
local_peer = room.local_peer

# Example: List remote peers
remote_peers = room.remote_peers
```

### 4. Produce and Consume Media
Produce and consume tracks like video, audio, or screen.

#### Producing Media
To produce media, use the `LocalPeer.produce()` method.

```python
track = "video_track"  # Replace with the actual media track
producer = await local_peer.produce(track)
```

#### Consuming Media
To consume media from a remote peer, use the `LocalPeer.consume()` method.

```python
producer_id = "producer_id"  # Replace with the actual producer ID
consumer = await local_peer.consume(producer_id)
```

##### Auto-Consuming Media
To automatically consume media from all producers, set the `autoConsume` option to `True`.

```python
options = HuddleClientOptions(autoConsume=True)
client = HuddleClient(project_id="project_id", options=options)

room = await client.create(room_id="room_id", token=jwt_token)
```

### 5. Close the Connection
Always close the connection when done.

```python
await client.close()
```

## Modules

### 1. `access_token`
Manages access tokens, including permissions and roles.

### 2. `huddle_client`
Main entry point for connecting to the Huddle01 infrastructure. Manages rooms, peers, and communication.

### 3. `room`
Defines the structure and management of rooms.

### 4. `remote_peer`
Handles remote peers connected to a room.

### 5. `socket`
Manages WebSocket connections with advanced features like reconnection.


## Classes and Functions

### `AccessToken`
- `to_jwt()`: Generates a JWT token for authentication.

### `HuddleClient`
- `create(room_id: str, token: str)`: Connects to a room.
- `close()`: Closes the client and associated resources.

### `Room`
- `connect()`: Connects to a room.
- `state`: Provides the current connection state.

### `Socket`
- `connect(token: str)`: Establishes a WebSocket connection.
- `close(code: int)`: Closes the WebSocket connection.

### `LocalPeer`
- `produce(track: Any)`: Produces a media track.
- `consume(producer_id: str)`: Consumes a media track.

