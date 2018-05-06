import io
from PIL import Image
import requests
import sys
from flask import Flask, request, jsonify
from models import db, Contact

sys.stderr = sys.stdout


def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app, db


app, db = create_app()


@app.route("/api/v0.1/contact", methods=['POST'])
def contact_create():
    try:
        db.session.add(Contact(**request.json))
        db.session.commit()
    except Exception:
        raise
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Error creating contact.'})

    return jsonify({'success': True})


@app.route("/api/v0.1/contact/<uid>", methods=['PUT'])
def contact_edit(uid):
    try:
        contact = Contact.query.filter_by(id=uid).first()

        for field, value in request.json.items():
            setattr(contact, field, value)

        db.session.add(contact)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Error updating contact.'})

    return jsonify({'success': True})


@app.route("/api/v0.1/contact/<uid>", methods=['DELETE'])
def contacts_delete(uid):
    try:
        contact = Contact.query.filter_by(id=uid).first()
        db.session.delete(contact)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Error deleting contact.'})

    return jsonify({'success': True})


@app.route("/api/v0.1/photo", methods=['POST'])
def photo_upload():
    try:
        photo = request.files.get('photo').read()

        Image.MAX_IMAGE_PIXELS = None
        ratio = 0.5

        image = Image.open(io.BytesIO(photo))
        new_dimensions = (int(round(image.size[0] * ratio)), int(round(image.size[1] * ratio)))

        new_image = image.resize(new_dimensions, Image.ANTIALIAS)
        new_image.format = image.format
        new_image.save('new_photo.jpg')
    except Exception:
        return jsonify({'success': False, 'error': str(e)})

    return jsonify({'success': True})


@app.route("/api/v0.2/photo", methods=['POST'])
def photo_upload_v2():
    photo_raw = request.files.get('photo')
    response = requests.post('http://localhost:82/photo-api/v0.1/photo', files={'photo': photo_raw})

    return jsonify(response.json())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
