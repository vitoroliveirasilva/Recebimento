from flask import render_template, redirect, flash
from Recebimento import app, db
from Recebimento.models import Responsavel, ResponsavelFilial, Filial
from flask_login import login_required
from Recebimento.forms import CadastroResponsavelForm, EditarResponsavelForm
from Recebimento.utils import user_exists, register_new_responsavel, commit_or_rollback, update_responsavel, delete_responsavel, get_filial_choices


@app.route('/cadastro/responsavel', methods=['GET', 'POST'])
@login_required
def register_responsavel():
    form = CadastroResponsavelForm()
    form.filiais.choices = [(filial.id, filial.nome) for filial in get_filial_choices()]
    
    if form.validate_on_submit():
        try:
            if not user_exists(form.nome.data):
                responsavel = register_new_responsavel(form.data, db)
                for filial_id in form.filiais.data:
                    responsavel_filial = ResponsavelFilial(responsavel_id=responsavel.id, filial_id=int(filial_id))
                    db.session.add(responsavel_filial)
                commit_or_rollback(db)
                flash('Responsável registrado com sucesso.', 'success')
                return redirect('/tabela-responsaveis')
            else:
                flash('Responsável já existe. Por favor, escolha outro nome.', 'warning')
        except Exception as e:
            flash(f'Erro ao registrar o responsável: {str(e)}', 'danger')
    
    return render_template('/register/responsavel.html', form=form)

@app.route('/editar_responsavel/<int:responsavel_id>', methods=['GET', 'POST'])
@login_required
def editar_responsavel(responsavel_id):
    responsavel = Responsavel.query.get_or_404(responsavel_id)
    form = EditarResponsavelForm(obj=responsavel)

    try:
        filiais = [(filial.id, filial.nome) for filial in Filial.query.all()]
        filiais_associadas = [rf.filial_id for rf in responsavel.responsaveis_filial]
        form.filiais.choices = filiais
    except Exception as e:
        flash(f'Ocorreu um erro ao buscar as filiais: {str(e)}', 'danger')
        return redirect('/tabela-responsaveis')
    
    if form.validate_on_submit():
        data = form.data
        try:
            # Verifica se o nome de usuário foi alterado
            if responsavel.usuario != data['usuario']:
                # Verifica se o novo nome de usuário já existe
                if user_exists(data['usuario']):
                    flash('Erro: Usuário já existe. Por favor, escolha outro nome.', 'warning')
                    return redirect(f'/editar_responsavel/{responsavel_id}')
                else:
                    update_responsavel(responsavel, form, db)
                    flash('O responsável foi atualizado com sucesso!', 'success')
                    return redirect('/tabela-responsaveis')
            else:
                update_responsavel(responsavel, form, db)
                flash('O responsável foi atualizado com sucesso!', 'success')
                return redirect('/tabela-responsaveis')        
        except Exception as e:
            flash(f'Ocorreu um erro ao atualizar o responsável: {str(e)}', 'danger')

    return render_template('/edit/responsavel.html', form=form, responsavel=responsavel, filiais=filiais, filiais_associadas=filiais_associadas)

@app.route('/excluir_responsavel/<int:responsavel_id>', methods=['POST'])
@login_required
def excluir_responsavel(responsavel_id):
    responsavel = Responsavel.query.get_or_404(responsavel_id)
    if delete_responsavel(responsavel, responsavel_id, db):
        flash('Responsável excluído com sucesso.', 'success')
    else:
        flash('Erro ao excluir o responsável.', 'Erro')
    return redirect('/tabela-responsaveis')
