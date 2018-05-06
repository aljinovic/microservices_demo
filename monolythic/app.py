from flask import Flask, redirect, url_for, render_template, request, flash
from models import db, Contact
from forms import ContactForm
from migrations import run_migrations


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'my secret'
    app.config['DEBUG'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    run_migrations()  # Create some fake data
    return app, db


app, db = create_app()


@app.route("/")
def contacts():
    all_contacts = Contact.query.order_by(Contact.name).all()
    return render_template('web/contacts.html', contacts=all_contacts)


@app.route('/contacts/new', defaults={'uid': None}, methods=['GET', 'POST'])
@app.route("/contacts/edit/<uid>", methods=('GET', 'POST'))
def edit_contact(uid=None):
    my_contact = Contact.query.filter_by(id=uid).first() if uid else None
    form = ContactForm(obj=my_contact)

    if form.validate_on_submit():
        if not my_contact:
            my_contact = Contact()

        try:
            form.populate_obj(my_contact)
            db.session.add(my_contact)
            db.session.commit()
            flash('Saved successfully', 'success')

            if uid:
                return redirect(url_for('contacts'))
        except:
            db.session.rollback()
            flash('Error saving contact.', 'danger')

    return render_template('web/edit_contact.html', form=form)


@app.route("/search")
def search():
    name_search = request.args.get('name')
    all_contacts = Contact.query.filter(Contact.name.contains(name_search)).all()

    return render_template('web/contacts.html', contacts=all_contacts)


@app.route("/contacts/delete", methods=['POST'])
def contacts_delete():
    try:
        db.session.delete(Contact.query.filter_by(id=request.form['id']).first())
        db.session.commit()
        flash('Delete successfully.', 'danger')
    except:
        db.session.rollback()
        flash('Error delete  contact.', 'danger')

    return redirect(url_for('contacts'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
