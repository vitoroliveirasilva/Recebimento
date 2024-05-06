from flask import render_template, request
from Recebimento import app
from flask_login import login_required
from Recebimento.utils import get_all_users, get_all_filiais, get_all_centros, get_all_registros
from Recebimento.models import NotaFiscal, Filial


@app.route('/tabela-responsaveis')
@login_required
def table_responsaveis():
    return render_template('/tables/responsavel.html', responsaveis=get_all_users())

@app.route('/tabela-filiais')
@login_required
def table_filiais():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 2, type=int)
    filiais = Filial.query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('/tables/filial.html', filiais=filiais)

@app.route('/tabela-centros')
@login_required
def table_centros():
    return render_template('/tables/centro.html', centros=get_all_centros())

@app.route('/tabela-registros')
@login_required
def table_registros():
    return render_template('/tables/registros.html', registros=get_all_registros())

@app.route('/chave_acesso/<int:nota_fiscal_id>', methods=['GET', 'POST'])
@login_required
def viw_nf(nota_fiscal_id):
    notas_fiscais = [NotaFiscal.query.get_or_404(nota_fiscal_id)]
    return render_template('/partials/NotaFiscal.html', nfs=notas_fiscais)
