import json
from channels.generic.websocket import AsyncWebsocketConsumer

from elsecommon.transports.router import Router
from elsepublic.api.interfaces.proxy_operation_interfaces import ProxyOperationInterface
from elsepublic.api.serializers.proxy_operation_serializer import ProxyOpParamsSerializer


class CallOperation(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super(CallOperation, self).__init__(*args, **kwargs)
        self.session_uuid = None

    async def connect(self):
        self.session_uuid = str(self.scope['url_route']['kwargs']['session'])

        await self.channel_layer.group_add(
            self.session_uuid,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.session_uuid,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        proxy_op = Router[ProxyOperationInterface]
        proxy_params = ProxyOpParamsSerializer(data=text_data_json['operation_data']).to_entity()
        proxy_op(
            proxy_params,
            session_uuid=self.session_uuid,
            operation_request=text_data_json['operation_request'],
            web_socket_consumer='send_result',
        )

    async def send_result(self, event):
        message = dict(
            result=event['operation_result'],
            operation_request=event['operation_request'],
        )

        await self.send(text_data=json.dumps(message))
