from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class CadastroUsuarioForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=255)])
    usuario = StringField('Usuário', validators=[DataRequired(), Length(min=2, max=255)])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirm_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha')])
    permissao = IntegerField('Permissão', validators=[DataRequired()])
    filiais = SelectMultipleField('Filiais', coerce=int)
    submit = SubmitField('Registrar')

class EditarResponsavelForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=255)])
    usuario = StringField('Usuário', validators=[DataRequired(), Length(min=2, max=255)])
    senha = PasswordField('Senha')
    confirm_senha = PasswordField('Confirmar Senha', validators=[EqualTo('senha')])
    permissao = IntegerField('Permissão', validators=[DataRequired()])
    filiais = SelectMultipleField('Filiais', coerce=int)
    alterar_senha = StringField('Alterar Senha')
    submit = SubmitField('Atualizar')

class CadastroFilialForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=255)])
    submit = SubmitField('Registrar')

class EditarFilialForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=255)])
    submit = SubmitField('Atualizar')

class CadastroCentroForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=255)])
    filial = SelectField('Filial', coerce=int)
    submit = SubmitField('Registrar')

class EditarCentroForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=255)])
    filial = SelectField('Filial', coerce=int)
    submit = SubmitField('Atualizar')
