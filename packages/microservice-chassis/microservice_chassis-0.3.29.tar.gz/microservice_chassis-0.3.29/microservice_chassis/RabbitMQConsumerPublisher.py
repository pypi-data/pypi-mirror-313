from datetime import datetime
import ssl

import pika
import threading
import logging
import time

logger = logging.getLogger(__name__)


class ThreadedConsumerPublisher(threading.Thread):

    def __init__(self, ampq_url, service_name, ca_certificate_path, client_certificate_path, client_key_path, cn_server_hostname):
        threading.Thread.__init__(self)
        self.service_name = service_name
        self.parameters = pika.URLParameters(ampq_url)
        self.parameters.heartbeat = 600
        self.connection = None
        self.channel = None

        ssl_context = ssl.create_default_context(cafile=ca_certificate_path)
        ssl_context.minimum_version = ssl.TLSVersion.TLSv1_3
        ssl_context.load_cert_chain(
            certfile=client_certificate_path,
            keyfile=client_key_path
        )
        self.ssl_options = pika.SSLOptions(context=ssl_context, server_hostname=cn_server_hostname) # Add SSL options for TLS
        self._stop_event = threading.Event()  # Thread stop signal
        self.lock = threading.Lock()  # Lock for synchronizing

        # Track declarations and consumers
        self.exchanges = []
        self.queues = []
        self.bindings = []
        self.consumers = []

        self._connect()

    def _connect(self):
        """Establishes a new connection and channel and re-declares necessary queues and consumers."""
        while not self._stop_event.is_set():
            try:
                # Apply SSL options if provided
                connection_params = self.parameters
                if self.ssl_options:
                    connection_params.ssl_options = self.ssl_options

                self.connection = pika.BlockingConnection(connection_params)
                self.channel = self.connection.channel()
                logger.info("RabbitMQ connection established.")

                # Re-establish all declarations, bindings, and consumers
                self._redeclare_all()

                return
            except pika.exceptions.AMQPConnectionError as e:
                logger.error("Connection failed, retrying in 5 seconds: %s", e)
                time.sleep(5)  # Wait before retrying

    def _redeclare_all(self):
        """Re-declares all exchanges, queues, bindings, and consumers."""
        for exchange_name, exchange_type in self.exchanges:
            self.channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)

        for queue_name in self.queues:
            self.channel.queue_declare(queue=queue_name, auto_delete=False)

        for queue_name, exchange_name, routing_key in self.bindings:
            self.channel.queue_bind(queue=queue_name, exchange=exchange_name, routing_key=routing_key)

        for queue_name, message_handler in self.consumers:
            self.channel.basic_consume(queue=queue_name, on_message_callback=message_handler)

        logger.info("Re-declared exchanges, queues, bindings, and consumers.")

    def exchange_declare(self, exchange_name, exchange_type='topic'):
        self.exchanges.append((exchange_name, exchange_type))  # Track exchange declarations
        self.channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)

    def queue_declare(self, queue_name):
        self.queues.append(queue_name)  # Track queue declarations
        self.channel.queue_declare(queue=queue_name, auto_delete=False)

    def bind_queue(self, queue_name, exchange_name, routing_key):
        self.bindings.append((queue_name, exchange_name, routing_key))  # Track bindings
        self.channel.queue_bind(queue=queue_name, exchange=exchange_name, routing_key=routing_key)

    def consume_on_queue(self, queue_name, message_handler):
        self.consumers.append((queue_name, message_handler))  # Track consumers
        self.channel.basic_consume(queue=queue_name, on_message_callback=message_handler)

    def run(self):
        while not self._stop_event.is_set():
            try:
                if self.channel.is_open:
                    self.channel.start_consuming()
                else:
                    logger.warning("Channel closed, reconnecting...")
                    self._connect()
            except pika.exceptions.AMQPConnectionError:
                logger.error("Connection lost during consuming, reconnecting...")
                self._connect()  # Reconnect on connection error
            except Exception as e:
                logger.error("Unexpected error in consumer: %s", e)
                self._connect()  # Reconnect on unexpected errors

    def start_consumer(self):
        consumer_thread = threading.Thread(target=self.run)
        consumer_thread.start()

    def stop(self):
        logger.debug('Stopping consumer...')
        self._stop_event.set()
        if self.channel.is_open:
            self.channel.stop_consuming()

        if self.connection.is_open:
            self.channel.close()
            self.connection.close()

    def publish_message(self, exchange_name, routing_key, message):
        with self.lock:
            try:
                if not self.connection.is_open or not self.channel.is_open:
                    logger.debug("Re-establishing RabbitMQ connection for publishing...")
                    self._connect()

                properties = pika.BasicProperties(
                    headers={
                        "origin_service": self.service_name,
                        "timestamp": datetime.now().isoformat()
                    }
                )

                self.channel.basic_publish(
                    exchange=exchange_name,
                    routing_key=routing_key,
                    body=message,
                    properties=properties
                )
                logger.info("Message published: \"%s\" on exchange: \"%s\" with routing key: \"%s\"",
                            message, exchange_name, routing_key)
            except pika.exceptions.AMQPConnectionError as e:
                logger.error("Connection error during publish, attempting reconnect: %s", e)
                self._connect()
            except Exception as e:
                logger.error("Unexpected error during publish: %s", e)
                self._connect()
