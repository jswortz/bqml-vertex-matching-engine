# Documentation

Refer to this [https://docs.google.com/document/d/1Wyxra0NjjUmzkLajLrJ4bq68D7a6CnO5FksFITpWREg/edit](document) if you are onboarding in this project

## Endpoints

- `/chatbot`:
    - Method: POST
    - Description: interaction with the retail store chatbot
    - Headers: 
        - `Authorization*`: token access string
    - Body Params (JSON):
        - `session_id*`: string that uniquely identifies a conversation instance
        - `query_string*`: the sentence typed by the user
    - Response:
        - response matched by dialog flow
    - Example:
        
        ```
            {

                "session_id": "adfgfdsgdsf",
                "query_string": "Can I change my item?"
            }
        ``` 

