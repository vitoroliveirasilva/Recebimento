from flask import render_template, redirect, flash
from Recebimento import app, db
from Recebimento.models import Filial
from flask_login import login_required
from Recebimento.forms import CadastroFilialForm, EditarFilialForm
from Recebimento.utils import filial_exists, register_new_filial, update_filial, delete_filial


@app.route('/cadastro/filiais', methods=['GET', 'POST'])
@login_required
def register_filial():
    form = CadastroFilialForm()
    
    if form.validate_on_submit():
        try:
            data = form.data
            if not filial_exists(data['nome']):
                register_new_filial(data)
                flash('Filial registrada com sucesso.', 'success')
                return redirect('/tabela-filiais')
            else:
                flash('Filial já existe. Por favor, escolha outro nome.', 'warning')
        except Exception as e:
            flash(f'Erro ao registrar a filial: {str(e)}', 'danger')

    return render_template('/register/filial.html', form=form)

@app.route('/editar_filial/<int:filial_id>', methods=['GET', 'POST'])
@login_required
def editar_filial(filial_id):
    filial = Filial.query.get_or_404(filial_id)
    form = EditarFilialForm(obj=filial)
    
    if form.validate_on_submit():
        data = form.data
        try:
            if not filial_exists(data['nome']):
                update_filial(filial, data, db)
                flash('Filial atualizada com sucesso.', 'success')
                return redirect('/tabela-filiais')
            else:
                flash('Filial já existe. Por favor, escolha outro nome.', 'warning')
        except Exception as e:
            flash(f'Ocorreu um erro ao atualizar a filial: {str(e)}', 'danger')

    return render_template('/edit/filial.html', form=form, filial=filial)

@app.route('/excluir_filial/<int:filial_id>', methods=['POST'])
@login_required
def excluir_filial(filial_id):
    filial = Filial.query.get_or_404(filial_id)
    if delete_filial(filial, filial_id, db):
        flash('Filial excluída com sucesso.', 'success')
    else:
        flash('Não foi possível excluir a filial.', 'danger')
    return redirect('/tabela-filiais')
