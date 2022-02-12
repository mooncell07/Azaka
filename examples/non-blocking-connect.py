import asyncio

import azaka


async def main() -> None:

    client = azaka.Client()

    @client.register
    async def vn(ctx: azaka.Context) -> None:
        vn = await ctx.get_vn(lambda VN: VN.ID == 11)
        print(vn)

    await client.connect()


asyncio.run(main())
