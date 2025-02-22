import json
from enum import Enum
from dataclasses import dataclass
from typing import Union


# Define an enumeration for the message types
class MessageType(Enum):
    CHAT = "chat"
    REACTION = "reaction"


# Define the structure for each message type using dataclasses
@dataclass
class ChatMessage:
    text: str
    timestamp: str
    username: str


@dataclass
class ReactionMessage:
    id: int
    reaction_text: str


# Define the Message class with dynamic structure based on type
class Message:
    def __init__(self, message_type: MessageType, content: Union[ChatMessage, ReactionMessage], username: str, token: str):
        self.message_type = message_type
        self.content = content
        self.username = username
        self.token = token

    @staticmethod
    def from_json(json_str: str):
        # Parse the JSON string
        data = json.loads(json_str)
        
        # Extract the username and token for authentication
        username = data['username']
        token = data['token']

        message_type = MessageType(data['type'])

        # Create a message object based on the type
        if message_type == MessageType.CHAT:
            content = ChatMessage(text=data['text'], timestamp=data['timestamp'], username=data['username'])
        elif message_type == MessageType.REACTION:
            content = ReactionMessage(id=data['id'], reaction_text=data['reaction_text'])
        else:
            raise ValueError(f"Unsupported message type: {message_type}")

        # Return the Message object
        return Message(message_type, content, username, token)

    def __str__(self):
        return f"Message(type={self.message_type.value}, username={self.username}, token={self.token}, content={self.content})"