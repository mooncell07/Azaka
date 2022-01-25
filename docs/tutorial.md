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
- **Condition** - Azaka has many `Condition` classes which contain fields which support various operators.

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
