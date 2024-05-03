from Recebimento import app, db
from Recebimento.models import Responsavel

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0')
