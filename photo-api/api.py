from flask import Flask, request, jsonify
import io
import sys
from PIL import Image

sys.stderr = sys.stdout


def create_app():
    # Flask
    app = Flask(__name__)
    app.config['DEBUG'] = False
    return app


app = create_app()


@app.route("/photo-api/v0.1/photo", methods=['POST'])
def photo_upload():
    try:
        photo = request.files.get('photo')

        Image.MAX_IMAGE_PIXELS = None
        ratio = 0.5

        image = Image.open(io.BytesIO(photo.read()))
        new_dimensions = (int(round(image.size[0] * ratio)), int(round(image.size[1] * ratio)))

        new_image = image.resize(new_dimensions, Image.ANTIALIAS)
        new_image.format = image.format
        new_image.save('new_photo.jpg')
    except Exception:
        return jsonify({'success': False, 'error': str(e)})

    return jsonify({'success': True})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
