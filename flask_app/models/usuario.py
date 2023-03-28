from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    db_name = 'taxi_empresa'
    def __init__(self,db_data):
        self.id = db_data['id']
        self.nombre = db_data['nombre']
        self.apellido = db_data['apellido']
        self.empresa = db_data['empresa']
        self.cargo = db_data['cargo']
        self.telefono = db_data['telefono']
        self.email = db_data['email']
        self.password = db_data['password']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']


    # 2) CREATE OPERATIONS
    # 2.1) Create User
    @classmethod
    def save(cls,data):
        query = "INSERT INTO usuarios (nombre, apellido, empresa, cargo, telefono, email, password, created_at, updated_at) VALUES(%(nombre)s, %(apellido)s, %(empresa)s, %(cargo)s, %(telefono)s, %(email)s, %(password)s, NOW(), NOW())"
        results = connectToMySQL(cls.db_name).query_db(query,data) 
        return results



    # 1) READ OPERATIONS
    # 1.1) Get All Users
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM usuarios;"
        results = connectToMySQL(cls.db_name).query_db(query)
        usuarios = []
        for usuario in results:
            usuarios.append(cls(usuario))
        return usuarios

    # 1.2) Get One User By Id
    @classmethod
    def get_one_usuario(cls,data):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    # 1.3) Get One User By Email
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) < 1:
            return False
        return User(results[0])
    
    # 1.4) Get One User By Empresa
    @classmethod
    def get_by_empresa(cls,data):
        query = "SELECT * FROM usuarios WHERE empresa = %(empresa)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) < 1:
            return False
        return User(results[0])
    
    # 1.5) Get One User By tipo_conductor
    # @classmethod
    # def get_by_es_conductor(cls,data):
    #     query = "SELECT * FROM usuarios WHERE es_conductor = %(es_conductor)s;"
    #     results = connectToMySQL(cls.db_name).query_db(query,data)
    #     if len(results) < 1:
    #         return None
    #     return User(results[0])


    # 3) UPDATE OPERATIONS
    # -----

    # 4) DELETE OPERATIONS
    # -----

    # 5) VALIDATIOS
    # 5.1) Validate User
    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['nombre']) < 2:
            is_valid = False
            flash("Nombre debe tener al menos 2 caracteres.","register")
        if len(user['apellido']) < 2:
            is_valid = False
            flash("Apellido debe tener al menos 2 caracteres.","register")
        if len(user['empresa']) < 2:
            is_valid = False
            flash("Empresa debe tener al menos 2 caracteres.","register")
        
        if user['cargo'] == "--Selecciona--":
            is_valid = False
            flash("Debes seleccionar tipo de cargo.","register")

        if len(user['telefono']) != 11:
            is_valid = False
            flash("Teléfono debe ser de 11 caracteres (56123456789).","register")

        if not EMAIL_REGEX.match(user['email']):
            is_valid = False
            flash("Direccion de Email Invalido.","register")

        

        if len(user['password']) < 8:
            is_valid = False
            flash("Password debe tener al menos 8 caracteres.","register")
        if user['password'] != user['confirm']:
            is_valid = False
            flash("Passwords no coincide!","register")

        return is_valid
