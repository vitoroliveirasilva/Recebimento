from .extract_utils import extrai_cnpj, extrai_nf


def get_nota_fiscal_data(form, chave_acesso, session):
    return {
        'chave_acesso': chave_acesso,
        'cnpj': extrai_cnpj(chave_acesso),
        'nf': extrai_nf(chave_acesso),
        'codigo_cte': form.codigo_cte.data,
        'volumes': form.volumes.data,
        'filial_id': session['filial_id'],
        'centro_id': form.centro.data
    }

def define_status(form):
    status = "Aguardando Conferência"
    if form.recusa.data and form.avarias.data:
        status = "Recusado por avaria"
    elif form.recusa.data:
        status = "Recusa"
    return status

def get_recebimento_data(form, nota_fiscal_id):
    return {
        'nota_fiscal_id': nota_fiscal_id,
        'status': define_status(form),
        'prioridade': form.prioridade.data,
        'responsavel_id': form.responsavel.data
    }
