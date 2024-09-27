# Importamos los módulos necesarios
from flask import Flask, request, jsonify
import mysql.connector
from dotenv import load_dotenv
import os

# Cargamos las variables de entorno desde el archivo .env
load_dotenv()

# Creamos una instancia de la aplicación Flask
app = Flask(__name__)

# Configuración de conexión a la base de datos desde variables de entorno
db_config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME')
}

# Clase para la gestión de usuarios
class User:
    def __init__(self, db_config):
        self.db_config = db_config

    def get_all_users(self):
        return self._execute_query("SELECT * FROM users")

    def create_user(self, name, email):
        return self._execute_query("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email), commit=True)

    def update_user(self, user_id, name, email):
        return self._execute_query("UPDATE users SET name = %s, email = %s WHERE id = %s", (name, email, user_id), commit=True)

    def delete_user(self, user_id):
        return self._execute_query("DELETE FROM users WHERE id = %s", (user_id,), commit=True)

    def _execute_query(self, query, params=None, commit=False):
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params) if params else cursor.execute(query)

        if commit:
            conn.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            conn.close()
            return affected_rows
        
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

# Instanciamos la clase User
user_db = User(db_config)

# Ruta principal para verificar que la API está funcionando
@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': '¡La API está funcionando!'})

# Ruta para obtener todos los usuarios
@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = user_db.get_all_users()
        return jsonify(users)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para crear un nuevo usuario
@app.route('/users', methods=['POST'])
def create_user():
    try:
        new_user = request.json
         # Validaciones
        if 'name' not in new_user or not new_user['name']:
            return jsonify({'error': 'El nombre es obligatorio'}), 400
        if 'email' not in new_user or not new_user['email']:
            return jsonify({'error': 'El email es obligatorio'}), 400
        
        name = new_user['name']
        email = new_user['email']
        user_id = user_db.create_user(name, email)
        return jsonify({'message': 'Usuario creado exitosamente', 'id': user_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para actualizar un usuario existente
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        updated_user = request.json
        # Validaciones
        if 'name' not in updated_user or not updated_user['name']:
            return jsonify({'error': 'El nombre es obligatorio'}), 400
        if 'email' not in updated_user or not updated_user['email']:
            return jsonify({'error': 'El email es obligatorio'}), 400

        name = updated_user.get('name')
        email = updated_user.get('email')
        affected_rows = user_db.update_user(user_id, name, email)

        if affected_rows == 0:
            return jsonify({'message': 'Usuario no encontrado'}), 404
        
        return jsonify({'message': 'Usuario actualizado exitosamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para eliminar un usuario
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        affected_rows = user_db.delete_user(user_id)

        if affected_rows == 0:
            return jsonify({'message': 'Usuario no encontrado'}), 404
        
        return jsonify({'message': 'Usuario eliminado exitosamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Iniciamos la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)
