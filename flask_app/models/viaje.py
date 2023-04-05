import pymysql
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime


class Ride:
    db_name = "taxi_empresa"

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

    @classmethod
    def save(cls, data):
        print(data)
        query = "INSERT INTO viajes (direccion_inicio, direccion_destino, detalles, usuario_id, conductor_id, valor_viaje, created_at, updated_at)\
                VALUES (%(direccion_inicio)s, %(direccion_destino)s, %(detalles)s, %(usuario_id)s, NULL, NULL, NOW(), NOW());"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results


    @classmethod
    def get_all(cls):
        query = "SELECT viajes.id, viajes.direccion_inicio, viajes.direccion_destino, viajes.detalles, viajes.usuario_id, viajes.conductor_id, viajes.valor_viaje, viajes.created_at, viajes.updated_at, CONCAT(usuarios.nombre, ' ', usuarios.apellido) AS solicitante, usuarios.telefono, usuarios.email AS usuario_email, conductores.id, conductores.nombre AS conductor_nombre, conductores.apellido AS conductor_apellido, conductores.email AS conductor_email FROM viajes LEFT JOIN usuarios ON usuarios.id = viajes.usuario_id LEFT JOIN conductores ON conductores.id = viajes.conductor_id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        return results


    @classmethod
    def get_all_para_conductor(cls):
        query = "SELECT viajes.id, viajes.direccion_inicio, viajes.direccion_destino, viajes.detalles, viajes.usuario_id, viajes.conductor_id, viajes.valor_viaje, viajes.created_at, viajes.updated_at, usuarios.nombre AS usuario_nombre, usuarios.apellido AS usuario_apellido, usuarios.telefono, usuarios.email AS usuario_email, conductores.id, conductores.nombre AS conductor_nombre, conductores.apellido AS conductor_apellido, conductores.email AS conductor_email FROM viajes LEFT JOIN usuarios ON usuarios.id = viajes.usuario_id LEFT JOIN conductores ON conductores.id = viajes.conductor_id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        viajes = []
        for row in results:
            if row["conductor_nombre"]:
                conductor = row["conductor_nombre"] + " " + row["conductor_apellido"]
            else:
                conductor = None

            data = {
                "id": row["id"],
                "direccion_inicio": row["direccion_inicio"],
                "direccion_destino": row["direccion_destino"],
                "detalles": row["detalles"],
                "usuario_id": row["usuario_id"],
                "conductor_id": row["conductor_id"],
                "valor_viaje": row["valor_viaje"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
                "solicitante": (row["usuario_nombre"] + " " + row["usuario_apellido"]),
                "conductor": conductor 
            }
            viajes.append(cls(data))

        return viajes


    @classmethod
    def get_by_conductor(cls, conductor_id):
        query = "SELECT viajes.id, viajes.direccion_inicio, viajes.direccion_destino, viajes.detalles, viajes.usuario_id, viajes.conductor_id, viajes.valor_viaje, viajes.created_at, viajes.updated_at, CONCAT(usuarios.nombre, ' ', usuarios.apellido) AS solicitante, usuarios.telefono, usuarios.email AS usuario_email, conductores.id, conductores.nombre AS conductor_nombre, conductores.apellido AS conductor_apellido, conductores.email AS conductor_email FROM viajes LEFT JOIN usuarios ON usuarios.id = viajes.usuario_id LEFT JOIN conductores ON conductores.id = viajes.conductor_id WHERE viajes.conductor_id = %(conductor_id)s;"
        data = { "conductor_id": conductor_id }
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results


    @classmethod
    def get_by_usuario(cls, usuario_id):
        query = "SELECT viajes.id, viajes.direccion_inicio, viajes.direccion_destino, viajes.detalles, viajes.usuario_id, viajes.conductor_id, viajes.valor_viaje, viajes.created_at, viajes.updated_at, CONCAT(usuarios.nombre, ' ', usuarios.apellido) AS solicitante, usuarios.telefono, usuarios.email AS usuario_email, conductores.id, conductores.nombre AS conductor_nombre, conductores.apellido AS conductor_apellido, conductores.email AS conductor_email FROM viajes LEFT JOIN usuarios ON usuarios.id = viajes.usuario_id LEFT JOIN conductores ON conductores.id = viajes.conductor_id WHERE viajes.usuario_id = %(usuario_id)s"
        data = { "usuario_id": usuario_id }
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results


    @classmethod
    def get_one_with_users(cls, data):
        query =  "SELECT viajes.id, viajes.usuario_id, viajes.direccion_inicio, viajes.direccion_destino, viajes.detalles, viajes.conductor_id, viajes.created_at, viajes.updated_at, viajes.valor_viaje, CONCAT(usuarios.nombre, ' ', usuarios.apellido) AS solicitante, conductor.nombre AS conductor_nombre, conductor.apellido AS conductor_apellido FROM viajes LEFT JOIN usuarios as usuarios ON usuarios.id = viajes.usuario_id LEFT JOIN conductores as conductor ON conductor.id = viajes.conductor_id WHERE viajes.id= %(id)s ;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results


    @classmethod
    def editar_viaje(cls, data):
        query = "UPDATE viajes SET direccion_inicio=%(direccion_inicio)s, direccion_destino=%(direccion_destino)s, detalles=%(detalles)s WHERE id = %(viaje_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)


    @classmethod
    def update_valor_viaje(cls, data):
        query = "UPDATE viajes SET valor_viaje=%(valor_viaje)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)


    @classmethod
    def add_driver(cls, data):
        query = "UPDATE viajes SET conductor_id=%(conductor_id)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)


    @classmethod
    def cancel_driver(cls, data):
        query = "UPDATE viajes SET conductor_id=NULL WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)


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
    
    
    

    @classmethod
    def buscar_ultimo_viaje_de_usuario(cls, usuario_id):
        query = "SELECT viajes.id, viajes.direccion_inicio, viajes.direccion_destino, viajes.detalles, viajes.usuario_id, viajes.conductor_id, viajes.valor_viaje, viajes.created_at, viajes.updated_at, CONCAT(usuarios.nombre, ' ', usuarios.apellido) AS solicitante, usuarios.telefono, usuarios.email AS usuario_email, conductores.id, conductores.nombre AS conductor_nombre, conductores.apellido AS conductor_apellido, conductores.email AS conductor_email FROM viajes LEFT JOIN usuarios ON usuarios.id = viajes.usuario_id LEFT JOIN conductores ON conductores.id = viajes.conductor_id WHERE viajes.usuario_id = %(usuario_id)s ORDER BY created_at DESC LIMIT 1;"
        data = { "usuario_id": usuario_id }
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results
