from flask import render_template, redirect, flash
from Recebimento import app, db, bcrypt
from flask_login import login_required, current_user
from Recebimento.forms import AlteracaoSenhaForm


@app.route('/alteracao_senha', methods=['GET', 'POST'])
@login_required
def alteracao_senha():
    form = AlteracaoSenhaForm()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.senha_hash, form.senha_atual.data):
            current_user.senha_hash = bcrypt.generate_password_hash(form.nova_senha.data).decode('utf-8')
            db.session.commit()
            flash('Senha alterada com sucesso!', 'success')
            return redirect('/')
        else:
            flash('Senha atual incorreta.', 'error')
    return render_template('edit/senha.html', form=form)
