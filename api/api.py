import asyncio
from aiohttp import web, ClientSession
import sys, io
from models import session, Contact
from PIL import Image

sys.stderr = sys.stdout


async def contact_create(request):
    new_contact = Contact(**await request.json())
    session.add(new_contact)
    session.commit()

    return web.json_response({'success': True, 'id': new_contact.id})


async def contact_edit(request):
    contact = session.query(Contact).filter_by(id=request.match_info.get('id')).first()

    for field, value in (await request.json()).items():
        setattr(contact, field, value)

    session.add(contact)
    session.commit()

    return web.json_response({'success': True})


async def contact_delete(request):
    contact = session.query(Contact).filter_by(id=request.match_info.get('id')).first()
    session.delete(contact)
    session.commit()

    return web.json_response({'success': True})


async def photo_upload(request):
    data = await request.post()
    photo = data['photo'].file.read()

    ratio = 0.5
    Image.MAX_IMAGE_PIXELS = None
    image = Image.open(io.BytesIO(photo))
    new_dimensions = (int(round(image.size[0] * ratio)), int(round(image.size[1] * ratio)))
    new_image = image.resize(new_dimensions, Image.ANTIALIAS)
    new_image.format = image.format
    new_image.save('new_photo.jpg')

    return web.json_response({'success': True})


async def photo_upload_v2(request):
    data = await request.post()
    photo_raw = data['photo'].file.read()

    asyncio.get_event_loop().create_task(call_photo_api(photo_raw))

    return web.json_response({'success': True})


async def call_photo_api(photo):
    photo_api_url = 'http://photo-api/photo-api/v0.1/photo'
    async with ClientSession() as aiohttp_session:
        async with aiohttp_session.post(photo_api_url, data={'photo': photo}) as _:
            pass


app = web.Application()
app.router.add_route('POST', '/api/v0.1/contact', contact_create)
app.router.add_route('PUT', '/api/v0.1/contact/{id}', contact_edit)
app.router.add_route('DELETE', '/api/v0.1/contact/{id}', contact_delete)
app.router.add_route('POST', '/api/v0.1/photo', photo_upload)
app.router.add_route('POST', '/api/v0.2/photo', photo_upload_v2)
