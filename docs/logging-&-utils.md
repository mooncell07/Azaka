## Logging

Azaka writes logs for the events happening in the library at `DEBUG` level and also enables the
asyncio debug logger internally. Due to the nature of the library, it is recommended to keep logging ON to prevent any errors/events go silent.

Here we will use python's built-in [logging][] module to log the events:

```py
import logging

logging.basicConfig(level=logging.DEBUG)
```
