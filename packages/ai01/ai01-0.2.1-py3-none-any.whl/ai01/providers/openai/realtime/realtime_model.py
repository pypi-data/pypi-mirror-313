import asyncio
import logging

from pydantic import BaseModel

from ai01.agent import Agent
from ai01.utils.socket import SocketClient

from . import _api, _exceptions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RealTimeModelOptions(BaseModel):
    """
    RealTimeModelOptions is the configuration for the RealTimeModel.
    """

    oai_api_key: str
    """
    OpenAI API Key is the API Key for the OpenAI API.
    """

    model: _api.RealTimeModels = "gpt-4o-realtime-preview"
    """
    Model is the RealTimeModel to be used, defaults to gpt-4o-realtime-preview.
    """

    instructions: str = ""
    """
    Instructions is the Initial Prompt given to the Model.
    """

    modalities: list[_api.Modality] = ["text", "audio"]
    """
    Modalities is the list of things to be used by the Model.
    """

    voice: _api.Voice = "alloy"
    """
    Voice is the of audio voices which will be generated and returned by the Model.
    """

    temperature: float = 0.8
    """
    Temperature is the randomness of the Model, to select the next token.
    """

    input_audio_format: _api.AudioFormat = "pcm16"
    """
    Input Audio Format is the format of the input audio, which is given to the Model.
    """

    output_audio_format: _api.AudioFormat = "pcm16"
    """
    Output Audio Format is the format of the audio, which is returned by the Model.
    """

    base_url: str = "wss://api.openai.com/v1/realtime"
    """
    Base URL is the URL of the RealTime API, defaults to the OpenAI RealTime API.
    """

    tool_choice: _api.ToolChoice = "auto"
    """
    Tools are different other APIs which the Model can access, defaults to auto.
    """

    server_vad_opts: _api.ServerVad = {
        "type": "server_vad",
        "threshold": 0.5,
        "prefix_padding_ms": 1000,
        "silence_duration_ms": 500,
    }
    """
    Server VAD which means Voice Activity Detection is the configuration for the VAD, to detect the voice activity.
    """

    loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
    """
    Loop is the Event Loop to be used for the RealTimeModel, defaults to the current Event Loop.
    """

    class Config:
        arbitrary_types_allowed = True


class RealTimeModel:
    def __init__(self, agent: Agent, options: RealTimeModelOptions):
        # Agent is the instance which is interacting with the RealTimeModel.
        self.agent = agent

        self._opts = options
        # Loop is the Event Loop to be used for the RealTimeModel.
        self.loop = options.loop

        # Socket is the WebSocket connection to the RealTime API.
        self.socket = SocketClient(
            url=f"{self._opts.base_url}?model={self._opts.model}",
            headers={
                "Authorization": f"Bearer {self._opts.oai_api_key}",
                "OpenAI-Beta": "realtime=v1",
            },
            loop=self.loop,
            json=True,
        )

        # Turn Detection is the configuration for the VAD, to detect the voice activity.
        self.turn_detection = options.server_vad_opts

        # Logger for RealTimeModel.
        self._logger = logger.getChild(f"RealTimeModel-{self._opts.model}")

    def session_update(self):
        """
        Session Updated is the Event Handler for the Session Update Event.
        """
        try:
            self._logger.info("Send Session Updated ")

            if not self.socket.connected:
                raise _exceptions.RealtimeModelNotConnectedError()

            opts = self._opts

            session_data: _api.ClientEvent.SessionUpdateData = {
                "instructions": self._opts.instructions,
                "voice": opts.voice,
                "input_audio_format": opts.input_audio_format,
                "input_audio_transcription": {"model": "whisper-1"},
                "max_response_output_tokens": 100,
                "modalities": opts.modalities,
                "temperature": opts.temperature,
                "tools": [],
                "turn_detection": opts.server_vad_opts,
                "output_audio_format": opts.output_audio_format,
                "tool_choice": opts.tool_choice,
            }

            payload: _api.ClientEvent.SessionUpdate = {
                "session": session_data,
                "type": "session.update",
            }

            self.loop.create_task(self.socket.send(payload))

        except Exception as e:
            self._logger.error(f"Error Sending Session Update Event: {e}")
            raise

    async def connect(self):
        """
        Connects the RealTimeModel to the RealTime API.
        """
        try:
            self._logger.info(f"Connecting to RealTime API at {self._opts.base_url}")

            await self.socket.connect()

        except _exceptions.RealtimeModelNotConnectedError as e:
            raise e

        except Exception as e:
            self._logger.error(f"Error connecting to RealTime API: {e}")
            raise _exceptions.RealtimeModelSocketError()
