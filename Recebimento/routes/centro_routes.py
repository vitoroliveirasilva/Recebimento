from flask import render_template, redirect, flash
from Recebimento import app, db
from Recebimento.models import Centro, Filial
from flask_login import login_required
from Recebimento.forms import CadastroCentroForm, EditarCentroForm
from Recebimento.utils import get_filial_choices, centro_exists, register_new_centro, update_centro, delete_centro, get_all_filiais


@app.route('/cadastro/centros', methods=['GET', 'POST'])
@login_required
def register_centro():
    form = CadastroCentroForm()
    form.filial.choices = [(filial.id, filial.nome) for filial in get_filial_choices()]
    
    if form.validate_on_submit():
        try:
            data = form.data
            if not centro_exists(data['nome']):
                register_new_centro(data)
                flash('Centro registrado com sucesso.', 'success')
                return redirect('/tabela-centros')
            else:
                flash('Centro já existe. Por favor, escolha outro nome.', 'warning')
        except Exception as e:
            flash(f'Erro ao registrar o centro: {str(e)}', 'danger')

    return render_template('/register/centro.html', form=form)

@app.route('/editar_centro/<int:centro_id>', methods=['GET', 'POST'])
@login_required
def editar_centro(centro_id):
    centro = Centro.query.get_or_404(centro_id)
    form = EditarCentroForm(obj=centro)
    
    if form.validate_on_submit():
        data = form.data
        try:
            if not centro_exists(data['nome']):
                update_centro(centro, data, db)
                flash('Centro atualizado com sucesso.', 'success')
                return redirect('/tabela-centros')
            else:
                flash('Centro já existe. Por favor, escolha outro nome.', 'warning')
        except Exception as e:
            flash(f'Ocorreu um erro ao atualizar o centro: {str(e)}', 'danger')
    
    return render_template('/edit/centro.html', form=form, centro=centro)

@app.route('/excluir_centro/<int:centro_id>', methods=['POST'])
@login_required
def excluir_centro(centro_id):
    centro = Centro.query.get_or_404(centro_id)
    if delete_centro(centro, db):
        flash('Centro excluído com sucesso.', 'success')
    else:
        flash('Erro ao excluir o centro.', 'danger')
    return redirect('/tabela-centros')
