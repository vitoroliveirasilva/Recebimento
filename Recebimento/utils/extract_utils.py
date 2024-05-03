from .generic_utils import extract_from_key


def extrai_cnpj(chave_acesso):
    return extract_from_key(chave_acesso, 6, 20)

def extrai_nf(chave_acesso):
    return extract_from_key(chave_acesso, 25, 34)
