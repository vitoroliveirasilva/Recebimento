from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, SubmitField, BooleanField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Optional, EqualTo
from Recebimento.utils import get_all_filiais


class EditarResponsavelForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=255)])
    ativo = BooleanField('Ativo', validators=[Optional()])
    usuario = StringField('Usuário', validators=[DataRequired(), Length(min=2, max=255)])
    alterar_senha = BooleanField('Alterar Senha', validators=[Optional()])
    nova_senha = PasswordField('Nova Senha', validators=[Optional(), Length(min=6)])
    confirm_nova_senha = PasswordField('Confirmar Nova Senha', validators=[Optional(), EqualTo('nova_senha')])
    permissao = BooleanField('Permissão', validators=[Optional()])
    filiais = SelectMultipleField('Filiais', coerce=int, choices=[], validators=[DataRequired()])
    submit = SubmitField('Atualizar')

class EditarFilialForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=255)])
    submit = SubmitField('Atualizar')

class EditarCentroForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=255)])
    filial = SelectField('Filial', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Atualizar')

    def __init__(self, *args, **kwargs):
        super(EditarCentroForm, self).__init__(*args, **kwargs)
        self.filial.choices = [(filial.id, filial.nome) for filial in get_all_filiais()]
