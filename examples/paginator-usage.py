import azaka

client = azaka.Client()


@client.register
async def main(ctx: azaka.Context) -> None:
    interface = azaka.Interface(type=ctx.vn, flags=(azaka.Flags.BASIC,))
    interface.set_condition(lambda VN: VN.SEARCH % "fate")

    paginator: azaka.Paginator = azaka.Paginator(client, interface)

    async for page in paginator:
        if (
            paginator.current_page_num < 3
        ):  # Not necessary, i did it to avoid getting throttled.
            print(page)
        else:
            break


client.start()
