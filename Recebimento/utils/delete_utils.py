from Recebimento.models import ResponsavelFilial
from flask import session
from .generic_utils import delete_record


def delete_centro(centro, db):
    return delete_record(centro, db)

def delete_filial(filial, filial_id, db):
    ResponsavelFilial.query.filter_by(filial_id=filial_id).delete()
    return delete_record(filial, db)

def delete_nota(nota, db):
    return delete_record(nota, db)

def delete_registro(registro, db):
    return delete_record(registro, db)

def delete_responsavel(responsavel, responsavel_id, db):
    ResponsavelFilial.query.filter_by(responsavel_id=responsavel_id).delete()
    return delete_record(responsavel, db)

def delete_session():
    session.pop('filial_id', None)
    session.pop('chave_acesso', None)
