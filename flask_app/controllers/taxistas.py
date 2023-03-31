from flask import render_template, request, redirect, session, flash
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.taxista import Taxista
from flask_app.models.viaje import Ride
# from flask_app.models.viaje import Ride

bcrypt = Bcrypt(app)

@app.route('/login_taxistas')
def login_taxistas():
    return render_template("login_taxista.html")

@app.route('/register_taxistas')
def register_taxistas():
    return render_template("register_taxista.html")

@app.route('/register_taxista',methods=['POST'])
def register_taxista():
    is_valid = Taxista.validate_user(request.form)
    if not is_valid:
        return redirect("/login_register_taxistas")
    
    conductor = {
        "nombre": request.form["nombre"],
        "apellido": request.form["apellido"],
        "empresa": request.form["empresa"],
        "es_conductor": 1 if request.form.getlist('es_conductor') else 0,
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form["password"]),
    }

    id = Taxista.save(conductor)
    if not id:
        flash("Email ya existe.","register")
        return redirect('/login_register_taxistas')

    session['conductor_id'] = id
    return redirect('/viajes/disponibles')


@app.route("/login_taxista",methods=['POST'])
def login_taxista():
    data = {
        "email": request.form['email'],
        "empresa": request.form['empresa']
    }
    conductor = Taxista.get_by_email(data)
    empresa = Taxista.get_by_empresa(data)

    if not conductor:
        flash("Email, Empresa y/o Password Invalido","login")
        return render_template("/login_taxista.html")
    if not empresa:
        flash("Email, Empresa y/o Password Invalido","login")
        return render_template("/login_taxista.html")
    if not bcrypt.check_password_hash(conductor.password,request.form['password']):
        flash("Email, Empresa y/o Password Invalido","login")
        return render_template("/login_taxista.html")
    
    session['conductor_id'] = conductor.id
    return redirect('/viajes/disponibles')





@app.route('/logout')
def logout_taxista():
    session.clear()
    return redirect('/')