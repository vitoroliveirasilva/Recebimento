from Recebimento.models import Responsavel, Filial, Centro, NotaFiscal, RegistroRecebimento, ResponsavelFilial
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from Recebimento import bcrypt, db
from flask import request, flash, redirect, url_for
from .specific_utils import get_last_status

def register_new_responsavel(data, db):
    hashed_password = bcrypt.generate_password_hash(data['senha']).decode('utf-8')
    new_user = Responsavel(
        ativo=int(data['ativo']),
        nome=data['nome'],
        usuario=data['usuario'],
        senha_hash=hashed_password,
        permissao=int(data['permissao'])
    )
    db.session.add(new_user)
    db.session.commit()
    return new_user

def register_new_filial(data):
    new_filial = Filial(nome=data['nome'])
    db.session.add(new_filial)
    db.session.commit()
    return new_filial

def register_new_centro(data):
    new_centro = Centro(nome=data['nome'], filial_id=int(data['filial']))
    db.session.add(new_centro)
    db.session.commit()
    return new_centro

def register_new_responsavelfilial(responsavel, filiais, db):
    for filial_id in filiais:
        responsavel_filial = ResponsavelFilial(responsavel_id=responsavel.id, filial_id=filial_id)
        db.session.add(responsavel_filial)
    commit_or_rollback(db)

def register_new_nota_fiscal(data, db):
    nova_nf = NotaFiscal(
        chave_acesso=data['chave_acesso'],
        cnpj=data['cnpj'],
        nf=data['nf'],
        codigo_cte=data['codigo_cte'],
        volumes=data['volumes'],
        filial_id=data['filial_id'],
        centro_id=data['centro_id']
    )
    db.session.add(nova_nf)
    commit_or_rollback(db)
    return nova_nf

def register_new_recebimento(data, db):
    new_receipt = RegistroRecebimento(
        nota_fiscal_id=data['nota_fiscal_id'],
        data_recebimento=datetime.now(),
        status=data['status'],
        prioridade=data['prioridade'],
        responsavel_id=data['responsavel_id'],
        data_atualizacao=datetime.now()
    )
    db.session.add(new_receipt)
    commit_or_rollback(db)
    return new_receipt

def register_new_status(form, chave_acesso, db):
    last_record = get_last_status(chave_acesso)
    if last_record is None:
        flash('Não foi encontrado nenhum registro anterior com a chave de acesso fornecida.', 'error')
        return redirect(url_for('registros'))
    else:
        data = {
            'nota_fiscal_id': last_record.nota_fiscal_id,
            'data_recebimento': last_record.data_recebimento,
            'status': request.form.get('status'),
            'prioridade': last_record.prioridade,
            'responsavel_id': form.responsavel.data,
        }

        if data['status']=="NF finalizada":
            data_guarda = datetime.now()
        else:
            data_guarda = None

        new_receipt = RegistroRecebimento(
            nota_fiscal_id=data['nota_fiscal_id'],
            data_recebimento=data['data_recebimento'],
            status=data['status'],
            data_guarda=data_guarda,
            prioridade=data['prioridade'],
            responsavel_id=data['responsavel_id'],
            data_atualizacao=datetime.now()
        )
        db.session.add(new_receipt)
        commit_or_rollback(db)
        return new_receipt

def register_estorno(form, chave_acesso, db):
    last_record = get_last_status(chave_acesso)
    if last_record is None:
        flash('Não foi encontrado nenhum registro anterior com a chave de acesso fornecida.', 'error')
        return redirect(url_for('registros'))
    else:
        data = {
            'nota_fiscal_id': last_record.nota_fiscal_id,
            'data_recebimento': last_record.data_recebimento,
            'status': 'Estornado',
            'data_guarda': last_record.data_guarda,
            'prioridade': last_record.prioridade,
            'responsavel_id': form.responsavel.data,
        }

        new_receipt = RegistroRecebimento(
            nota_fiscal_id=data['nota_fiscal_id'],
            data_recebimento=data['data_recebimento'],
            status=data['status'],
            data_guarda=data['data_guarda'],
            prioridade=data['prioridade'],
            responsavel_id=data['responsavel_id'],
            data_atualizacao=datetime.now()
        )
        db.session.add(new_receipt)
        commit_or_rollback(db)
        return new_receipt

def update_responsavelfilial(responsavel, filiais_selecionadas, db):
    ResponsavelFilial.query.filter_by(responsavel_id=responsavel.id).delete()
    for filial_id in filiais_selecionadas:
        responsavel_filial = ResponsavelFilial(responsavel_id=responsavel.id, filial_id=filial_id)
        db.session.add(responsavel_filial)
    commit_or_rollback(db)

def update_centro(centro, data, db):
    centro.nome = data['nome']
    centro.filial_id = int(data['filial'])
    db.session.commit()

def update_filial(filial, data, db):
    filial.nome = data['nome']
    db.session.commit()

def update_responsavel(responsavel, form, db):
    responsavel.nome = form.nome.data
    responsavel.ativo = form.ativo.data
    responsavel.usuario = form.usuario.data
    if form.alterar_senha.data:
        responsavel.senha_hash = bcrypt.generate_password_hash(form.nova_senha.data).decode('utf-8')
    responsavel.permissao = form.permissao.data
    db.session.commit()

def commit_or_rollback(db):
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e
