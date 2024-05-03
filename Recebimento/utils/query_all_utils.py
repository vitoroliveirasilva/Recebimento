from Recebimento.models import Responsavel, Filial, Centro, NotaFiscal, RegistroRecebimento


def get_all_users():
    responsaveis = Responsavel.query.all()
    return responsaveis

def get_all_filiais():
    filiais = Filial.query.all()
    return filiais

def get_all_centros():
    centros = Centro.query.all()
    return centros

def get_all_nfs():
    notas = NotaFiscal.query.all()
    return notas

def get_all_registros():
    registros = RegistroRecebimento.query.all()
    return registros
