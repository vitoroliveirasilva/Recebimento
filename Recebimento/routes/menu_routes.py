from flask import render_template, flash, session, request
from Recebimento import app
from flask_login import login_required, current_user
from Recebimento.utils import delete_session, get_filiais_responsavel_choices, handle_recebimento, handle_mudar_status, handle_estorno
from Recebimento.forms import ChaveAcessoForm

@app.route('/')
@login_required
def menu():
    return render_template('/partials/nav.html', current_user=current_user)

@app.route("/chave-acesso", methods=['GET', 'POST'])
@login_required
def cadastro_chaveacesso():
    delete_session()
    form = ChaveAcessoForm()
    filiais_por_responsavel = get_filiais_responsavel_choices(current_user.id)
    form.filial.choices = [(f.id, f.nome) for responsavel in filiais_por_responsavel.values() for f in responsavel]

    if form.validate_on_submit():
        session['filial_id'] = form.filial.data
        session['chave_acesso'] = form.chave_acesso.data
        action = request.form.get('action')

        if action == 'recebimento':            
            return handle_recebimento(form)
        elif action == 'mudar status':
            return handle_mudar_status(form)
        elif action == 'estorno':
            return handle_estorno(form)
        else:
            flash("Não foi possível encontrar a rota solicitada.", "Erro:")
    elif form.errors:
        flash(form.errors, "Erros:")

    return render_template('/partials/index.html', form=form, filiais_por_responsavel=filiais_por_responsavel)
