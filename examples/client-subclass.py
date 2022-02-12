import azaka
import typing as t


class MyClient(azaka.Client):
    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        super().__init__(*args, **kwargs)
        self.register(self.main)

    async def main(self, ctx: azaka.Context) -> None:
        vn = await ctx.get_vn(lambda VN: VN.ID == 11)
        print(vn)


client = MyClient()
client.start()
