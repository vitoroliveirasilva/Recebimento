from flask import render_template, request
from Recebimento import app, db
from flask_login import login_required
from Recebimento.models import NotaFiscal, Filial, Centro, RegistroRecebimento, Responsavel
from sqlalchemy import desc, and_, func

@app.route('/tabela-responsaveis')
@login_required
def table_responsaveis():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    responsaveis = Responsavel.query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('/tables/responsavel.html', responsaveis=responsaveis)

@app.route('/tabela-filiais')
@login_required
def table_filiais():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    filiais = Filial.query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('/tables/filial.html', filiais=filiais)

@app.route('/tabela-centros')
@login_required
def table_centros():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    centros = Centro.query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('/tables/centro.html', centros=centros)

@app.route('/tabela-registros', methods=['POST'])
@login_required
def table_registros_id():
    nota_fiscal_id = request.form.get('nota_fiscal_id')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Consulta o registro específico para obter a chave de acesso
    registro = RegistroRecebimento.query.filter_by(nota_fiscal_id=nota_fiscal_id).first()
    chave_acesso = registro.nota_fiscal.chave_acesso if registro else None

    # Filtra e ordena os registros pelo ID da nota fiscal e pela data de atualização
    registros = RegistroRecebimento.query.filter_by(nota_fiscal_id=nota_fiscal_id).order_by(desc(RegistroRecebimento.data_atualizacao)).paginate(page=page, per_page=per_page, error_out=False)

    return render_template('/tables/registros_chave.html', registros=registros, nota_fiscal_id=nota_fiscal_id, chave_acesso=chave_acesso)

@app.route('/tabela-last-registros')
@login_required
def table_registros_last():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Subconsulta para encontrar o maior id para cada nota fiscal
    subquery = db.session.query(RegistroRecebimento.nota_fiscal_id, func.max(RegistroRecebimento.id).label('max_id')).group_by(RegistroRecebimento.nota_fiscal_id).subquery('t')

    # Junta a subconsulta de volta à tabela original para obter os registros correspondentes
    registros = db.session.query(RegistroRecebimento).join(subquery, and_(RegistroRecebimento.nota_fiscal_id == subquery.c.nota_fiscal_id, RegistroRecebimento.id == subquery.c.max_id)).paginate(page=page, per_page=per_page, error_out=False)

    return render_template('/tables/last_registros.html', registros=registros)

@app.route('/chave_acesso/<int:nota_fiscal_id>', methods=['GET', 'POST'])
@login_required
def viw_nf(nota_fiscal_id):
    notas_fiscais = [NotaFiscal.query.get_or_404(nota_fiscal_id)]
    return render_template('/partials/NotaFiscal.html', nfs=notas_fiscais)
