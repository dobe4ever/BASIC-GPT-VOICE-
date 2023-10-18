functions = [
    {
        "name": "set_custom_instructions",
        "description": "Overwrites the current custom instructions. Call this function when the user specifically asks to set or edit custom instructions.",
        "parameters": {
            "type": "object",
            "properties": {
                "instructions": {
                    "type": "string",
                    "description": "The instructions that ChatGPT will see as the top message in every user interaction (aka the system message)"
                }
            },
            "required": ["instructions"]
        }
    }
]
