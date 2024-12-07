import pika
from pika.adapters.blocking_connection import BlockingConnection, BlockingChannel


class Rabbit:
    def __init__(self, host, port, username, password):
        credentials = pika.PlainCredentials(username, password)
        self.connection_parameters = pika.ConnectionParameters(
            host=host,
            port=port,
            credentials=credentials,
            virtual_host="/")
        self.connection: BlockingConnection | None = None
        self.channel: BlockingChannel | None = None

    def __enter__(self):
        self.connection = pika.BlockingConnection(self.connection_parameters)
        self.channel = self.connection.channel()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
