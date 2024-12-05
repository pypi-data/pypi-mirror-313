<!-- Begin Banner -->
<a href="https://huddle01.com"><p align="center">
<img height=100 src="https://user-images.githubusercontent.com/34184939/167926050-f1e2db1d-49ae-4b51-bd98-68e09b45c5b1.svg"/>

</p></a>
<p align="center">
  <strong>The dRTC Infra for AI.</strong>
</p>

<!-- End Banner -->

# Overview 🚀
This repository aims to bridge the gap between Artificial Intelligence (AI) and Real-Time Communication (RTC) technologies. It provides a set of examples and tutorials to help developers integrate AI into their WebRTC applications. 

# Features 🎯
- **Agents**: AI-powered agents that can be integrated into WebRTC applications, such as chatbots, voicebots, and video bots.

- **LLM Models**: API for integrating Large Language Models (LLM) into WebRTC applications, such as Realtime API, Text-to-Speech, and Speech-to-Text.

# Quick Start 🚀

To install the core Agents library:
```bash
pip install ai01
```

Internally the Library uses `huddle01-ai` package to interact with the dRTC Network and build WebRTC Connections.

# Basic Usage 📝

```python
import asyncio
from ai01.agent import Agent, AgentOptions
from ai01.providers.openai import AudioTrack
from ai01.rtc import RTCOptions, Role, HuddleClientOptions

# Configure RTC options
rtc_options = RTCOptions(
    api_key="your_huddle_api_key",
    project_id="your_project_id",
    room_id="your_room_id",
    role=Role.HOST,
    metadata={"displayName": "AI Agent"}
)

# Initialize Agent
agent = Agent(
    options=AgentOptions(
        rtc_options=rtc_options,
        audio_track=AudioTrack()
    )
)
```

# Module Documentation 📖

The core module can be broken down into the following submodules:

- **`ai01.agent`**: Core module for creating AI agents that can be integrated into WebRTC applications, each agent can be considered as a separate entity that can be connected to a dRTC room, and can interact with other agents and users.

- **`ai01.providers`**: Module for integrating AI providers into the core module, such as OpenAI, Google Cloud, and Microsoft Azure, and also exposes API to integrate custom AI providers.

- **`ai01.rtc`**: Module for integrating Real-Time Communication (RTC) technologies into the core module, such as Huddle, Twilio, and Agora, and also exposes API to integrate custom RTC providers, Each Agent in itself is connected to an RTC room.

Anything can be built with mixing and matching different agents with different models in any pattern which is suitable for the application.

## Agent Module
The Agent module provides the core functionality for creating AI agents that can participate in real-time communication rooms.

An Agent is a high-level entity that can:

- Connect to dRTC network
- Interact with AI models
- Process media streams
- Handle room events

### Agent Methods
- **`join()`**

Join Method is used to join the dRTC Network and establish a websocket connection, upon successful connection the agent is assigned a `room` 
using which agent can setup necessary event listeners before calling `connect` method.

```python
from ai01.agent import Agent, AgentOptions
from ai01.rtc import RoomEvents

room = await agent.join()

@room.on(RoomEvent.RoomJoined)
def on_room_joined():
    print("Room Joined")

```
> Note: The `join` method is an async method and should be awaited before calling any other method.


- **`connect(`)**

Connect Method is used to establish a WebRTC Connection with the room, upon successful connection the agent can start sending and receiving media streams.

```python
await agent.connect()
```

### Events


## Providers Module
The Providers module provides a set of APIs for integrating AI providers into the core module.

Currently, the following providers are supported:
- `OpenAI`: Realtime API, Text-to-Speech, Speech-to-Text
- `Gemini`: Realtime API, Text-to-Speech, Speech-to-Text

### OpenAI Provider
The OpenAI provider provides an API for integrating OpenAI models into the core module.


### RTC Module





