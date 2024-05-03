from flask import render_template, request, redirect, flash
from Recebimento import app, db, bcrypt
from Recebimento.models import Responsavel, Filial, ResponsavelFilial, Centro

def commit_or_rollback():
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

def user_exists(username):
    return Responsavel.query.filter_by(usuario=username).first() is not None

def filial_exists(nome):
    return Filial.query.filter_by(nome=nome).first() is not None

def cadastrar_responsavel(data):
    hashed_password = bcrypt.generate_password_hash(data['senha']).decode('utf-8')
    new_user = Responsavel(nome=data['nome'], usuario=data['usuario'], senha_hash=hashed_password, permissao=int(data['permissao']))
    db.session.add(new_user)
    return new_user

def cadastrar_filial(data):
    new_filial = Filial(nome=data['nome'])
    db.session.add(new_filial)
    return new_filial

@app.route('/')
def menu():
    return render_template('cadastro/IndexCadastro.html')

@app.route('/Cadastro/Usuario', methods=['GET', 'POST'])
def CadUser():
    if request.method == 'POST':
        try:
            data = request.form
            if user_exists(data['usuario']):
                flash('Erro: Usuário já existe. Por favor, escolha outro nome de usuário.')
            else:
                new_user = cadastrar_responsavel(data)
                for filial_id in request.form.getlist('filial'):
                    new_user_fil = ResponsavelFilial(responsavel=new_user, filial_id=int(filial_id))
                    db.session.add(new_user_fil)
                commit_or_rollback()
                flash('Usuário registrado com sucesso.')
        except Exception as e:
            flash(f'Erro ao registrar o usuário: {str(e)}')

        return redirect('/Cadastro/Usuario')

    responsaveis = Responsavel.query.all()
    filiaisdropdown = Filial.query.all()
    filiais_por_responsavel = {responsavel: [rf.filial for rf in responsavel.responsaveis_filial] for responsavel in responsaveis}
    return render_template('cadastro/CadastroUsuario.html', responsaveis_filiais=filiais_por_responsavel, filiaisdropdown=filiaisdropdown)

@app.route('/editar_responsavel/<int:responsavel_id>', methods=['GET', 'POST'])
def editar_responsavel(responsavel_id):
    responsavel = Responsavel.query.get_or_404(responsavel_id)
    if request.method == 'POST':
        try:
            data = request.form
            if user_exists(data['usuario']) and data['usuario'] != responsavel.usuario:
                flash('Erro: Usuário já existe. Por favor, escolha outro nome de usuário.')
                return redirect(f'/editar_responsavel/{responsavel_id}')

            responsavel.nome = data['nome']
            responsavel.usuario = data['usuario']
            responsavel.permissao = int(data['permissao'])

            if data.get('alterar_senha') == '1' and data.get('senha'):
                hashed_password = bcrypt.generate_password_hash(data['senha']).decode('utf-8')
                responsavel.senha_hash = hashed_password

            ResponsavelFilial.query.filter_by(responsavel_id=responsavel.id).delete()
            for filial_id in request.form.getlist('filial'):
                filial = Filial.query.get_or_404(int(filial_id))
                responsavel_filial = ResponsavelFilial(responsavel=responsavel, filial_id=filial.id)
                db.session.add(responsavel_filial)

            commit_or_rollback()
            flash('Responsável atualizado com sucesso.')
            return redirect('/Cadastro/Usuario')
        except Exception as e:
            flash(f'Erro ao atualizar o responsável: {str(e)}')

    filiais = Filial.query.all()
    filiais_selecionadas = [rf.filial_id for rf in responsavel.responsaveis_filial]
    return render_template('cadastro/EditarResponsavel.html', responsavel=responsavel, filiais=filiais, filiais_selecionadas=filiais_selecionadas)

@app.route('/excluir_responsavel/<int:responsavel_id>', methods=['POST'])
def excluir_responsavel(responsavel_id):
    try:
        responsavel = Responsavel.query.get_or_404(responsavel_id)
        # Exclua todas as instâncias de ResponsavelFilial associadas ao responsável
        ResponsavelFilial.query.filter_by(responsavel_id=responsavel_id).delete()
        # Agora você pode excluir o responsável com segurança
        db.session.delete(responsavel)
        commit_or_rollback()
        flash('Responsável excluído com sucesso!')
    except Exception as e:
        flash(f'Erro ao excluir o responsável: {str(e)}')
    return redirect('/Cadastro/Usuario')

