from .specific_utils import nota_fiscal_exists, get_last_status
from Recebimento.models import Responsavel
from flask import redirect, flash

def get_filiais_por_responsavel(user_id):
    return {Responsavel.query.get(user_id): [rf.filial for rf in Responsavel.query.get(user_id).responsaveis_filial]}

def handle_recebimento(form):
    last_status = get_last_status(form.chave_acesso.data)
    if not nota_fiscal_exists(form.chave_acesso.data) or (last_status and last_status.status=="Estornado"):
        return redirect('/cadastro/recebimento')
    else:
        flash("A chave de acesso já está cadastrada ou o último status não é 'Estornado'.", "warning")
        return redirect('/')

def handle_mudar_status(form):
    last_status = get_last_status(form.chave_acesso.data)
    if nota_fiscal_exists(form.chave_acesso.data) and (last_status and last_status.status!="Estornado"):
        return redirect('/mudar-status')
    else:
        flash("A chave de acesso não está cadastrada ou o último status é 'Estornado'.", "warning")
        return redirect('/')

def handle_estorno(form):
    last_status = get_last_status(form.chave_acesso.data)
    if nota_fiscal_exists(form.chave_acesso.data) and (last_status and last_status.status!="Estornado"):
        return redirect('/estorno')
    else:
        flash("A chave de acesso não está cadastrada ou o último status é 'Estornado'.", "warning")
        return redirect('/')
