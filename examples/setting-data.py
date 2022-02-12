"""
Setting data requires authentication. You can either use password or session token. Username
is a required parameter in both the cases.

For this example i am assuming that you have a password and username.
"""

import azaka

client = azaka.Client(username="your_username", password="your_password")


@client.register
async def main(ctx: azaka.Context) -> None:
    interface = azaka.SETInterface(id=50)
    interface.write_notes("This is a test note.")

    response_type = await client.set(interface)
    print(response_type)


client.start()
