import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings

from elsecommon.services.pika_connect_service import pika_connection
from elsecommon.transports.event_transport import EventTransport


class ApiEventTransport(EventTransport):
    """
    Async transport for web API
    """
    def __init__(self, interface: any, expose=False):
        self.result_exchange_name = f'{self.get_exchange_name(interface)}.result'
        self.result_queue_name = f'{self.get_queue_name(interface)}.result'
        self.result_queue = None
        super(ApiEventTransport, self).__init__(interface, expose=expose)

    def init_event_server(self):
        super(ApiEventTransport, self).init_event_server()
        pika_connection.get_channel().exchange_declare(exchange=self.result_exchange_name, exchange_type='topic')
        qres = pika_connection.get_channel().queue_declare(queue=self.result_queue_name)
        self.result_queue = qres.method.queue

        pika_connection.get_channel().queue_bind(
            exchange=self.result_exchange_name,
            queue=self.result_queue,
            routing_key='#',
        )
        pika_connection.get_channel().basic_consume(
            self.on_event_response,
            queue=self.result_queue,
            no_ack=False
        )

    def on_event_response(self, ch, method, properties, body):
        message = json.loads(body)
        result = message['result']
        context = message['context']
        ch.basic_ack(delivery_tag=method.delivery_tag)

        channel_layer = get_channel_layer()
        web_socket_consumer = context['web_socket_consumer']
        async_to_sync(channel_layer.group_send)(
            context['session_uuid'],
            dict(
                type=web_socket_consumer,
                operation_result=result,
                **context,
            )
        )
