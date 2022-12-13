import logging


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def find_clients(text, mappings):
    """
    Finds all clients mentioned in the text.

    Args:
        text: The text to search for clients.
        mappings: A list of OwnerClientMapping objects.

    Returns:
        A list of clients mentioned in the text.
    """
    clients = []
    for mapping in mappings:
        if any(cust in text for cust in mapping.clients):
            clients.append(mapping.owner)
    return clients


def send_mention(channel_id, clients):
    """
    Sends a mention to the owners of the specified clients.

    Args:
        channel_id: The ID of the Slack channel to send the mention to.
        clients: A list of clients whose owners should be mentioned.
    """
    for client in clients:
        try:
            client.chat_postMessage(channel=channel_id, text="<@"+client+">")
        except Exception as e:
            logger.error("Failed to send mention to owner of client %s: %s", client, e)