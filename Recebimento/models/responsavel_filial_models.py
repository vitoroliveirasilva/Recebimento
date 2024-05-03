from Recebimento import db

class ResponsavelFilial(db.Model):
    responsavel_id = db.Column(db.Integer, db.ForeignKey('responsavel.id'), primary_key=True)
    filial_id = db.Column(db.Integer, db.ForeignKey('filial.id'), primary_key=True)
