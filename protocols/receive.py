#standards imports
import json, logging

#imports to use AMQP 1.0 communication protocol
from proton import Message
from proton.handlers import MessagingHandler
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
        None
        
        #implementing the local script