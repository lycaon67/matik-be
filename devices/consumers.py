import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async 
from devices.management import DevicesManagement, ChannelsManagement

class DeviceConsumer(WebsocketConsumer):

    def connect(self):
        try:
            self.home_id = self.scope['url_route']['kwargs']['home_id']
            self.home_group_name = 'homegroup_{0}'.format(self.home_id)

            async_to_sync(self.channel_layer.group_add)(self.home_group_name, self.channel_name)
            
            self.accept()
            device_channel_list = DevicesManagement().find_by_all_homeId(home_id=self.home_id)

            self.send(text_data=json.dumps({
                'type':'deviceInfo',
                'deviceStatus': device_channel_list
            }))
        except Exception as err:
            print("[Channel Error]: ", err)
        
        # await self.send(text_data=json.dumps({
        #     'type':'initialized',
        #     'message':"success"
        # }))

    def receive(self, text_data=None):
        data = json.loads(text_data)
        channelId = data['channelId']
        status = data['status']
        channel_info = ChannelsManagement().find_by_id(id=channelId)
        ChannelsManagement().update_by_id(id=channelId, status=status)
        
        async_to_sync(self.channel_layer.group_send)(
            'homegroup_{0}'.format(self.home_id),
            {
                'type':'device_message',
                'deviceStatus': {}
            }
        )

        

    def device_message(self, event):
        device_channel_list = DevicesManagement().find_by_all_homeId(home_id=self.home_id)
        self.send(text_data=json.dumps({
            'type':'deviceInfo',
            'deviceStatus': device_channel_list
        }))


    # def disconnect(self, code):
    #     async_to_sync(self.channel_layer.group_discard)(self.home_room_group_name, self.channel_name)

    # async def onOpen_message(self):

    #     await self.send(text_data=json.dumps({
    #         "data":{
    #             "home": 1,
    #             "room": 2,
    #             "devices": [
    #                 {
    #                     "id": 1,
    #                     "key": 123,
    #                     "type": "control",
    #                     "status": [
    #                         {"value": True}
    #                     ]
    #                 }
    #             ]
    #         }
    #     }))