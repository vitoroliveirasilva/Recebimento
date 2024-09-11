from flask import render_template, redirect, url_for, flash
from Recebimento import app, bcrypt, login_manager
from Recebimento.models import Responsavel
from flask_login import login_required, logout_user, login_user
from Recebimento.forms import LoginForm


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Responsavel.query.filter_by(usuario=form.username.data).first()
        if user:
            if user.ativo:
                if bcrypt.check_password_hash(user.senha_hash, form.password.data):
                    login_user(user)
                    return redirect('/')
                else:
                    flash('Senha incorreta.', 'danger')
            else:
                flash('Usuário inativo. Entre em contato com o administrador.', 'danger')
        else:
            flash('Usuário não encontrado.', 'danger')

    return render_template('/auth/login.html', form=form)

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

# Usuário não autenticado
@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))
