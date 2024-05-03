from flask_login import UserMixin
from Recebimento import db, bcrypt

class Responsavel(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    ativo = db.Column(db.Boolean, nullable=False, default=False)
    nome = db.Column(db.String(255), nullable=False)
    usuario = db.Column(db.String(255), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    permissao = db.Column(db.Boolean, nullable=False)
    responsaveis_filial = db.relationship('ResponsavelFilial', backref='responsavel')

    @classmethod
    def check_user_existence(cls, username):
        return cls.query.filter_by(usuario=username).first() is not None

    @classmethod
    def register_responsavel(cls, data):
        ativo = True if data['ativo'] == '1' else False
        hashed_password = bcrypt.generate_password_hash(data['senha']).decode('utf-8')
        new_user = cls(ativo=ativo, nome=data['nome'], usuario=data['usuario'], senha_hash=hashed_password, permissao=int(data['permissao']))
        db.session.add(new_user)
        return new_user