from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime


class Ride:
    db_name = "taxis_empresa"

    def __init__(self, db_data):
        self.id = db_data["id"]
        self.direccion_inicio = db_data["direccion_inicio"]
        self.direccion_destino = db_data["direccion_destino"]
        self.detalles = db_data["detalles"] if db_data["detalles"] else None
        self.usuario_id = db_data["usuario_id"]
        self.conductor_id = db_data["conductor_id"] if db_data["conductor_id"] else None
        self.valor_viaje = db_data["valor_viaje"] if db_data["valor_viaje"] else None
        self.created_at = db_data["created_at"]
        self.updated_at = db_data["updated_at"]

        # ------ Pyhon Sorthand If Else ------
        # self.usuario = db_data["usuario"] if db_data["usuario"] else None
        # self.conductor = db_data["conductor"] if db_data["conductor"] else None



    # 2) CREATE OPERATIONS
    # 2.1) Crear Viaje
    @classmethod
    def save(cls, data):
        print(data)
        query = "INSERT INTO viajes (direccion_inicio, direccion_destino, detalles, usuario_id, conductor_id, valor_viaje, created_at, updated_at)\
                VALUES (%(direccion_inicio)s, %(direccion_destino)s, %(detalles)s, %(usuario_id)s, NULL, NULL, NOW(), NOW());"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results





    # # 1) READ OPERATIONS
    # # 1.1) Obtener todos los Viajes
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM viajes LEFT JOIN usuarios ON usuario.id = viajes.usuario_id LEFT JOIN conductores ON conductores.id = viajes.conductor_id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        viajes = []
        for row in results:
            if row["conductores.nombre"]:
                conductor = row["conductores.nombre"] + " " + row["conductores.apellido"]
            else:
                conductor = None

            data = {
                "id": row["id"],
                "direccion_inicio": row["direccion_inicio"],
                "direccion_destino": row["direccion_destino"],
                # "rideshare_date": datetime.strptime(row["rideshare_date"], "%Y-%m-%d").date() if row["rideshare_date"] != "" else "",
                "detalles": row["detalles"],
                "solicitante_id": row["solicitante_id"],
                "conductor_id": row["conductor_id"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
                "solicitante": (row["nombre"] + " " + row["apellido"]),
                "conductor": conductor 
            }
            viajes.append(cls(data))

        return viajes
    
    # # 1.2) Get One Ride with rider and driver
    @classmethod
    def get_one_with_users(cls, data):
        query =  "SELECT * FROM viajes LEFT JOIN usuarios ON usuario.id = viajes.usuario_id LEFT JOIN conductores ON conductores.id = viajes.conductor_id WHERE viaje.id= %(id)s ;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        row = results[0]
        
        # if row['conductores.nombre']:
        #     driver = row['conductores.nombre'] + " " + row['conductores.apellido']
        # else:
        #     driver = None
        
        data_2 = {
            "id" : row["id"],
            "usuario_id": row["usuario_id"],
            "direccion_inicio": row["direccion_inicio"],
            "direccion_destino": row["direccion_destino"],
            # "rideshare_date": datetime.strptime(row["rideshare_date"], "%Y-%m-%d").date() if row["rideshare_date"] != "" else "",
            "detalles": row["detalles"],
            "conductor_id": row["conductor_id"],
            "created_at" : row['created_at'],
            "updated_at" : row['updated_at'],
            "solicitante" : row['usuarios.nombre'] + " " + row['usuarios.apellido'],
            "conductor" : row['conductores.nombre'] + " " + row['conductores.apellido']
        }
        
        ride = cls(data_2)
        return ride


    # # 3) UPDATE OPERATIONS
    # # 3.1) Modificar Viaje
    @classmethod
    def update_viaje(cls, data):
        query = "UPDATE viajes SET direccion_inicio=%(direccion_inicio)s, direccion_destino=%(direccion_destino)s, detalles=%(detalles)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def update_valor_viaje(cls, data):
        query = "UPDATE viajes SET valor_viaje=%(valor_viaje)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    





    
    # # 3.2) Agregar Conductor
    @classmethod
    def add_driver(cls, data):
        query = "UPDATE viajes SET conductor_id=%(conductor_id)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    # # 3.3) Conductor Cancela Viaje
    # @classmethod
    # def cancel_driver(cls, data):
    #     query = "UPDATE viajes SET conductor_id=NULL WHERE id = %(id)s;"
    #     return connectToMySQL(cls.db_name).query_db(query, data)

    # # 4) DELETE OPERATIONS
    # # 4.1) Borrar Viaje
    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM viajes WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

        # 5) VALIDATIOS
    # 5.1) Validate Viaje
    @staticmethod
    def validate_ride(ride,type):
        is_valid = True
        if type == 'new' and len(ride['direccion_inicio']) < 8:
            is_valid = False
            flash("Direccion de inicio debe contener al menos 8 caracteres.","ride")
        if len(ride['direccion_destino']) < 8:
            is_valid = False
            flash("Direccion de destino debe contener al menos 8 caracteres.","ride")
        return is_valid