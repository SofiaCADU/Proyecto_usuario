36# project_name/models/user.py
from app.config.mysqlconnection import connectToMySQL

class User:
    DB = 'esquema_user'

    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = """
                INSERT INTO usuarios (nombre, email, password)
                VALUES (%(nombre)s, %(email)s, %(password)s);
                """
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_by_email(cls, data):
        query = """
                SELECT * FROM usuarios
                WHERE email = %(email)s;
                """
        result = connectToMySQL(cls.DB).query_db(query, data)
        if not result:
            return False
        return cls(result[0])