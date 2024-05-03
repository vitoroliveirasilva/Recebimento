from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from Recebimento import db

class Responsavel(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    usuario = db.Column(db.String(255), unique=True, nullable=False)  # Restrição única adicionada aqui
    senha_hash = db.Column(db.String(255), nullable=False)
    permissao = db.Column(db.Integer, nullable=False)

class Filial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), unique=True, nullable=False)  # Restrição única adicionada aqui


class Centro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    filial_id = db.Column(db.Integer, db.ForeignKey('filial.id'))
    filial = db.relationship('Filial', backref=db.backref('centros', lazy=True))

class ResponsavelFilial(db.Model):
    responsavel_id = db.Column(db.Integer, db.ForeignKey('responsavel.id'), primary_key=True)
    filial_id = db.Column(db.Integer, db.ForeignKey('filial.id'), primary_key=True)
    responsavel = db.relationship('Responsavel', backref=db.backref('responsaveis_filial', lazy=True))
    filial = db.relationship('Filial', backref=db.backref('responsaveis_filial', lazy=True))

class NotaFiscal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chave_acesso = db.Column(db.String(255), nullable=False)
    cnpj = db.Column(db.String(14), nullable=False)
    nf = db.Column(db.String(255), nullable=False)
    codigo_cte = db.Column(db.String(255), nullable=False)
    volumes = db.Column(db.Integer, nullable=False)
    filial_id = db.Column(db.Integer, db.ForeignKey('filial.id'))
    filial = db.relationship('Filial', backref=db.backref('notas_fiscais', lazy=True))
    centro_id = db.Column(db.Integer, db.ForeignKey('centro.id'))
    centro = db.relationship('Centro', backref=db.backref('notas_fiscais', lazy=True))
    responsavel_id = db.Column(db.Integer, db.ForeignKey('responsavel.id'))
    responsavel = db.relationship('Responsavel', backref=db.backref('notas_fiscais', lazy=True))

class RegistroRecebimento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nota_fiscal_id = db.Column(db.Integer, db.ForeignKey('nota_fiscal.id'))
    nota_fiscal = db.relationship('NotaFiscal', backref=db.backref('registros_recebimento', lazy=True))
    data_recebimento = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(255), nullable=False)
    data_guarda = db.Column(db.Date, nullable=False)
    prioridade = db.Column(db.Integer, nullable=False)
