from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import iot.routing
'''
the Iot Application and consumers won't be 
routed by the ProtocolTypeRouter for applications
because of the known differences that it
has in relation to the other ASGI Applications:

IOT PROTOCOL            X       ASGI APPLICATIONS
Server-Machine          X       Server-User
External Server         X       Hosted with the WSGI Applications
Multiples Servers       X       A single ASGI Server

Instead, the IoT Application will run in the back
in a separate thread handling all MQTT clients,
connections and communications. It'll communicate
with the other consumers and ASGI applications
using the redis channel layers and group communication
inside each channels ASGI consumer.
'''

application = ProtocolTypeRouter({})
'''
ASGI Application:
we'll use this to route the ASGI Applications
in the website. for example, the 'websocket'
<protocol> for the future dashboard <app>
the usage might be as follows:
'<protocol>': AuthMiddlewareStack(
    URLRouter(<app>.routing.<protocol>_urlpatterns))
'''