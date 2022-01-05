<p align="center"> <img src="https://cdn-icons-png.flaticon.com/512/2322/2322246.png" height=200> </p>

# WELCOME!

Welcome to Azaka, a work-in-progress asynchronous API wrapper around the [visual novel database](https://vndb.org/) written in python.

This wrapper is aimed to provide 100% API coverage being extremely simple to use and powerful. Now let's discuss why you should use it in next section.

# LINKS -

- [Features](https://github.com/mooncell07/Azaka#features--)
- [Problems](https://github.com/mooncell07/Azaka#problems--)
- [Installation](https://github.com/mooncell07/Azaka#installation--)
- [Usage](https://github.com/mooncell07/Azaka#usage--)
- [Docs. & Tuts.](https://github.com/mooncell07/Azaka#documentation--tutorial--)
- [Thanks](https://github.com/mooncell07/Azaka#thanks)

## FEATURES -

- **Fully Asynchronous** - Everything which poses a threat of blocking the I/O for a significant amount of time is async.
- **Caching** - Azaka supports caching responses, which saves us from getting throttled quickly!
- **Easy to Use** - Azaka provides a really easy to use interface for creating complex commands and a bunch of ready-made presets for those in hurry.
- **Global Exception handling** - Azaka provides utility for handling command errors globally to save you from try-except hell! Also it does alot behind the screen to save you from sending and receiving bad stuff anyways!
- **No Dependency requirement** - No third party dependency is required to do anything in entire library.


## PROBLEMS -

*(yes, i am a gud person)*

- **Bloat** - A few decisions have been taken which have caused the lib. to weigh too much but trust me, it's not dead weight, they help with UX.
- **Syntax Requirement** - I know, a lot of things are needed to be done even by the user to make it operational. I am working on fixing it.
- **Slow Development & bug hunting** - I am the only person working on entire lib and i have a lot of work irl too so sorrryyy.
- **Models are not well optimized** - All the models are fully constructed even if there is no need of some members. Working on it.
- **Support** - Well.. i can only help with it so yea you can contact me on discord `Nova#3379`.


## INSTALLATION -

You can install Azaka using pip.

`pip install -U azaka`

That's it! There is no other required requirement.

Additionally, you can also install

- [uvloop](https://pypi.org/project/uvloop/)
- [orjson](https://pypi.org/project/orjson/)

for speeding up the stuff!

## USAGE -

*Example of getting basic VN data.*

```py
import azaka
from azaka import VNCondition as VN

client = azaka.Client()

@client.register
async def main(ctx) -> None:
    vn = await client.get_basic_vn_info(VN.ID == 60)
    print(vn[0])

client.start()
```

Above example used a preset (`client.get_basic_vn_info`), you can use azaka's Interface to build a command yourself!

```py
import azaka
from azaka import Type, Flags

client = azaka.Client()

@client.register
async def main(ctx) -> None:
    with azaka.Interface(type=Type.VN, flags=(Flags.BASIC,)) as interface:
        VN = interface.condition()
        interface.set_condition((VN.SEARCH % "fate") & (VN.ID == 50))

    vn = await client.get(interface)
    print(vn[0])

client.start()
```

## DOCUMENTATION & TUTORIAL -

Documentation is still in development and will be available soon!


## THANKS

Thank you for your visit :)
