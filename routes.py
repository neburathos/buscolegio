import os
import secrets
from flask import render_template, url_for, flash, redirect, request, session
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateUserForm, UpdateInstituteForm, SearchForm
from flaskblog.models import Instituto, Extra, User
from flaskblog.tables import InstituteTable
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 2',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 2',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    }
]


@app.route("/home", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def home():
    form = SearchForm()
    institutos = []
    if form.validate_on_submit():
        institutos = Instituto.query.filter(Instituto.name.like('%{}%'.format(form.search.data))).all()
    picture = url_for('static', filename='profile_pics/')
    return render_template('home.html', picture=picture, form=form, institutos=institutos) # 

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        picture_file = save_picture(form.image_file.data)  
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, image_file=picture_file, role=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Usuario {form.username.data} creado! Ya puedes ingresar.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registro', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            session['user_id'] = user.id
            print(current_user.instituto)
            print(session['user_id'])
            next_page=(request.args.get('next'))
            flash('Has ingresado al sistema!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Incorrecto. Por favor, comprueba el usuario y la contraseña', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)
    return picture_fn

@app.route("/user", methods=['GET', 'POST'])
@login_required
def user():
    profile_pic = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('user.html', title='Usuario', profile_pic=profile_pic)

@app.route("/user/<int:user_id>/update", methods=['GET', 'POST'])
@login_required
def user_update(user_id):
    form = UpdateUserForm()

    if form.validate_on_submit():
        if form.image_file.data:
            picture_file = save_picture(form.image_file.data)
            current_user.image_file = picture_file
            flash('Linformación de usuario ha sido acutualizada con éxito')
            return redirect(url_for('user'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.image_file.data = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('user.html', title='Opciones de Usuario', form=form)

@app.route("/instituto/update", methods=['GET', 'POST'])
@login_required
def instituto_update():
    form = UpdateInstituteForm()

    if current_user.role != "inst":
        flash('Acceso denegado', 'danger')
        return redirect(url_for('{}'.format(current_user.role)))

    if form.validate_on_submit():
        picture_file = save_picture(form.cover_picture.data)
        instituto = Instituto.query.filter_by(responsable=current_user).first()
        instituto.name = form.name.data
        instituto.email = form.email.data
        instituto.url = form.url.data
        instituto.address = form.address.data
        instituto.phone = form.phone.data
        instituto.est = form.est.data
        instituto.description = form.description.data
        instituto.state = form.state.data
        instituto.loc = form.loc.data
        instituto.teachers = form.teachers.data
        instituto.classrooms = form.classrooms.data
        instituto.rel_conf = form.rel_conf.data
        instituto.level = form.level.data
        instituto.enrollment = form.enrollment.data
        instituto.fee = form.fee.data
        responsable = current_user
        cover_picture = picture_file
        db.session.commit()
        flash('Instituto actualizado con exito', 'success')
        return redirect(url_for('instituto_update'))
    elif request.method == 'GET':
        instituto = Instituto.query.filter_by(responsable=current_user).first() # instituto/actualizar
        form.name.data = instituto.name
        form.email.data = instituto.email
        form.cover_picture.data = url_for('static', filename='profile_pics/' + instituto.cover_picture)
        form.url.data = instituto.url
        form.address.data = instituto.address
        form.phone.data = instituto.phone
        form.est.data = instituto.est
        form.description.data = instituto.description
        form.state.data = instituto.state
        form.loc.data = instituto.loc
        form.teachers.data = instituto.teachers
        form.classrooms.data = instituto.classrooms
        form.rel_conf.data = instituto.rel_conf
        form.level.data = instituto.level
        form.enrollment.data = instituto.enrollment
        form.fee.data = instituto.fee
    return render_template('instituto.html', title='Datos del Instituto', form=form)

@app.route("/instituto/create", methods=['GET', 'POST'])
@login_required
def instituto_create():
    form = UpdateInstituteForm()

    if current_user.role != "inst":
        flash('Acceso denegado', 'danger')
        return redirect(url_for('{}'.format(current_user.role)))

    if form.validate_on_submit():
        picture_file = save_picture(form.cover_picture.data)
        instituto = Instituto( name=form.name.data, email=form.email.data, url=form.url.data, address=form.address.data, phone=form.phone.data, est=form.est.data, description=form.description.data, state=form.state.data, loc=form.loc.data, teachers=form.teachers.data, classrooms=form.classrooms.data, rel_conf=form.rel_conf.data, level=form.level.data, enrollment=form.enrollment.data, fee=form.fee.data, responsable=current_user, cover_picture=picture_file )
        db.session.add(instituto)
        db.session.commit()
        flash('Instituto {} creado con exito'.format(instituto.name), 'success')
        return redirect(url_for('instituto_create'))
    return render_template('instituto.html', title='Datos del Instituto', form=form)

@app.route("/instituto/details/<int:instituto_id>")
@login_required
def details(instituto_id):
    instituto = Instituto.query.get_or_404(instituto_id)
    return render_template('details.html', title=instituto.name, instituto=instituto)

