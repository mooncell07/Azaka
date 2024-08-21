<p align="center"> <img src="https://cdn-icons-png.flaticon.com/512/3276/3276136.png" height=100> </p>

<p align="center">
<img alt="Stargazers" src="https://img.shields.io/github/stars/mooncell07/Azaka?style=for-the-badge&logo=starship&color=C9CBFF&logoColor=D9E0EE&labelColor=302D41">
<img alt="Issues" src="https://img.shields.io/github/issues/mooncell07/Azaka?style=for-the-badge&logo=gitbook&color=B5E8E0&logoColor=D9E0EE&labelColor=302D41">
<img alt="Releases" src="https://img.shields.io/github/license/mooncell07/Azaka?style=for-the-badge&logo=github&color=F2CDCD&logoColor=D9E0EE&labelColor=302D41"/>
<img alt="Version" src="https://img.shields.io/pypi/v/azaka?style=for-the-badge&logo=github&color=89dceb&logoColor=D9E0EE&labelColor=302D41">

</p>

# LINKS

- [WELCOME!](#welcome)
  - [FEATURES](#features)
  - [INSTALLATION](#installation)
  - [USAGE](#usage)
  - [DOCUMENTATION & TUTORIAL](#documentation--tutorial)
  - [THANKS](#thanks)

# WELCOME!

Welcome to Azaka, a work-in-progress asynchronous and thin API Wrapper around the [visual novel database](https://vndb.org/) written in python.


## FEATURES

- **Fully Asynchronous** - The library supports Async. communication and other jobs.
- **Clean and Expressive** - Azaka's syntax is 
really clean and expressive with SQL like querying.
- **Well Typehinted & Tested** - Everything in the library is properly typehinted and checked with strict mypy type checking strategy. However there are few exceptions ;)

## INSTALLATION

You can install Azaka using pip.

`pip install azaka`

## USAGE

*Example of getting some basic VN data.*

```py
import asyncio
from azaka import Client, Node, select

query = (
    select("title", "image.url")
    .frm("vn")
    .where(Node("id") == "v17")
)

async def main() -> None:
    async with Client() as client:
        resp = await client.execute(query=query)
        vn = resp.results[0]
        print(vn.id, vn.title, vn.image["url"], sep="\n")

asyncio.run(main())
```

## DOCUMENTATION & TUTORIAL

Documentation will be available soon.


## THANKS

Thank you for your visit :)
