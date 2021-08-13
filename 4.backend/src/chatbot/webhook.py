from src.chatbot import intents
from src.config import DIALOGFLOW_AUTH_USER
from src.config import DIALOGFLOW_AUTH_PASSWORD
from dialogflow_fulfillment import WebhookClient

intent_map = {
    "product.search": intents.product_search,
    # "example.intent": intents.example_intent_func
}


def authorize(user, password):
    return user == DIALOGFLOW_AUTH_USER and \
        password == DIALOGFLOW_AUTH_PASSWORD


def handle_webhook(request_body):
    agent = WebhookClient(request_body)
    agent.handle_request(intent_map)

    return agent.response
