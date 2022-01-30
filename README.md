<p align="center"> <img src="https://cdn-icons-png.flaticon.com/512/2322/2322246.png" height=100> </p>
<p align="center"> <a href="https://www.codefactor.io/repository/github/mooncell07/azaka"><img src="https://www.codefactor.io/repository/github/mooncell07/azaka/badge" alt="CodeFactor" /></a> </p>

# WELCOME!

Welcome to Azaka, a work-in-progress asynchronous API wrapper around the [visual novel database](https://vndb.org/) written in python.

This wrapper is aimed to provide 100% API coverage being extremely simple to use and powerful. Now let's discuss why you should use it in next section.

# LINKS

- [WELCOME!](#welcome)
- [LINKS](#links)
  - [FEATURES](#features)
  - [PROBLEMS](#problems)
  - [INSTALLATION](#installation)
  - [USAGE](#usage)
  - [DOCUMENTATION & TUTORIAL](#documentation--tutorial)
  - [THANKS](#thanks)

## FEATURES

- **Fully Asynchronous** - Everything which poses a threat of blocking the I/O for a significant amount of time is async.
- **Single Connection** - Everything is handled by a single connection to the API and it is reused
(if it was not closed by the user). Giving your IP more amount of connections.
- **Easy to Use** - Azaka provides a really easy to use interface for creating complex commands and a bunch of ready-made presets.
- **Well Typehinted** - Everything in this library is properly typehinted.
- **No Dependency Requirement** - No third party dependency is required to do anything in entire library.


## PROBLEMS

*(yes, i am a gud person)*

- **Bloat** - A few decisions have been taken which have caused the lib. to weigh too much but trust me, it's not dead weight, they help with UX.
- **Slow Development & bug hunting** - I am the only person working on entire lib and i have a lot of work irl too so sorrryyy.
- **Models are not well optimized** - All the models are fully constructed even if there is no need of some members.
- **Support** - Well.. i can only help with it so yea you can contact me on discord `Nova#3379`.


## INSTALLATION

You can install Azaka using pip.

`pip install -U azaka`

That's it! There is no other required requirement.

Additionally, you can also install

- [uvloop](https://pypi.org/project/uvloop/)
- [orjson](https://pypi.org/project/orjson/)

for speeding up the stuff!

## USAGE

*Example of getting basic VN data.*

```py
import azaka

client = azaka.Client()

@client.register
async def main(ctx) -> None:
    vn = await ctx.get_vn(lambda VN: VN.ID == 11)
    print(vn[0])

client.start()
```

Above example used a preset (`client.get_vn`), you can use azaka's Interface to build a command yourself!

```py
import azaka
from azaka import Flags

client = azaka.Client()

@client.register
async def main(ctx) -> None:
    with azaka.Interface(type=ctx.vn, flags=(Flags.BASIC,)) as interface:
        interface.set_condition(lambda VN: (VN.SEARCH % "fate") & (VN.ID == 50))

    vn = await client.get(interface)
    print(vn[0])

client.start()
```

## DOCUMENTATION & TUTORIAL

Documentation can be found [here](https://mooncell07.github.io/Azaka/).


## THANKS

Thank you for your visit :)
