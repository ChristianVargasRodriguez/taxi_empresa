import time
from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.taxista import Taxista
from flask_app.models.usuario import User
from flask_app.models.viaje import Ride
from datetime import datetime
import locale


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
    locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8')
    if viaje_actual[0]['valor_viaje'] is not None:
        viaje_actual[0]['valor_viaje'] = locale.currency(viaje_actual[0]['valor_viaje'], grouping=True, symbol=False, international=False)
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
        if r.valor_viaje is None and r.valor_viaje != 0:
            print(r.valor_viaje)
            if r.conductor_id is None:
                viajes_sin_conductor.append(r)
            else:
                viajes_con_conductor.append(r)

    return render_template("dashboard_taxista.html",conductor=conductorX, viajes_sin_conductor=viajes_sin_conductor, viajes_con_conductor=viajes_con_conductor)

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
        
        # Obtener la fecha actual
        fecha_actual = datetime.now()
        fecha_actual_form = datetime.today().strftime('%Y-%m-%d')
        # Obtener el inicio y fin del día actual
        inicio_dia_actual = fecha_actual.replace(hour=0, minute=0, second=0, microsecond=0)
        fin_dia_actual = fecha_actual.replace(hour=23, minute=59, second=59, microsecond=999999)

        # Configurar el idioma de destino en español Chile
        locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8')

        viajes_del_dia = []

        for viaje in todo_viajes:
            # Obtener la fecha del viaje
            fecha_str = viaje["created_at"].strftime('%Y-%m-%d %H:%M:%S')
            fecha_viaje = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S')
            
            fecha_formateada = fecha_viaje.strftime('%H:%M %d/%m/%Y')
            viaje["created_at"] = fecha_formateada
            
            if viaje['valor_viaje'] is not None:
                viaje['valor_viaje'] = locale.currency(viaje['valor_viaje'], grouping=True, symbol=False, international=False)
            else: 
                viaje['valor_viaje'] = 0
                
            # Verificar si el viaje está dentro del día actual
            if inicio_dia_actual <= fecha_viaje <= fin_dia_actual:
                viajes_del_dia.append(viaje)

        return render_template("todo_viajes.html", todo_viajes=viajes_del_dia, inicio_dia_actual=fecha_actual_form, fin_dia_actual=fecha_actual_form)

    if "conductor_id" in session:
        conductor_id = session.get("conductor_id")
        data = {"id": conductor_id}
        todo_viajes = Ride.get_by_conductor(conductor_id)

        # Obtener la fecha actual
        fecha_actual = datetime.now()

        # Obtener el inicio y fin del día actual
        inicio_dia_actual = fecha_actual.replace(hour=0, minute=0, second=0, microsecond=0)
        fin_dia_actual = fecha_actual.replace(hour=23, minute=59, second=59, microsecond=999999)

        # Configurar el idioma de destino en español
        locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8')

        viajes_del_dia = []

        for viaje in todo_viajes:
            # Obtener la fecha del viaje
            fecha_str = viaje["created_at"].strftime('%Y-%m-%d %H:%M:%S')
            fecha_viaje = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S')
            
            fecha_formateada = fecha_viaje.strftime('%H:%M %d/%m/%Y')
            viaje["created_at"] = fecha_formateada
            
            if viaje['valor_viaje'] is not None:
                viaje['valor_viaje'] = locale.currency(viaje['valor_viaje'], grouping=True, symbol=False, international=False)
            else: 
                viaje['valor_viaje'] = 0
                
            # Verificar si el viaje está dentro del día actual
            if inicio_dia_actual <= fecha_viaje <= fin_dia_actual:
                viajes_del_dia.append(viaje)

        return render_template("todo_viajes.html", todo_viajes=viajes_del_dia)


