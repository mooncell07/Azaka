# Basics

## Creating a VNDB account.

Even though it is not *compulsory* to have a VNDB account it is needed at a few sections so it is
recommended to create one.

For creating an account at VNDB you need to go to the [VNDB Website](https://vndb.org/u/register).

## VNDB API & Azaka

VNDB exposes it's API through a Bi-Directional TCP connection through which all the transactions
of request and response are made. A session is made when a `login` command is sent to the API and
can stay alive forever so you don't have to login every time you want to make a request!

Azaka internally handles most of the connection related operations and exposes a simple interface to
the users so you don't have to care much about connection related stuff.

## Terminology

Below are few terms which are used in this documentation.

- **Command** - A command is a request to the VNDB API to perform a specific action.
- **Connection** - A link between the client and the VNDB API which in this context is made up of a
Secured TCP network protocol.
- **Interface** - An abstraction of lower level `get` and `set` methods to make it easier to make complex commands.
- **Condition** - Azaka has many `Condition` classes which contain fields which support various operations.

## Connection Begins!

Now it's time to make the wrapper do something!

Let's start by importing the library.

```py
import azaka
```

Now let's create a `Client` object.

```py
client = azaka.Client()
```

The `Client` object is the main entry point to the library and also you can pass
your username and password to the constructor to login as that user.

Now that we have a `Client` object we can register our coroutines to be called by the lib!

```py
@client.register
async def main(ctx: azaka.Context) -> None:
    await client.wait_until_connect() # Wait until we are connected to the VNDB API.
    print("Connected!")
```

`client.register` is a decorator which registers a coroutine to be called by the library. It
also puts `azaka.Context` object in the coroutine's 0th argument.

We just need one more thing to connect to the API!

```py
client.start() # This method *blocks* forever.
```

That's it! Now just run the script and you should be able to see `Connected!` printed soon!

----------

# Commands and Conditions

So now that you know how to use the library to connect to the API,
let's now make a simple command which will get information from the VNDB API.

A command is a request to the API to perform a specific action and the lib
provides an interface to make these things easily, so let's see how to use it!

But before that let's first import the [enum.Enum][] `Flags` for setting up flags.

*Flags are used to specify what information you want to fetch.*

```py
from azaka import Flags
```

Now we can use flags like `Flags.BASIC`, `Flags.DETAILS` etc. In case you want to
know what flags fetch what information then just read the documentation of the object
you are getting. There are `FLAGS: X` headings given and also there is a table below
each of them which tell what attributes will get a value sent by the API.

Now let's create an interface which will get DETAILS of a specific VN.

```py
@client.register
async def main(ctx):
    # In type parameter you can pass one of the types context has.
    # You can pass more flags in the tuple too like `flags=(Flags.BASIC, Flags.DETAILS)`
    with azaka.Interface(type=ctx.vn, flags=(Flags.DETAILS,)) as interface:
        ...
```

We now have an interface which will produce an incomplete command which will look like this!

`vn details`

And yeah you can use `Interface` as a context manager too! Looks good right?!
Let's proceed!

Now that type and flags are set, it's time to put up some conditions.
But how conditions work in azaka? Well, it is
really simple.

Let's put up a simple condition which we will unbreak!

```py
@client.register
async def main(ctx):
    with azaka.Interface(type=ctx.vn, flags=(Flags.DETAILS,)) as interface:
        interface.set_condition(lambda VN: VN.ID == 1)
```

We use `Interface.set_condition` method to set up a condition. We either pass a callable
to it which accepts a single argument of a subclass of `BaseCondition` or pass in a `BoolOProxy`
object which will be used as a condition.

`BoolOProxy` object should never be created by a user. It is generated when you condition a field
of BaseCondition against a value. So something like this:
```py
from azaka import VNCondition

my_condition = VNCondition.ID == 1
print(type(my_condition))

o/p

<class 'azaka.commands.proxy.BoolOProxy'>
```

Now you can pass this condition to the interface!


```py
@client.register
async def main(ctx):
    with azaka.Interface(type=ctx.vn, flags=(Flags.DETAILS,)) as interface:
        interface.set_condition(my_condition)
```

This one is exactly the same as previous one so, it's upon you what you wanna use!
I will be using lambda functions for this tutorial.

*For callback `lambda` should be preferred.*

VNDB also allows usage of the logical `AND` and `OR` operators and for that i abused the
syntax of `&` and `|` operators :)

And another operator `~` for searching substrings for which i abused the `%` operator.
So, just for demonstration purposes:

```py
@client.register
async def main(ctx):
    with azaka.Interface(type=ctx.vn, flags=(Flags.DETAILS,)) as interface:
        interface.set_condition(
            lambda VN: ((VN.TITLE % "reeeee") & (VN.ORIG_LANG != ["en", "ja"])) | (VN.ID > 4)
        )
```

Logic for above condition will be... vn's title should be like "reeeee" and vn's original language
should be either "en" (english) or "ja" (japanese). Well there ain't any VN named "reeeee" as of now
so that's a `False` and that is why it will not check original language. so it's like
`False or VN.ID > 4` now, there are ids present which are more than `4` so that's a `True` and it will
return all the VNs which have id more than 4. You will have to consider the operator precedence. Azaka
handles all the parsing.

Now let's continue!

`azaka.Interface` also provides options, to use them use `Interface.add_option` method.
You can look at it's documentation to see what options are available.

Ok so i just want API to return 2 VNs in the response and their names should match the word `"fate"`
but API will return like 10 of them in a single response! So, let's add an option for that!

```py
@client.register
async def main(ctx):
    with azaka.Interface(type=ctx.vn, flags=(Flags.DETAILS,)) as interface:
        interface.set_condition(lambda VN: VN.TITLE % "fate")
        interface.add_option(results=2) # This will tell API to return 2 VNs.
```

Now we have an interface which has type of `VN` and a flag `DETAILS`
with a condition and an option! Let's see how it looks like now in command form!

`vn details (title ~ "fate"){"results": 2}`

Nice! We are really close to issuing our first command!
Now we just have to call the `Client.get` method and pass our interface as an argument.

```py
@client.register
async def main(ctx):
    with azaka.Interface(type=ctx.vn, flags=(Flags.DETAILS,)) as interface:
        interface.set_condition(lambda VN: VN.TITLE % "fate")
        interface.add_option(results=2)
    result = await client.get(interface)
    print(result)
```

And that's it! We are ready to go! Our command will look like this now:

`get vn details (title ~ "fate"){"results": 2}`

Let's put our boilerplate code back in place now to run the script.


```py
import azaka
from azaka import Flags


client = azaka.Client()


@client.register
async def run_on_connect(ctx: azaka.Context) -> None:
    await client.wait_until_connect()
    print("Connected!")


@client.register
async def main(ctx: azaka.Context) -> None:
    with azaka.Interface(type=ctx.vn, flags=(Flags.DETAILS,)) as interface:
        interface.set_condition(lambda VN: VN.TITLE % "fate")
        interface.add_option(results=2)
    result = await client.get(interface)
    print(result)


client.start()
```

Now run it and you will see the message `Connected!` and then the result which will be a list of
2 `VN` objects!
