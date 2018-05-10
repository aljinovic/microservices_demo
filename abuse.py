import asyncio
from aiohttp import ClientSession
import sys

index = 1
file = open('LARGE_IMAGE.jpg', 'rb').read()

async def call_photo_api(version):
    global index
    global file

    photo_api_url = f'http://0.0.0.0:81/api/{version}/photo'
    async with ClientSession() as aiohttp_session:
        async with aiohttp_session.post(photo_api_url, data={'photo': file}) as _:
            print(f'  - response #{index}')
            index += 1


async def abuse():
    for i in range(20):
        tasks = []
        for _ in range(10):
            tasks.append(call_photo_api(sys.argv[1]))

        await asyncio.gather(*tasks)


loop = asyncio.get_event_loop()
loop.run_until_complete(abuse())
