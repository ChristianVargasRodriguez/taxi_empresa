from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Taxista:
    db_name = 'taxi_empresa'
    def __init__(self,db_data):
        self.id = db_data['id']
        self.nombre = db_data['nombre']
        self.apellido = db_data['apellido']
        self.empresa = db_data['empresa']
        self.email = db_data['email']
        self.password = db_data['password']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']


    # 2) CREATE OPERATIONS
    # 2.1) Create Taxista
    @classmethod
    def save(cls,data):
        query = "INSERT INTO conductores (nombre, apellido, empresa, email, password, created_at, updated_at) VALUES(%(nombre)s, %(apellido)s, %(empresa)s, %(email)s, %(password)s, NOW(), NOW())"
        results = connectToMySQL(cls.db_name).query_db(query,data) 
        return results


    # # 1) READ OPERATIONS
    # # 1.1) Get All Taxista
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM conductores;"
        results = connectToMySQL(cls.db_name).query_db(query)
        taxista = []
        for usuario in results:
            taxista.append(cls(usuario))
        return taxista

    # # 1.2) Get One taxista By Id
    @classmethod
    def get_one_taxista(cls,data):
        query = "SELECT * FROM conductores WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    # # 1.3) Get One taxista By Email
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM conductores WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) < 1:
            return False
        return Taxista(results[0])
    
    # # 1.4) Get One User By Empresa
    @classmethod
    def get_by_empresa(cls,data):
        query = "SELECT * FROM conductores WHERE empresa = %(empresa)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) < 1:
            return False
        return Taxista(results[0])
    

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
        if not EMAIL_REGEX.match(user['email']):
            is_valid = False
            flash("Invalid Email Address.","register")
        if len(user['empresa']) < 2:
            is_valid = False
            flash("Empresa debe tener al menos 2 caracteres.","register")
        if len(user['password']) < 8:
            is_valid = False
            flash("Password debe tener al menos 8 caracteres.","register")
        if user['password'] != user['confirm']:
            is_valid = False
            flash("Passwords no coincide!","register")

        return is_valid
