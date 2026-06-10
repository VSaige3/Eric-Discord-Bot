import asyncio

async def a():
    await asyncio.sleep(1)
    print("hello")
async def b():
    print("goodbye")

async def c():
    await asyncio.gather(a(), b())

asyncio.run(c())