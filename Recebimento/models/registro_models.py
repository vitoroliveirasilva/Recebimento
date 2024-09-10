from Recebimento import db

class RegistroRecebimento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nota_fiscal_id = db.Column(db.Integer, db.ForeignKey('nota_fiscal.id'))
    data_recebimento = db.Column(db.DateTime)
    status = db.Column(db.String(255))
    data_guarda = db.Column(db.DateTime)
    prioridade = db.Column(db.Boolean, nullable=False)
    responsavel_id = db.Column(db.Integer, db.ForeignKey('responsavel.id'))
    data_atualizacao = db.Column(db.DateTime)

    nota_fiscal = db.relationship('NotaFiscal', backref=db.backref('registros', lazy=True))
    responsavel = db.relationship('Responsavel', backref=db.backref('registros', lazy=True))
