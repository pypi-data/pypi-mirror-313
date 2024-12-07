import json
import uuid
import time
from typing import List

from gai.lib.common.logging import getLogger

logger = getLogger(__name__)
from gai.lib.common.errors import InternalException, MessageNotFoundException
from gai.lib.dialogue.pydantic.DialogueMessagePydantic import DialogueMessagePydantic
from gai.lib.dialogue.pydantic.MonologueMessagePydantic import MonologueMessagePydantic
from threading import Lock

class DialogueStore:

    dialogue_id="00000000-0000-0000-0000-000000000000"
    round_no=0
    turn_no=0
    lock=Lock()

    def __init__(self, 
                 caller_id:str, 
                 agent_id:str, 
                 dialogue_id:str, 
                 api_host:str, 
                 message_count_cap:int=10,
                 message_char_cap:int=4000
                 ):
        
        self.caller_id = caller_id
        self.agent_id = agent_id
        self.capped_message_queue:list[DialogueMessagePydantic] = []
        dialogue_id = dialogue_id
        self.message_count_cap = message_count_cap
        self.message_char_cap = message_char_cap
        self.api_host = api_host
        self.dialogue_repo = None


    @staticmethod
    def create_message_id(dialogue_id,round_no,turn_no,postfix):
        return f"{dialogue_id}:{round_no}:{turn_no}{postfix}"

    def clear(self):
        DialogueStore.round_no=0
        DialogueStore.turn_no=0
        self.capped_message_queue:list[DialogueMessagePydantic] = []

    def list_dialogue_messages(self):
        return self.capped_message_queue

    def delete_dialogue_message(self,message_id):
        try:
            self.capped_message_queue = [msg for msg in self.capped_message_queue if msg.Id != message_id]
        except Exception as e:
            id = str(uuid.uuid4())
            logger.error(f'DialogueClient.delete_dialogue_message: error={str(e)} id={id}')
            raise InternalException(id)
    
    def get_last_message_by_role(
        self,
        role: str):
        try:
            message_queue = [msg for msg in self.capped_message_queue if msg.Role == role]
            last_message = message_queue[-1] if message_queue else None
            if last_message is None:
                return None
            return last_message
        except Exception as e:
            id = str(uuid.uuid4())
            logger.error(f'DialogueClient.get_last_message_by_role: error={str(e)} id={id}')
            raise InternalException(id)    
    
    def get_message_by_id(self,message_id: str):
        msg = next((msg for msg in self.capped_message_queue if msg.Id == message_id),None)
        return msg

    # Monologue is the thought process behind the agent's dialogue message.
    # To get the monologue, get the dialogue message then retrieve the monologue from the message.
    def get_monologue(self,message_id):
        try:
            message = next([msg for msg in self.capped_message_queue if msg.Id == message_id],None)
            if message is None:
                raise MessageNotFoundException()
            return message.Monologue
        except Exception as e:
            id = str(uuid.uuid4())
            logger.error(f'DialogueClient.get_monologue: error={str(e)} id={id}')
            raise InternalException(id)

    # def activate_dialogue(self,dialogue_id):
    #     try:
    #         self.dialogue_repo.activate_dialogue(dialogue_id)
    #     except Exception as e:
    #         id = str(uuid.uuid4())
    #         logger.error(f'DialogueClient.get_monologue: error={str(e)} id={id}')
    #         raise InternalException(id)
        
    # def get_active_dialogue(self):
    #     try:
    #         return self.dialogue_repo.get_active_dialogue(self.caller_id)
    #     except Exception as e:
    #         id = str(uuid.uuid4())
    #         logger.error(f'DialogueClient.get_active_dialogue: error={str(e)} id={id}')
    #         raise InternalException(id)

    # dialogue_id is always issued by DialogueClient.
    @staticmethod
    def NewDialogue(caller_id:str=None) -> str:
        try:
            DialogueStore.dialogue_id="00000000-0000-0000-0000-000000000000"
            DialogueStore.round_no=0
            DialogueStore.turn_no=0
            return DialogueStore.dialogue_id
        except Exception as e:
            id = str(uuid.uuid4())
            logger.error(f'DialogueClient.add_dialogue: error={str(e)} id={id}')
            raise InternalException(id)
        
    @staticmethod
    def NewTurn()->str:
        DialogueStore.turn_no += 1

    @staticmethod
    def NewRound()->str:
        DialogueStore.round_no += 1
        DialogueStore.turn_no = 0

    # Add user message and pop old message if capped length has exceeded
    def add_user_message(self,
                         message_id:str,
                         user_id:str,
                         content:str,
                         timestamp:int):
        
        user_message = DialogueMessagePydantic(
            Id=message_id,
            DialogueId=self.dialogue_id,
            Content=content,
            Name="user",
            Role="user",
            Timestamp=timestamp,
            Order = self.capped_message_queue[-1].Order + 1 if self.capped_message_queue else 0,
            OwnerId=user_id
        )

        try:
            self.capped_message_queue.append(user_message)
            if len(self.capped_message_queue) > self.message_count_cap:
                self.capped_message_queue = self.capped_message_queue[-self.message_count_cap:]
        except Exception as e:
            id = str(uuid.uuid4())
            logger.error(f'DialogueClient.update_dialogue: error={str(e)} id={id}')
            raise InternalException(id)

    # Add assistant message and pop old message if capped length has exceeded
    def add_assistant_message(self,
                              message_id:str,
                              name:str,
                              content:str,
                              monologue:List[MonologueMessagePydantic]=None
                              ):
        image_url = f"{self.api_host}/api/v1/persona/{name}/thumbnail"
        assistant_message = DialogueMessagePydantic(
            Id=message_id,
            DialogueId=self.dialogue_id,
            Content=content,
            Name=name,
            Role="assistant",
            Timestamp=int(time.time()),
            Order=self.capped_message_queue[-1].Order + 1 if self.capped_message_queue else 0,
            OwnerId=self.agent_id,
            ImageUrl=image_url,
            Monologue=None if not monologue else json.dumps([msg.dict() for msg in monologue])
        )
        try:
            self.capped_message_queue.append(assistant_message)
            if len(self.capped_message_queue) > self.message_count_cap:
                self.capped_message_queue = self.capped_message_queue[-self.message_count_cap:]
        except Exception as e:
            id = str(uuid.uuid4())
            logger.error(f'DialogueClient.update_dialogue: error={str(e)} id={id}')
            raise InternalException(id)

    # Called by chat to add dialogue message before return
    # First message may not be a user message but
    # the Last message will always the assistant message
    # Use this method when monologue is available
    def update_dialogue(self,
                        user_message_id:str,
                        assistant_message_id:str,
                        user_message:str,
                        monologue:List[MonologueMessagePydantic]):
        try:
            # Add user message to dialogue
            self.add_user_message(
                message_id=user_message_id,
                user_id=self.caller_id,
                content=user_message,
                timestamp=monologue[0].Timestamp
            )

            # Add assistant message to dialogue
            self.add_assistant_message(
                message_id=assistant_message_id,
                name=monologue[-1].Name,
                content=monologue[-1].Content,
                monologue=monologue
            )
        except Exception as e:
            id = str(uuid.uuid4())
            logger.error(f'DialogueClient.update_dialogue: error={str(e)} id={id}')
            raise InternalException(id)
