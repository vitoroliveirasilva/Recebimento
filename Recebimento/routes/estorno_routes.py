from flask import render_template, redirect, flash, session
from Recebimento import app, db
from Recebimento.models import NotaFiscal, RegistroRecebimento
from flask_login import login_required
from Recebimento.forms import EstornoForm
from Recebimento.utils import delete_session, get_responsavel_choices, register_estorno


@app.route("/estorno", methods=['GET', 'POST'])
@login_required
def estorno():
    form = EstornoForm()
    form.responsavel.choices = get_responsavel_choices(session.get('filial_id'))
    if form.validate_on_submit():
        try:
            register_estorno(form, session.get('chave_acesso'), db)
            flash('Recebimento registrado com sucesso!', 'success')
            delete_session()
            return redirect('/chave-acesso')
        except Exception as e:
            flash(f'Erro ao registrar o novo status: {str(e)}')
    elif form.errors:
        flash(form.errors, 'error')

    notas = NotaFiscal.query.all()
    registros = RegistroRecebimento.query.all()
    return render_template('/logic/mudar_status.html', form=form, notas=notas, registros=registros)
