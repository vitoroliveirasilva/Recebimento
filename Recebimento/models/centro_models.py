from Recebimento import db
from .filial_models import Filial

class Centro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    filial_id = db.Column(db.Integer, db.ForeignKey('filial.id'))
    filial = db.relationship('Filial', backref=db.backref('centros', lazy=True))

    @classmethod
    def register_centro(cls, data):
        filial = Filial.query.get(data['filial'])
        new_centro = cls(nome=data['nome'], filial=filial)
        db.session.add(new_centro)
        return new_centro