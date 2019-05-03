from paho.mqtt.client import Client
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

#list of topics involved in the MQTT communication
GREET_TOPIC         = 'init'
SYSGREET_TOPIC      = '{pk}/grt'
BIOINFO_TOPIC       = '{pk}/bio'
ACTION_TOPIC        = '{pk}/act'
AUTOACTION_TOPIC    = '{pk}/act/aut'
SETTING_TOPIC       = '{pk}/set'
SYSGREET_TOPIC_RE   = r'(?P<pk>\d+)/grt'
BIOINFO_TOPIC_RE    = r'(?P<pk>\d+)/bio'
ACTION_TOPIC_RE     = r'(?P<pk>\d+)/act'
AUTOACTION_TOPIC_RE = r'(?P<pk>\d+)/act/aut'
SETTING_TOPIC_RE    = r'(?P<pk>\d+)/set'

class CommunityBrokerConsumer (Client):
    '''
    The CommunityBrokerConsumer is a specialized type
    of Paho MQTT Client that enables the communication
    between the server and the systems inside a given
    community. It connects with one of the brokers
    registered in the Database Model CommunityBroker
    (iot.models.CommunityBroker)

    Constructor Inputs
    ------------------
    - community iot.models.CommunityBroker
    '''

    MQTT_ID         = 'SERVER'
    is_initialized  = False
    is_connected    = False
    channel_layer   = get_channel_layer()

    def __init__ (self, community):
        '''
        Uses the community information as a core info of the
        consumer to know the credentials and web address of the
        broker and then tries connection. It also adds the systems
        to the userdata information of the consumer.

        Inputs
        ------
        - community iot.models.CommunityBroker
        '''

        # WARNING: 
        # The System Model is not yet implemented, so we
        # are creating inline classes to represent what we are 
        # already using of the System Model, the primary key (pk) 
    
        #setting community as core info
        self.info = community
        #starts MQTT Client in superclass
        super().__init__(self.MQTT_ID, userdata=[type('System', (object,), {'pk' : 1})])
        #set credentials if existing
        if self.info.cred_username and self.info.cred_password:
            self.username_pw_set(self.info.cred_username, self.info.cred_password)
        #try connection
        try: self.connect(self.info.host, self.info.port)
        except: self.is_initialized = True
    
    def on_connect (self, client, systems, flags, rc):
        '''
        Sets is_initialized=True and is_connected=True, listens to all
        currently registered systems and sends the greet topic ("init")
        to ask all systems to "greet" back and update information of
        each particular system.
        '''

        #setting flags
        self.is_initialized = True
        self.is_connected = True
        #listen to each registered system
        for system in systems: self.listen_system(system)
        #greet to the systems
        self.publish(GREET_TOPIC)
    
    def on_disconnect (self, client, systems, flags, rc):
        '''
        Handles disconnection by setting is_connected=False
        ''' 
        self.is_connected = False

    def listen_system (self, system, new_system=False):
        '''
        Adds the system's namespace (<pk>/*) to the MQTT subscriptions
        and itself to the systems the consumer can control. Basically,
        it opens communication with the system.

        Inputs
        ------
        - system        iot.models.AquaponicSystem (unimplemented)
        - new_system    bool (True if system wasn't already registered)
        '''

        #subscribe to the "<pk>/*" namespace
        for topic, callback in [(BIOINFO_TOPIC, self.on_bioinfo),
            (AUTOACTION_TOPIC, self.on_autoaction), (SYSGREET_TOPIC, self.on_sysgreeting)]:
            self.subscribe(topic.format(pk=system.pk))
            self.message_callback_add(topic.format(pk=system.pk), callback)
        #add the system to the userdata systems
        if new_system: self._userdata.append(system)
        else: pass
    
    def mute_system (self, system):
        '''
        Removes the system's namespace (<pk>/*) from the MQTT subscriptions
        and itself from the systems the consumer can control. Basically,
        it shuts off communication with the system.

        Inputs
        ------
        - system    iot.models.AquaponicSystem (unimplemented)
        '''

        #unsubscribe to the "<pk>/*" namespace
        for topic in [BIOINFO_TOPIC, AUTOACTION_TOPIC, SYSGREET_TOPIC]:
            self.unsubscribe(topic.format(pk=system.pk))
            self.message_callback_remove(topic.format(pk=system.pk))
        #try to remove the system from the userdata systems
        try: self._userdata.remove(system)
        except: pass

    #Especific Communication Methods (unimplemented)
    def on_bioinfo (self, client, systems, data): 
        '''
        (unimplemented)
        Handles the "<pk>/bio" topic wich has the 
        measurements of biological and environmental factor 
        taken from each sensor.
        '''

        pass

    def on_autoaction (self, client, systems, data): 
        '''
        (unimplemented)
        Handles the "<pk>/act/aut" topic wich has the
        registry of every action taken by the system
        without user's instruction, automatically.
        '''
        
        pass

    def on_sysgreeting (self, client, systems, data): 
        '''
        (unimplemented)
        Handles the "<pk>/grt" topic wich receives
        information when a system connects or reconnects
        to the network. It'll give the status of each
        actor and the measures that weren't sent to
        make the server keep track of the actual state
        of the system despite connection issues.
        '''

        pass

    def send_action (self): 
        '''
        (unimplemented)
        Emits to the "<pk>/act" topic with an action instruction 
        for a single system to execute. It must have the system 
        specified, wich actor will be used and the data 
        necessary for the action.
        '''
        
        pass

    def send_settings (self): 
        '''
        (unimplemented)
        Emits to the "<pk>/set" topic with a setting 
        change for internal and autonomous system 
        control. It must have the system specified, wich
        setting will change and the new value of it.
        '''

        pass