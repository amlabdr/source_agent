#standards imports
import json, datetime, traceback

#imports to use AMQP 1.0 communication protocol
from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import Container
from send import Send

class RecvSpecification(MessagingHandler):
    def __init__(self, server,topic):
        super(RecvSpecification, self).__init__()
        self.server = server
        self.topic = topic
        
        
    def on_start(self, event):
        conn = event.container.connect(self.server)
        event.container.create_receiver(conn, self.topic)
        
    def on_message(self, event):
        try:
            jsonData = json.loads(event.message.body)
            endpoint=jsonData['endpoint']
            name = jsonData['name']
            when = jsonData['when']
            capability = jsonData['capability']
            exec_time = datetime.strptime(when, '%Y-%m-%d %H:%M:%S.%f')
            #2022-05-23 18:03:19.461738'

            #agent will publish a receipt for spec
            specification_receiptData=jsonData.copy()
            specification_receiptData['receipt'] = jsonData['specification']
            del specification_receiptData['specification']
            topic = event.message.reply_to
            Container(Send(self.server,topic, specification_receiptData)).run()

        except Exception:
            traceback.print_exc()