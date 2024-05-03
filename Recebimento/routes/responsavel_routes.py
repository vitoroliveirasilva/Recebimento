from flask import render_template, redirect, flash
from Recebimento import app, db
from Recebimento.models import Responsavel, ResponsavelFilial
from flask_login import login_required
from Recebimento.forms import CadastroResponsavelForm, EditarResponsavelForm
from Recebimento.utils import user_exists, register_new_responsavel, commit_or_rollback, update_responsavel, delete_responsavel, get_filial_choices


@app.route('/cadastro/responsavel', methods=['GET', 'POST'])
@login_required
def register_responsavel():
    form = CadastroResponsavelForm()
    form.filiais.choices = [(filial.id, filial.nome) for filial in get_filial_choices()]
    if form.validate_on_submit():
        print("Formulário submetido")
        try:
            if not user_exists(form.nome.data):
                responsavel = register_new_responsavel(form.data, db)
                for filial_id in form.filiais.data:
                    responsavel_filial = ResponsavelFilial(responsavel_id=responsavel.id, filial_id=int(filial_id))
                    db.session.add(responsavel_filial)
                commit_or_rollback(db)
                flash('Responsável registrado com sucesso.')
            else:
                flash('Erro: Responsável já existe. Por favor, escolha outro nome.')
        except Exception as e:
            flash(f'Erro ao registrar o responsável: {str(e)}')

        return redirect('/cadastro/responsavel')
    else:
        print(form.errors)
    
    return render_template('/register/responsavel.html', form=form)

@app.route('/editar_responsavel/<int:responsavel_id>', methods=['GET', 'POST'])
@login_required
def editar_responsavel(responsavel_id):
    responsavel = Responsavel.query.get_or_404(responsavel_id)
    form = EditarResponsavelForm(obj=responsavel)
    
    if form.validate_on_submit():
        update_responsavel(responsavel, form)
        commit_or_rollback()
        flash('O responsável foi atualizado com sucesso!', 'success')
        return redirect("/cadastro/responsaveis")

    return render_template('/edit/responsavel.html', form=form, responsavel=responsavel)

@app.route('/excluir_responsavel/<int:responsavel_id>', methods=['POST'])
@login_required
def excluir_responsavel(responsavel_id):
    responsavel = Responsavel.query.get_or_404(responsavel_id)
    if delete_responsavel(responsavel, responsavel_id, db):
        flash('Responsável excluído com sucesso.', 'success')
    else:
        flash('Erro ao excluir o responsável.', 'Erro')
    return redirect('/registros')
