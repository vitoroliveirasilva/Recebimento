from flask import render_template, redirect, flash, session
from Recebimento import app, db
from flask_login import login_required
from Recebimento.forms import RecebimentoForm
from Recebimento.utils import delete_session, get_responsavel_choices, get_centro_choices, nota_fiscal_exists, get_nota_fiscal_data, register_new_nota_fiscal, register_new_recebimento, get_recebimento_data, extrai_nf


@app.route("/cadastro/recebimento", methods=['GET', 'POST'])
@login_required
def cadastro_recebimento():
    form = RecebimentoForm()
    filial_id = session.get('filial_id')
    chave_acesso = session.get('chave_acesso')
    form.responsavel.choices = get_responsavel_choices(filial_id)
    form.centro.choices = get_centro_choices(filial_id)

    if form.validate_on_submit():
        try:
            if not nota_fiscal_exists(chave_acesso):
                nova_nf = register_new_nota_fiscal(get_nota_fiscal_data(form, chave_acesso, session), db)
                register_new_recebimento(get_recebimento_data(form, nova_nf.id), db)
                flash('Recebimento registrado com sucesso!', 'success')
                delete_session()
                return redirect('/')
            else:
                flash("Esta chave de acesso já está cadastrada.", 'danger')
                return redirect('/')
        except ValueError as e:
            flash(str(e), 'danger')
    elif form.errors:
        for campo, erros in form.errors.items():
            for erro in erros:
                flash(f'{campo.upper()}: {erro}', 'warning')

    return render_template('/logic/recebimento.html', form=form, nf=extrai_nf(chave_acesso))
