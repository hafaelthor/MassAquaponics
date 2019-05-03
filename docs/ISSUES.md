#IoT App
## Database Models
Community Broker
- I really want to make the CharFields of name and host non-empty. I've tried to set blank=False to use MinLengthValidator(1) etc. but it doesn't seem to work.
## Consumers
Community Broker Consumer
- I'm not sure if the is_connected flag is actually working.
- I never tested a reconnection, maybe the is_initialized flag should be a is_connecting flag so the loop won't try to repeatedly reconnect "overflowing" the connection function (if that's
a thing).