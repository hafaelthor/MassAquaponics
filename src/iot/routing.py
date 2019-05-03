from threading import Thread

from .models import CommunityBroker
from .consumers import CommunityBrokerConsumer

class BrokerHub (Thread):
    '''
    The BrokerHub is a thread running in the background 
    handling all the MQTT clients (CommunityBrokerConsumer)
    and enabling the IoT Communication via MQTT.
    '''
    
    def __init__ (self):
        '''
        Create the CommunityBrokerConsumer instances, connect then
        to each MQTT Broker and track then by the Broker Primary
        Key in the Database (CommunityBroker.pk) in the clients list
        '''

        Thread.__init__(self)
        self.clients = dict([(community.pk, CommunityBrokerConsumer(community)) 
            for community in CommunityBroker.objects.all()])

    def run (self):
        '''
        The main loop of the BrokerHub thread will be making the MQTT 
        Client loop() for each CommunityBrokerConsumer instance and 
        manage connection so it'll be connected everytime it's possible. 
        '''
        
        while True:
            for client in self.clients.values(): 
                #MQTT Loop
                client.loop()
                #Keep up connection with the broker
                if client.is_initialized and not client.is_connected: 
                    try: client.reconnect()
                    except: pass

def send_action (self): 
    '''
    (unimplemented)
    Send action instruction for a single system to execute.
    It must have the system specified, wich actor will
    be used and the data necessary for the action.
    '''
    
    pass

def send_setting (self): 
    '''
    (unimplemented)
    Change setting for internal and autonomous system 
    control. It must have the system specified, wich
    setting will change and the new value of it.
    '''
    
    pass

def listen_system (self):
    '''
    (unimplemented)
    Adds the system's namespace to the MQTT subscriptions
    and itself to the systems the consumer can control. Basically,
    it opens communication with the system 
    '''

    pass

def mute_system (self):
    '''
    (unimplemented)
    Removes the system's namespace from the MQTT subscriptions
    and itself from the systems the consumer can control. Basically,
    it shuts off communication with the system.
    '''

    pass

'''
Open Functions (unimplemented):
Will be the gateway from the server to each 
community and, therefore, each registered system.
The communication needed in this direction will 
support:
- settings change, 
- send actions and 
- listen or mute particular systems
'''

#create and run BrokerHub thread
hub = BrokerHub()
hub.start()