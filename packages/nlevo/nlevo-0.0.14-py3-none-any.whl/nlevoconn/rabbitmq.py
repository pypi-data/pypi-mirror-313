import time
import logging
from pika import (PlainCredentials,
                  ConnectionParameters,
                  BlockingConnection,
                  exceptions)
from unittest import TestCase, main

logger = logging.getLogger('connection')


class RabbitMQConnection:
    _instance = None

    def __new__(cls, host="nt10", port=5672, username="admin", password="admin"):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, host="nt10", port=5672, username="admin", password="admin"):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.connection = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self) -> bool:
        retries = 0
        while retries < 10:
            try:
                credentials = PlainCredentials(self.username, self.password)
                parameters = ConnectionParameters(
                    host=self.host, port=self.port, credentials=credentials)
                self.connection = BlockingConnection(parameters)
                logger.info('Connected to RabbitMQ')
                return True
            except exceptions.AMQPConnectionError as ex:
                logger.warning(f'Failed to connect to RabbitMQ: {ex}')
                retries += 1
                wait_time = 2 ** retries
                logger.warning(f'Retrying in {wait_time} seconds...')
                time.sleep(wait_time)

        logger.error(
            'Exceeded maximum number of connection retries. Stopping the code.')
        return False

    def is_connected(self):
        return self.connection is not None and self.connection.is_open

    def close(self):
        if self.is_connected():
            self.connection.close()
            self.connection = None
            logger.info('Closed RabbitMQ connection')

    def get_channel(self):
        if self.is_connected():
            return self.connection.channel()
        return None


class rabbitmq_test(TestCase):
    def test_connect(self):
        connect = RabbitMQConnection()
        self.assertTrue(connect.connect())
        self.assertTrue(connect.is_connected())
        connect.close()
        self.assertFalse(connect.is_connected())

    def test_getchannel(self):
        connect = RabbitMQConnection()
        connect.connect()
        self.assertIsNotNone(connect.get_channel())
        connect.close()


if __name__ == '__main__':
    main()
