from .specific_utils import nota_fiscal_exists, get_last_status
from Recebimento.models import Responsavel
from flask import redirect, flash

def get_filiais_por_responsavel(user_id):
    return {Responsavel.query.get(user_id): [rf.filial for rf in Responsavel.query.get(user_id).responsaveis_filial]}

def handle_recebimento(form):
    if not nota_fiscal_exists(form.chave_acesso.data) or get_last_status(form.chave_acesso.data)=="Estornado":
        return redirect('/cadastro/recebimento')
    else:
        flash("A chave de acesso já está cadastrada.", "Erro:")
        return redirect('/chave-acesso')

def handle_mudar_status(form):
    if nota_fiscal_exists(form.chave_acesso.data):
        return redirect('/mudar-status')
    else:
        flash("A chave de acesso não está cadastrada.", "Erro:")
        return redirect('/chave-acesso')

def handle_estorno(form):
    if nota_fiscal_exists(form.chave_acesso.data) and not get_last_status(form.chave_acesso.data)=="Estornado":
        return redirect('/estorno')
    else:
        flash("A chave de acesso não está cadastrada.", "Erro:")
        return redirect('/chave-acesso')
