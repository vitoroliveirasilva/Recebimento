from Recebimento import db
from .filial_models import Filial
from .centro_models import Centro

class NotaFiscal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chave_acesso = db.Column(db.String(255), unique=True)
    cnpj = db.Column(db.String(255))
    nf = db.Column(db.String(255))
    codigo_cte = db.Column(db.String(255))
    volumes = db.Column(db.Integer)
    filial_id = db.Column(db.Integer, db.ForeignKey('filial.id'))
    centro_id = db.Column(db.Integer, db.ForeignKey('centro.id'))
    filial = db.relationship('Filial', backref=db.backref('notas_fiscais', lazy=True))
    centro = db.relationship('Centro', backref=db.backref('notas_fiscais', lazy=True))
