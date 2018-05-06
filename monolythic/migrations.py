from models import db, Contact
from faker import Factory


def run_migrations():
    fake = Factory.create('hr_HR')

    db.drop_all()
    db.create_all()

    for _ in range(100):
        fullname = fake.name().split()

        db.session.add(Contact(
            name=fullname[0],
            surname=' '.join(fullname[1:]),
            email=fake.email(),
            phone=fake.phone_number()
        ))

    db.session.commit()