@app.route('/filtrar_viajes', methods = ['POST'])
def filtrar_viajes():

    if "usuario_id" in session:
        usuario_id = session.get("usuario_id")
        data = { "id": usuario_id }

        cargo = User.get_cargo_usuario(data)
        cargo = cargo[0]["cargo"]

        if cargo == "administrador":
            todo_viajes = Ride.get_all()
        elif cargo == "coordinador":
            todo_viajes = Ride.get_by_usuario(usuario_id)
        else:
            todo_viajes = Ride.get_by_usuario(usuario_id)

        # Configurar el idioma de destino en español Chile
        locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8')
        
        viajes_filtrados = []
        Filtro_Solicitantes = []

        for viaje in todo_viajes:
            
            fecha_inicio_str = request.form['fecha_inicio']
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
            fechaInicio = datetime.combine(fecha_inicio, datetime.min.time())
            
            fecha_fin_str = request.form['fecha_fin']
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
            fechaFin = datetime.combine(fecha_fin, datetime.min.time()).replace(hour=23, minute=59)

            # Obtener la fecha y hora del viaje
            fecha_str = viaje["created_at"].strftime('%Y-%m-%d %H:%M:%S')
            fecha_viaje = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S')
            
            if viaje['solicitante'] not in Filtro_Solicitantes:
                Filtro_Solicitantes.append(viaje['solicitante'])

            nom_solicitante = request.form['nom_solicitante']
            # Comparar las fechas y solicitante
            if (fechaInicio <= fecha_viaje and fecha_viaje <= fechaFin and nom_solicitante == "--Todos los Solicitantes--"):
                fecha_formateada = fecha_viaje.strftime('%H:%M %d/%m/%Y')
                viaje["created_at"] = fecha_formateada
                
                if viaje['valor_viaje'] is not None:
                    viaje['valor_viaje'] = locale.currency(viaje['valor_viaje'], grouping=True, symbol=False, international=False)
                else: 
                    viaje['valor_viaje'] = 0
                viajes_filtrados.append(viaje)
            
            elif (fechaInicio <= fecha_viaje and fecha_viaje <= fechaFin and nom_solicitante == viaje['solicitante']):
                fecha_formateada = fecha_viaje.strftime('%H:%M %d/%m/%Y')
                viaje["created_at"] = fecha_formateada
                
                if viaje['valor_viaje'] is not None:
                    viaje['valor_viaje'] = locale.currency(viaje['valor_viaje'], grouping=True, symbol=False, international=False)
                else: 
                    viaje['valor_viaje'] = 0
                viajes_filtrados.append(viaje)
                    
            fecha_inicio_format = fecha_inicio.strftime('%d/%m/%Y')
            fecha_fin_format = fecha_fin.strftime('%d/%m/%Y')


        return render_template("todo_viajes.html", todo_viajes=viajes_filtrados, fechaInicio=fecha_inicio_format, fechaFin=fecha_fin_format, Filtro_Solicitantes=Filtro_Solicitantes, inicio_dia_actual=fecha_inicio, fin_dia_actual=fecha_fin)




@app.route("/ultimo_viaje/<int:usuario_id>/")
def ultimo_viaje_usuario (usuario_id):
    data = {"usuario_id": usuario_id}
    ultimo_viaje = Ride.buscar_ultimo_viaje_de_usuario(data)
    viaje_id = ultimo_viaje[0]["viaje_id"]
    return render_template("viaje_en_curso.html", viaje=ultimo_viaje, viaje_id=viaje_id) 



@app.route('/viajes/<int:viaje_id>/cancelar_viaje', methods=['GET','POST'])
def cancelar_viaje(viaje_id):
    # POST REQUEST 
    if request.method == 'POST':
        if not Ride.detalle_viaje(request.form, "edit"):
            return redirect(f"/viajes/{viaje_id}/cancelar_viaje")
        Ride.cancelar_viaje(request.form)
        
        return redirect(f"/viaje/en_curso/{viaje_id}/")
    
    # GET REQUEST
    if 'usuario_id' not in session:
        return redirect('/')
    data = {
        'id': viaje_id
    }
    viaje = Ride.get_one_with_users(data)
    return render_template("cancelar_viaje.html", viaje=viaje)