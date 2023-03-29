from flask import render_template, request, redirect, session, flash
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.taxista import Taxista
from flask_app.models.viaje import Ride
# from flask_app.models.viaje import Ride

bcrypt = Bcrypt(app)

@app.route('/login_register_taxistas')
def login_register_taxistas():
    return render_template("login_taxista.html")

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
    return render_template("dashboard_taxista.html")


@app.route("/login_taxistas",methods=['POST'])
def login_taxistas():
    data = {
        "email": request.form['email'],
        "empresa": request.form['empresa']
    }
    conductor = Taxista.get_by_email(data)
    print("---------------------------------------------------------------")
    print(conductor)
    empresa = Taxista.get_by_empresa(data)
    print(empresa)

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




# @app.route("/viajes/disponibles")
# def viajes_disponibles():
#     if "conductor_id" not in session:
#         return redirect("/")
#     rides = Ride.get_all_viajes()

#     # rides_without_driver = [r for r in rides if r.driver == None]
#     # rides_with_driver = [r for r in rides if r.driver != None]

#     rides_without_driver = []
#     rides_with_driver = []
#     for r in rides:
#         if(r.driver == None):
#             rides_without_driver.append(r)
#         else:
#             rides_with_driver.append(r)

#     # users = User.get_all()
#     return render_template("dashboard.html",rider=rider, rides_without_driver=rides_without_driver, rides_with_driver=rides_with_driver)



@app.route('/logout')
def logout_taxista():
    session.clear()
    return redirect('/')