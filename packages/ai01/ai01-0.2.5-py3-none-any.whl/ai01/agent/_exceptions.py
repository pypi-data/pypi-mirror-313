from __future__ import annotations


class AgentError(Exception):
    """Base class for exceptions in this module."""

    message: str

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class RoomNotCreatedError(AgentError):
    """Exception raised for errors in the Agent Room, when Room is not created."""

    def __init__(
        self,
    ):
        super().__init__(
            """
            Room Creation Failed, Possible ways to fix this:
            - Call the `agen.join()` before calling `agent.connect()` to the Room
            - Make sure the API_KEY and Project_ID are valid before creating Room.
            - Make Sure the room_id is valid for the API_KEY being used to connect to the Room.
            """
        )


class RoomNotConnectedError(AgentError):
    """Exception raised for errors in the Agent Room, when Room is not connected."""

    def __init__(
        self,
    ):
        super().__init__(
            """
            Room is not created, Possible ways to fix this:
            - Call the `agent.join()` before calling `agent.connect()` to the Room
            - Make sure the API_KEY and Project_ID are valid before creating Room.
            - Make Sure the room_id is valid for the API_KEY being used to connect to the Room.
            """
        )
