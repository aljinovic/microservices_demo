from flask import Flask, request, jsonify
import io
import sys
from time import time
from PIL import Image

sys.stderr = sys.stdout


def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = False
    return app


app = create_app()


@app.route("/photo-api/v0.1/photo", methods=['POST'])
def photo_upload():
    start = time() * 1000

    photo = request.files.get('photo')

    Image.MAX_IMAGE_PIXELS = None
    ratio = 0.5

    image = Image.open(io.BytesIO(photo.read()))
    new_dimensions = (int(round(image.size[0] * ratio)), int(round(image.size[1] * ratio)))

    new_image = image.resize(new_dimensions, Image.ANTIALIAS)
    new_image.format = image.format
    new_image.save('new_photo.jpg')

    print('  - /photo-api/v0.1/photo | ' + str(round((time() * 1000 - start) / 1000, 2)) + 's')

    return jsonify({'success': True})
