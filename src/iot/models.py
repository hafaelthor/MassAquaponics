from django.db.models import Model, CharField, IntegerField
from django.core.validators import MinLengthValidator

# Create your models here.

class CommunityBroker (Model):
    '''
    The CommunityBroker will store the information
    necessary to connect to an MQTT broker wich 
    intermediates communication between the server 
    and each system inside a community.
    '''

    #The public name of the community
    name            = CharField(max_length=20)
    #Address where the MQTT broker resides
    host            = CharField(max_length=30)
    port            = IntegerField()
    #Optional broker credentials to add cyber security for the community
    cred_username   = CharField(max_length=20, null=True)
    cred_password   = CharField(max_length=20, null=True)
    #if credentials aren't used, set 
    #cred_username=None; cred_password=None

    def __repr__ (self):
        return f'<COMMUNITY BROKER {self.pk} | {self.name} on {self.host}:{self.port}>'