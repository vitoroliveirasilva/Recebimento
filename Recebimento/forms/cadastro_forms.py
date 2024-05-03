from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, SubmitField, BooleanField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Optional, EqualTo


class CadastroResponsavelForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=255)])
    ativo = BooleanField('Ativo', validators=[Optional()])
    usuario = StringField('Usuário', validators=[DataRequired(), Length(min=2, max=255)])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirm_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha')])
    permissao = BooleanField('Permissão', validators=[Optional()])
    filiais = SelectMultipleField('Filiais', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Registrar')

class CadastroFilialForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=255)])
    submit = SubmitField('Registrar')

class CadastroCentroForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=255)])
    filial = SelectField('Filial', coerce=int, choices=[], validators=[DataRequired()])
    submit = SubmitField('Registrar')
