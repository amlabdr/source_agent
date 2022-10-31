#standards imports
import json, datetime, traceback, logging

#imports to use AMQP 1.0 communication protocol
from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import Container
from utils.source import CLD1015
from utils.send import Send


class RecvSpecification(MessagingHandler):
    def __init__(self, server,topic,serialNumber):
        super(RecvSpecification, self).__init__()
        self.server = server
        self.topic = topic
        self.serialNumber=serialNumber
        
        
        
    def on_start(self, event):
        conn = event.container.connect(self.server)
        event.container.create_receiver(conn, self.topic)
        
    def on_message(self, event):
        try:
            jsonData = json.loads(event.message.body)
            logging.info("Analyzer will send receipt to the controller")
            
            endpoint=jsonData['endpoint']
            name = jsonData['name']
            when = jsonData['when']
            capability = jsonData['capability']
            logging.info("specification received for {}".format(capability))
            logging.info("Agent will send receipt to the controller for {}".format(capability))
           
            #agent will publish a receipt for spec
            specification_receiptData=jsonData.copy()
            
            specification_receiptData['receipt'] = jsonData['specification']
            del specification_receiptData['specification']
            topic = event.message.reply_to
            Container(Send(self.server,topic, specification_receiptData)).run()
            logging.info("agent will do the {}".format(capability))
            #agent will do the measurement/commanding
            self.source = CLD1015(self.serialNumber)
            if self.source.connected:
                
                if capability == "measure":
                    status=self.source.show_status()
                    result_msg = jsonData.copy
                    result_msg['result'] = result_msg['specification']
                    del result_msg['specification']
                    result_msg['resultValues'] = status
                    logging.info("Agent will send result {} to the controller".format(result_msg['resultValues']))
                    result_topic = 'topic:///multiverse/qnet/source/results'################
                    Container(Send(self.server,result_topic, result_msg)).run()

                elif capability == "command":
                    self.source.laser_on()
                else:
                    pass
            else:
                logging.info("Cannot connect to source {}".format(self.serialNumber))
        except Exception:
            traceback.print_exc()
            