@app.route('/Cadastro/Filial', methods=['GET', 'POST'])
def CadFilial():
    if request.method == 'POST':
        try:
            data = request.form
            if filial_exists(data['nome']):
                flash('Erro: Filial já existe. Por favor, escolha outro nome.')
            else:
                cadastrar_filial(data)
                commit_or_rollback()
                flash('Filial registrada com sucesso.')
        except Exception as e:
            flash(f'Erro ao registrar a filial: {str(e)}')

        return redirect('/Cadastro/Filial')

    filiais = Filial.query.all()
    return render_template('cadastro/CadastroFilial.html', filiais=filiais)

@app.route('/editar_filial/<int:filial_id>', methods=['GET', 'POST'])
def editar_filial(filial_id):
    filial = Filial.query.get_or_404(filial_id)
    if request.method == 'POST':
        try:
            data = request.form
            if filial_exists(data['nome']) and data['nome'] != filial.nome:
                flash('Erro: Filial já existe. Por favor, escolha outro nome.')
                return redirect(f'/editar_filial/{filial_id}')

            filial.nome = data['nome']
            commit_or_rollback()
            flash('Filial atualizada com sucesso.')
            return redirect('/Cadastro/Filial')
        except Exception as e:
            flash(f'Erro ao atualizar a filial: {str(e)}')

    return render_template('cadastro/EditarFilial.html', filial=filial)

@app.route('/excluir_filial/<int:filial_id>', methods=['POST'])
def excluir_filial(filial_id):
    try:
        filial = Filial.query.get_or_404(filial_id)
        ResponsavelFilial.query.filter_by(filial_id=filial_id).delete()
        db.session.delete(filial)
        commit_or_rollback()
        flash('Filial excluída com sucesso!')
    except Exception as e:
        flash(f'Erro ao excluir a filial: {str(e)}')
    return redirect('/Cadastro/Filial')

@app.route('/Cadastro/Centro', methods=['GET', 'POST'])
def CadCentro():
    if request.method == 'POST':
        try:
            data = request.form
            if Centro.query.filter_by(nome=data['nome']).first():
                flash('Erro: Centro já existe. Por favor, escolha outro nome.')
            else:
                new_centro = Centro(nome=data['nome'], filial_id=int(data['filial']))
                db.session.add(new_centro)
                db.session.commit()
                flash('Centro registrado com sucesso.')
        except Exception as e:
            flash(f'Erro ao registrar o centro: {str(e)}')

        return redirect('/Cadastro/Centro')
    
    centros = Centro.query.all()
    filiais = Filial.query.all()
    return render_template('cadastro/CadastroCentro.html', centros=centros, filiais=filiais)

@app.route('/editar_centro/<int:centro_id>', methods=['GET', 'POST'])
def editar_centro(centro_id):
    centro = Centro.query.get_or_404(centro_id)
    if request.method == 'POST':
        try:
            data = request.form
            centro_existente = Centro.query.filter(Centro.nome == data['nome'], Centro.id != centro_id).first()
            if centro_existente:
                flash('Erro: Centro já existe. Por favor, escolha outro nome.')
                return redirect(f'/editar_centro/{centro_id}')

            centro.nome = data['nome']
            centro.filial_id = int(data['filial'])
            db.session.commit()
            flash('Centro atualizado com sucesso.')
            return redirect('/Cadastro/Centro')
        except Exception as e:
            flash(f'Erro ao atualizar o centro: {str(e)}')

    filiais = Filial.query.all()
    return render_template('cadastro/EditarCentro.html', centro=centro, filiais=filiais)

@app.route('/excluir_centro/<int:centro_id>', methods=['POST'])
def excluir_centro(centro_id):
    try:
        centro = Centro.query.get_or_404(centro_id)
        db.session.delete(centro)
        db.session.commit()
        flash('Centro excluído com sucesso!')
    except Exception as e:
        flash(f'Erro ao excluir o centro: {str(e)}')
    return redirect('/Cadastro/Centro')
