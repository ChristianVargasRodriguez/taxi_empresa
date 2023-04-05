from flask import render_template, request, redirect, session, flash
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.usuario import User

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register_usuarios')
def register_usuarios():
    return render_template("register_usuario.html")

@app.route('/register_usuario',methods=['POST'])
def register():
    is_valid = User.validate_user(request.form)
    if not is_valid:
        return redirect("/register_usuarios")
    
    new_user = {
        "nombre": request.form["nombre"],
        "apellido": request.form["apellido"],
        "empresa": request.form["empresa"],
        "cargo": request.form["cargo"],
        "telefono": request.form["telefono"],
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form["password"]),
    }

    id = User.save(new_user)
    if not id:
        flash("Email ya existe.","register")
        return redirect('/register_usuarios')
    
    session['usuario_id'] = id
    return redirect('/pedir_viaje')

@app.route('/login_usuarios')
def login_usuarios():
    return render_template("login_usuario.html")


@app.route("/login_usuario",methods=['POST'])
def login_usuario():    
    data = {
        "email": request.form['email'],
        "empresa": request.form['empresa']
    }
    usuario = User.get_by_email(data)
    empresa = User.get_by_empresa(data)


    if not usuario:
        flash("Email, Empresa y/o Password Invalido","login")
        return redirect("/login_usuarios")
    if not empresa:
        flash("Email, Empresa y/o Password Invalido","login")
        return redirect("/login_usuarios")
    if not bcrypt.check_password_hash(usuario.password,request.form['password']):
        flash("Email, Empresa y/o Password Invalido","login")
        return redirect("/login_usuarios")
    
    session['usuario_id'] = usuario.id
    session['cargo'] = usuario.cargo
    return redirect('/pedir_viaje')


@app.route('/pedir_viaje')
def pedir_viaje():
    if 'usuario_id' not in session:
        return redirect('/login_usuarios')
    data = {"id": session["usuario_id"]}
    usuario = User.get_one_usuario(data)
    return render_template("pedir_viaje.html", usuario=usuario)



@app.route('/logout', methods = ['POST'])
def logout():
    session.clear()
    return redirect('/')