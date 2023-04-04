from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.taxista import Taxista
from flask_app.models.usuario import User
from flask_app.models.viaje import Ride



@app.route("/viajes/solicitud", methods=["GET", "POST"])
def solicitud_viaje():
    if "usuario_id" not in session:
        return redirect("/")
    
    data = {"id": session["usuario_id"]}
    usuario = User.get_one_usuario(data)

    # POST REQUEST
    if request.method == "POST":
        is_valid = Ride.validate_ride(request.form, "new")
        if not is_valid:
            return redirect("/viajes/solicitud")
        viaje_id = Ride.save(request.form)
        return redirect(f"/viaje/en_curso/{viaje_id}/") 
    return render_template("pedir_viaje.html", usuario=usuario)


@app.route("/viajes/<int:viaje_id>/add_driver/<int:conductor_id>")
def add_driver(viaje_id, conductor_id):
    data_2 = {"id": viaje_id, "conductor_id": conductor_id}
    data = {"id": viaje_id}
    conductor = Ride.add_driver(data_2)
    viaje = Ride.get_one_with_users(data)
    return render_template("viaje_en_curso.html", viaje=viaje, conductor=conductor)


@app.route("/viaje/en_curso/<int:viaje_id>/")
def details_ride(viaje_id):
    data = {"id": viaje_id}
    viaje_actual = Ride.get_one_with_users(data)
    return render_template("viaje_en_curso.html", viaje=viaje_actual) 


@app.route('/viajes/<int:viaje_id>/editar', methods=['GET','POST'])
def editar_viaje(viaje_id):
    # POST REQUEST 
    if request.method == 'POST':
        if not Ride.validate_ride(request.form, "edit"):
            return redirect(f"/viajes/{viaje_id}/editar")
        Ride.editar_viaje(request.form)
        return redirect(f"/viaje/en_curso/{viaje_id}/")
    
    # GET REQUEST
    if 'usuario_id' not in session:
        return redirect('/')
    data = {
        'id': viaje_id
    }
    viaje = Ride.get_one_with_users(data)
    return render_template("editar_viaje.html", viaje=viaje)



@app.route("/viajes/disponibles")
def viajes_disponibles():
    if "conductor_id" not in session:
        return redirect("/")
    data = {"id": session["conductor_id"]}
    conductorX = Taxista.get_one_taxista(data)
    viajes = Ride.get_all_para_conductor()

    viajes_sin_conductor = []
    viajes_con_conductor = []
    for r in viajes:
        if(r.conductor_id == None):
            viajes_sin_conductor.append(r)
        else:
            viajes_con_conductor.append(r)

    return render_template("dashboard_taxista.html",conductor=conductorX, viajes=viajes, viajes_sin_conductor=viajes_sin_conductor, viajes_con_conductor=viajes_con_conductor)

@app.route('/viajes/<int:viaje_id>/cancel_driver')
def cancel_driver(viaje_id):
    data = {
        'id': viaje_id
    }
    Ride.cancel_driver(data)
    return redirect('/viajes/disponibles')


@app.route('/viajes/<int:viaje_id>/valor', methods=['GET','POST'])
def editar_valor_viaje(viaje_id):
    Ride.update_valor_viaje(request.form)
    return redirect(f"/viaje/en_curso/{viaje_id}/")


@app.route('/todos_los_viajes')
def todos_los_viajes():
    if "usuario_id" in session:
        usuario_id = session.get("usuario_id")
        data = { "id": usuario_id}

        cargo = User.get_cargo_usuario(data)
        cargo = cargo[0]["cargo"]

        if cargo == "administrador":
            todo_viajes = Ride.get_all()
        elif cargo == "coordinador":
            todo_viajes = Ride.get_by_usuario(usuario_id)
        else:
            todo_viajes = Ride.get_by_usuario(usuario_id)
        
        return render_template("todo_viajes.html", todo_viajes=todo_viajes)
    
    if "conductor_id" in session:
        conductor_id = session.get("conductor_id")
        data = {"id": conductor_id}
        todo_viajes = Ride.get_by_conductor(conductor_id)

        return render_template("todo_viajes.html", todo_viajes=todo_viajes)