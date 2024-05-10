from sqlalchemy.exc import SQLAlchemyError
from flask import flash

def record_exists(model, **kwargs):
    return model.query.filter_by(**kwargs).first() is not None

def delete_record(record, db):
    try:
        db.session.delete(record)
        db.session.commit()
        return True
    except SQLAlchemyError:
        db.session.rollback()
        return False

def extract_from_key(key, start, end):
    '''if len(key) != 44:
        flash("A chave de acesso deve ter 44 dígitos.", "Erro:")'''
    return key[start:end]

def commit_or_rollback(db):
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e
