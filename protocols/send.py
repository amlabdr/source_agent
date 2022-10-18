#standards imports
import json

#imports to use AMQP 1.0 communication protocol
from proton import Message
from proton.handlers import MessagingHandler

class Send(MessagingHandler):
    def __init__(self, server, topic, messages):
        super(Send, self).__init__()
        self.server = server
        self.topic = topic
        self.confirmed = 0
        self.data = messages
        self.total = 1

    def on_connection_error(self, event):
        return super().on_connection_error(event)
    
    def on_transport_error(self, event) -> None:
        return super().on_transport_error(event)
        
    def on_start(self, event):
        conn = event.container.connect(self.server)
        event.container.create_sender(conn, self.topic)
   
    def on_sendable(self, event):
        msg = Message(body=json.dumps(self.data))
        event.sender.send(msg)
        event.sender.close()
        
    def on_rejected(self, event):
        return super().on_rejected(event)
        
    def on_accepted(self, event):
        self.confirmed += 1
        if self.confirmed == self.total:
            event.connection.close()
    

    def on_disconnected(self, event):
        self.sent = self.confirmed