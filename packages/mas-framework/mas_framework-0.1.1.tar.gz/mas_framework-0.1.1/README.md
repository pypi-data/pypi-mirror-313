# MAS AI - Multi-Agent System AI Infrastructure

NOTE: This project is under active development and not yet stable. 🧪


MAS AI is a flexible and robust infrastructure for building multi-agent systems with a focus on reliable message passing and agent lifecycle management.

## Features

- **Reliable Message Transport**: Redis-based pub/sub system with separate channels for system and agent messages
- **Agent Lifecycle Management**: Automatic registration, health checks, and graceful shutdown
- **Flexible Persistence**: Pluggable storage backends (in-memory provided)
- **Type Safety**: Full typing support with strict mypy compliance
- **Core Services**: Built-in discovery and registration services

## Installation

```bash
pip install mas-framework
```

## Quick Start

1. Start Redis server (required for message transport):

```bash
redis-server
```

2. Create your agent:

```python
from mas.protocol import Message
from mas.sdk.agent import Agent


class MyAgent(Agent):
   async def _initialize(self) -> None:
      """Custom initialization logic."""
      pass

   async def _cleanup(self) -> None:
      """Custom cleanup logic."""
      pass

   async def _handle_agent_message(self, message: Message) -> None:
      """Handle incoming agent messages."""
      print(f"Received message: {message.payload}")
```

3. Run your agent:

```python
import asyncio

from mas import MASCoreService
from mas.persistence.memory import InMemoryProvider
from mas.transport.redis import RedisTransport
from mas.transport.service import TransportService


async def main():
   # Initialize core services
   persistence = InMemoryProvider()
   transport = TransportService(transport=RedisTransport())
   core = MASCoreService(transport=transport, persistence=persistence)

   # Start core service
   await core.start()

   # Create and start agent
   agent = MyAgent(
           config=AgentConfig(
                   agent_id="my_agent",
                   endpoint="http://localhost:8080/my_agent",
                   capabilities={"feature1", "feature2"}
           ),
           transport=transport,
           persistence=persistence
   )

   await agent.start()

   try:
      # Keep running
      while True:
         await asyncio.sleep(1)
   finally:
      await agent.stop()
      await core.stop()


if __name__ == "__main__":
   asyncio.run(main())
```

## Architecture

### Components

1. **Agent SDK**

   - Base Agent class with lifecycle management
   - Message handling infrastructure
   - Health check system

2. **Transport Layer**

   - Redis-based pub/sub implementation
   - Separate channels for system and agent messages
   - Reliable message delivery

3. **Core Services**

   - Agent registration and discovery
   - Status monitoring
   - Capability-based agent lookup

4. **Persistence Layer**
   - Pluggable storage backend
   - In-memory implementation provided
   - Interface for custom implementations

### Message Types

1. **System Messages**

   - `REGISTRATION_REQUEST`: Agent registration
   - `REGISTRATION_RESPONSE`: Registration confirmation
   - `STATUS_UPDATE`: Agent health checks
   - `ERROR`: Error notifications

2. **Agent Messages**
   - `AGENT_MESSAGE`: Direct agent communication
   - `DISCOVERY_REQUEST`: Agent discovery
   - `DISCOVERY_RESPONSE`: Discovery results

## Examples

### Chain Message Example

See the chain message example in `examples/chain/` demonstrating message passing between multiple agents:

```python
from mas.protocol import Message, MessageType
from mas.sdk.agent import Agent


class ChainAgent(Agent):
   async def _handle_agent_message(self, message: Message) -> None:
      if message.message_type == MessageType.AGENT_MESSAGE:
         count = message.payload["chain_count"]
         print(f"Agent {self.id} received message (count: {count})")

         if count >= 4:
            print("Chain complete!")
            return

         await self.send_message(
                 target_id=self.next_agent_id,
                 content={"chain_count": count + 1}
         )
```

Run the example:

```bash
python -m examples.chain.main
```

## Advanced Usage

### Custom Transport Implementation

Implement `ITransport` interface for custom transport layers:

```python
from typing import AsyncGenerator

from mas.transport.interfaces import ITransport
from mas.protocol import Message


class MyTransport(ITransport):
   async def initialize(self) -> None:
      pass

   async def publish(self, message: Message) -> None:
      pass

   async def subscribe(self, channel: str) -> AsyncGenerator[Message, None]:
      pass

   async def cleanup(self) -> None:
      pass

   async def unsubscribe(self, channel: str) -> None:
      pass
```

### Custom Persistence

Implement `IPersistenceProvider` for custom storage:

```python
from mas.persistence.interfaces import IPersistenceProvider


class MyStorage(IPersistenceProvider):
   async def initialize(self) -> None:
      pass

   async def create_agent(self, agent: Agent) -> Agent:
      pass

   async def get_agent(self, agent_id: str) -> Optional[Agent]:
      pass
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `pytest`
5. Submit a pull request

## License

MIT License - see LICENSE file for details
