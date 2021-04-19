from src.retail import search_benchmark
from src.service_layer import handler

from dialogflow_fulfillment import Card

def product_search(agent):

    query = agent.parameters.get('query')

    #TODO response = search(query=query, pageSize=3)
    response = search_benchmark(query=query, pageSize=3)

    if not response.results:
        agent.add(f"I couldn't find anything that matches '{query}'... 😢")
        return

    if response.was_autocorrected:
        agent.add(f"Do you mean '{response.query}'?")
    
    agent.add("Here's what I found 👇")

    for product in response.results:
        agent.add(Card(
            title=product.name,
            subtitle=product.brand,
            image_url=product.image_url
        ))