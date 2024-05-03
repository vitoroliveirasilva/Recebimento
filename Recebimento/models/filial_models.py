from Recebimento import db

class Filial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    responsaveis_filial = db.relationship('ResponsavelFilial', backref='filial')

    @classmethod
    def check_filial_existence(cls, nome):
        return cls.query.filter_by(nome=nome).first() is not None

    @classmethod
    def register_filial(cls, data):
        new_filial = cls(nome=data['nome'])
        db.session.add(new_filial)
        return new_filial
