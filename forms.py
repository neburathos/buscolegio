from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, DateTimeField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User

class RegistrationForm(FlaskForm):
    email = StringField('Email *', validators=[DataRequired(), Email()])
    username = StringField('Nombre *', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Contraseña *', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Contraseña *', validators=[DataRequired(), EqualTo('password')])
    image_file = FileField('Imagen De Perfil *', validators=[DataRequired(), FileAllowed(['jpg', 'png'])])
    role = SelectField(u'Soy:', choices=[('user', 'Padre / Madre'), ('inst', 'Institución')])
    submit = SubmitField('Registrar')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Esa cuenta de email ya ha sido utilizada, por favor seleccionar otra')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Ingresar')

class UpdateInstituteForm(FlaskForm):
    email = StringField('Email *', validators=[DataRequired(), Email()])
    name = StringField('Nombre Institución *', validators=[DataRequired(), Length(min=2, max=20)])
    cover_picture = FileField('Imagen De Portada', validators=[DataRequired(), FileAllowed(['jpg', 'png'])])
    url = StringField('Página Web')
    address = StringField('Dirección *', validators=[DataRequired()])
    phone =  IntegerField('Telefono')
    est = DateTimeField('Fundado', format='%m/%d/%y') # , validators=[DataRequired()]
    description = TextAreaField('Descripción')
    state = StringField('Departamento') 
    loc = StringField('Localidad') # , validators=[DataRequired()]
    teachers = IntegerField('Cantidad De Profesores')
    classrooms = IntegerField('Cantidad de Aulas')
    rel_conf = StringField('Confesión Religiosa')
    level = SelectField(u'Nivel', choices=[('Inicial', 'Inicial'), ('Primaria', 'Primaria',), ('Secundaria', 'Secundaria') ])
    enrollment = IntegerField('Matricula')
    fee = IntegerField('Cuota Mensual')
    submit = SubmitField('Actualizar')

class UpdateUserForm(FlaskForm):
    email = StringField('Email *', validators=[DataRequired(), Email()])
    username = StringField('Nombre Responsable *', validators=[DataRequired(), Length(min=2, max=20)])
    image_file = FileField('Imagend de Perfil')
    submit = SubmitField('Actualizar')

class SearchForm(FlaskForm):
    search = StringField('Buscar Institución')
    submit = SubmitField('Aceptar')