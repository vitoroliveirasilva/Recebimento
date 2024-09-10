from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length, Optional, NumberRange, Regexp
from Recebimento.utils import STATUS_CHOICES


class ChaveAcessoForm(FlaskForm):
    chave_acesso = StringField('chave_acesso', validators=[DataRequired(), Length(min=40, max=46), Regexp('^\d{40,46}$', message="A chave de acesso deve ser composta apenas por números")])
    filial = SelectField('filial', coerce=int, choices=[], validators=[DataRequired()])

class RecebimentoForm(FlaskForm):
    codigo_cte = StringField('Código CTE', validators=[Optional(), Length(min=1, max=100)])
    volumes = IntegerField('Volumes', validators=[DataRequired(), NumberRange(min=1, max=1000)])
    responsavel = SelectField('Responsável', coerce=int, choices=[], validators=[DataRequired()])
    centro = SelectField('Centro', coerce=int, choices=[], validators=[DataRequired()])
    prioridade = BooleanField('Prioridade', validators=[Optional()])
    avarias = BooleanField('Avarias', validators=[Optional()])
    recusa = BooleanField('Recusa', validators=[Optional()])
    submit = SubmitField('Registrar')

class MudarStatusForm(FlaskForm):
    responsavel = SelectField('responsavel', coerce=int, choices=[], validators=[DataRequired()])
    status = SelectField('status', choices=STATUS_CHOICES, validators=[DataRequired()])
    submit = SubmitField('Registrar')

class EstornoForm(FlaskForm):
    responsavel = SelectField('responsavel', coerce=int, choices=[], validators=[DataRequired()])
    submit = SubmitField('Registrar')