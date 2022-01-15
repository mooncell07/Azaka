## Logging

Azaka writes logs for the events happening in the library at `DEBUG` level and also enables the
asyncio debug logger internally. Due to the nature of the library, it is recommended to keep logging ON to prevent any errors/events go silent.

Here we will use python's built-in [logging][] module to log the events:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
```

This will write azaka, asyncio and other library's logs to the console.


## Discord Integration

Well, you can integrate Azaka with your discord bot easily!

For now i have only tested it with [hata](https://github.com/HuyaneMatsu/hata) (ver. `1.1.131`) so the following steps
will only work with hata, but there will be more soon!

### Hata

#### *Step 1: Install hata.*

Hata is available on [PyPi](https://pypi.org/project/hata/) so just install it with pip.

`pip install hata`

------

#### *Step 2: Create a bot application.*

From [Discord dev. portal](https://discord.com/developers/applications) create a bot application
and invite the bot to your server.

------

#### *Step 3: Install azaka.*

Assuming everything is working properly with the discord bot, now install azaka with pip as well.

`pip install azaka`

------

#### *Step 4: Create the hata and azaka Clients.*

Now construct azaka's and hata's `Client` and pass hata's event loop to the `loop` parameter of azaka's Client.

Like this:

```python
import hata
from hata.ext import asyncio
import azaka

hata_client = hata.Client("your_discord_token", extensions="commands_v2", prefix="!")
azaka_client = azaka.Client(loop=hata_client.loop)
```

------

#### *Step 5: Create a [asyncio.Future][] for azaka results.*

We need to do this because azaka uses callbacks and without it we won't be able to get the callback's
results.

so,

```python
import hata
from hata.ext import asyncio
import azaka

hata_client = hata.Client("your_discord_token", extensions="commands_v2", prefix="!")
azaka_client = azaka.Client(loop=hata_client.loop)
azaka_future = hata_client.loop.create_future()
```

------

#### *Step 6: Create a command and a callback for azaka.*
We need to create a command using hata to get input from discord and a callback to register to azaka
everytime this command is called.

EZ:

```python
import hata
from hata.ext import asyncio
import azaka

hata_client = hata.Client("your_discord_token", extensions="commands_v2", prefix="!")
azaka_client = azaka.Client(loop=hata_client.loop)
azaka_future = hata_client.loop.create_future()

async def fetch_vn(ctx: azaka.Context, name: str) -> None:
    result = await ctx.get_vn(lambda VN: VN.TITLE % name, details=True)
    azaka_future.set_result(result)

@hata_client.commands
async def vn(*msg: str) -> None:
    name = " ".join(msg)
    azaka_client.register(fetch_vn, name=name)  # register the callback to be called when this command is called and azaka is ready to issue it's own commands.
    result = await azaka_future

    azaka_future.clear()  # Clear the future to reuse it.
    return result  # Send the result to discord.
```

------


#### *Step 7: Start both the clients.*

Now just call the `start` method of both the clients and if everything went well, the program should be connected
to discord and VNDB!

You must start hata's client before azaka's.

```python
import hata
from hata.ext import asyncio
import azaka

hata_client = hata.Client("your_discord_token", extensions="commands_v2", prefix="!")
azaka_client = azaka.Client(loop=hata_client.loop)
azaka_future = hata_client.loop.create_future()

async def fetch_vn(ctx: azaka.Context, name: str) -> None:
    result = await ctx.get_vn(lambda VN: VN.TITLE % name, details=True)
    azaka_future.set_result(result)

@hata_client.commands
async def vn(*msg: str) -> None:
    name = " ".join(msg)
    azaka_client.register(fetch_vn, name=name)
    result = await azaka_future

    azaka_future.clear()
    return result

hata_client.start()
azaka_client.start()
```

------

Well that's it! If you are facing any trouble with hata then feel free to join their [support server](https://discord.com/invite/3cH2r5d) to ask! I'm there too btw :) (`Nova#3379`)

A working example of the above code can be found in my other repository [Serenity](https://github.com/mooncell07/Serenity/blob/master/azaka-maid/bot.py).
