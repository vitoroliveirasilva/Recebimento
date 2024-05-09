from flask import render_template, redirect, flash
from Recebimento import app, db
from Recebimento.models import Centro, Filial
from flask_login import login_required
from Recebimento.forms import CadastroCentroForm, EditarCentroForm
from Recebimento.utils import get_filial_choices, centro_exists, register_new_centro, update_centro, delete_centro


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
                flash('Centro registrado com sucesso.')
            else:
                flash('Erro: Centro já existe. Por favor, escolha outro nome.')
        except Exception as e:
            flash(f'Erro ao registrar o centro: {str(e)}')

        return redirect('/cadastro/centros')

    return render_template('/register/centro.html', form=form)

@app.route('/editar_centro/<int:centro_id>', methods=['GET', 'POST'])
@login_required
def editar_centro(centro_id):
    centro = Centro.query.get_or_404(centro_id)
    form = EditarCentroForm(obj=centro)
    
    if form.validate_on_submit():
        data = form.data
        if not centro_exists(data['nome'], centro_id):
            update_centro(centro, data)
            flash('Centro atualizado com sucesso.')
            return redirect('/cadastro/centros')
        else:
            flash('Centro já existe. Por favor, escolha outro nome.', 'Erro')
            return redirect(f'/editar_centro/{centro_id}')

    filiais = Filial.query.all()
    return render_template('/edit/centro.html', form=form, centro=centro, filiais=filiais)

@app.route('/excluir_centro/<int:centro_id>', methods=['POST'])
@login_required
def excluir_centro(centro_id):
    centro = Centro.query.get_or_404(centro_id)
    if delete_centro(centro, db):
        flash('Centro excluído com sucesso.', 'Sucesso')
    else:
        flash('Erro ao excluir o centro.')
    return redirect('/tabela-centros')
