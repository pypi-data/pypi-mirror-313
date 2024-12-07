from gai.lib.dialogue.pydantic.MonologueMessagePydantic import MonologueMessagePydantic

import time

class MonologueMessageBuilder:

    def __init__(self, messages=None):
        self.messages = messages or []

    def AddSystemMessage(self, Content, Title="Init", Timestamp:int=None):
        self.messages.append(MonologueMessagePydantic(
            Order=len(self.messages),
            Name="System",
            Role="system",
            Title=Title,
            Content=Content,
            Timestamp= Timestamp or int(time.time())
        ))
        return self

    def AddUserMessage(self, Content, Title="Init", Timestamp:int=None):
        self.messages.append(MonologueMessagePydantic(
            Order=len(self.messages),
            Name="User",
            Role="user",
            Title=Title,
            Content=Content,
            Timestamp= Timestamp or int(time.time())
        ))
        return self

    def AddAssistantMessage(self, Content=None,Title="Init",Timestamp:int=None):
        if Content is None:
            Content = ""
        self.messages.append(MonologueMessagePydantic(
            Order=len(self.messages),
            Name="Assistant",
            Role="assistant",
            Title=Title,
            Content=Content,
            Timestamp= Timestamp or int(time.time())
        ))
        return self

    def Build(self):
        return self.messages
    
    def BuildRoleMessages(self):
        return [{
            "role": x.Role, 
            "content": x.Content
            } for x in self.messages]
