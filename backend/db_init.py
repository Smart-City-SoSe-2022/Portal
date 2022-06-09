from app import app, db

with app.test_request_context():
    db.init_app(app)
    db.drop_all()
    db.create_all()

print("Done!")
