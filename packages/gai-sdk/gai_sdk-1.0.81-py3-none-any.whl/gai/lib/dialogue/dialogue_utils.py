import json
from gai.lib.dialogue.dialogue_message import DialogueMessage

def ExtractRecap(messages:list[DialogueMessage] , last_n:int=6) -> str:
    
    last_n_messages = messages[-last_n:]

    recap = []

    # Get past messages and last user message
    for message in last_n_messages:

        # ignore placeholder
        if not message.Content:
            continue

        # ignore images
        if message.Content.startswith('data:image'):
            continue

        recap.append({"name":message.Name,"content":message.Content})
        # if message.Role == 'user':
        #     text += f"<{message.Role}>"
        #     text += message.Content
        #     text += f"</{message.Role}>"
        # else:
        #     text += f"<{message.Name}>"
        #     text += message.Content
        #     text += f"</{message.Name}>"

    return recap

# def ExtractRecap(messages:list[DialogueMessage] , last_n:int=6) -> str:
#     recap = []

#     # Get past messages and last user message
#     for message in messages:

#         # ignore placeholder
#         if not message.Content:
#             continue

#         # ignore images
#         if message.Content.startswith('data:image'):
#             continue

#         if message.Role == 'user':
#             recap.append({"user": message.Content})
#         else:
#             recap.append({message.Name: message.Content})

#     # Recap last n messages and inject into monologue template [1]
#     recap = recap[-last_n:]

#     # Convert to JSON string
#     recap = json.dumps(recap)

#     return recap