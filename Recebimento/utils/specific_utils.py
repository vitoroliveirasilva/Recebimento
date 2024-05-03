from Recebimento.models import Responsavel, Filial, Centro, NotaFiscal, RegistroRecebimento
from .generic_utils import record_exists


def user_exists(username):
    return record_exists(Responsavel, usuario=username)

def filial_exists(nome):
    return record_exists(Filial, nome=nome)

def centro_exists(nome):
    return record_exists(Centro, nome=nome)

def nota_fiscal_exists(chave_acesso):
    return record_exists(NotaFiscal, chave_acesso=chave_acesso)

def get_last_status(chave_acesso):
    last_record = RegistroRecebimento.query.join(NotaFiscal).filter(NotaFiscal.chave_acesso == chave_acesso).order_by(RegistroRecebimento.id.desc()).first()
    return last_record
