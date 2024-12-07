```mermaid

                stateDiagram-v2
                INIT --> CRAFT_TEXT_PROMPT: next / on_CRAFT_PROMPT
                CRAFT_TEXT_PROMPT --> GENERATE: next / on_GENERATE
                GENERATE --> END: next / on_ERROR / has_error
                GENERATE --> PROCESS: next / on_PROCESS / not_has_error
                PROCESS --> END: next
            
```