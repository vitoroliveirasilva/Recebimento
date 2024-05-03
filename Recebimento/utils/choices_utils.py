from Recebimento.models import Responsavel, Filial, Centro, ResponsavelFilial

def get_responsavel_choices(filial_id):
    responsaveis = Responsavel.query.join(ResponsavelFilial).filter(ResponsavelFilial.filial_id == filial_id).all()
    return [(r.id, r.nome) for r in responsaveis]

def get_centro_choices(filial_id):
    centros = Centro.query.filter_by(filial_id=filial_id).all()
    return [(c.id, c.nome) for c in centros]

def get_filial_choices():
    filiais = Filial.query.all()
    return filiais

def get_filiais_responsavel_choices(user_id):
    responsavel = Responsavel.query.get(user_id)
    return {responsavel: [rf.filial for rf in responsavel.responsaveis_filial]}

def get_filiais_do_responsavel(user_id):
    responsavel_filiais = ResponsavelFilial.query.filter_by(responsavel_id=user_id).all()
    filiais_ids = [rf.filial_id for rf in responsavel_filiais]
    return filiais_ids
