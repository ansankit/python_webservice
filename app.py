from flask import Flask, request, jsonify
from flask_mysql import MySQL

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'yourpassword'
app.config['MYSQL_DATABASE_DB'] = 'testdb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql = MySQL()
mysql.init_app(app)

# Get all employees
@app.route('/employees', methods=['GET'])
def get_employees():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    employees = [{'id': row[0], 'name': row[1], 'role': row[2]} for row in rows]
    return jsonify(employees)

# Get employee by ID
@app.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE id = %s", (id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row:
        return jsonify({'id': row[0], 'name': row[1], 'role': row[2]})
    return jsonify({'error': 'Employee not found'}), 404

# Create employee
@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.get_json()
    name = data.get('name')
    role = data.get('role')
    if not name or not role:
        return jsonify({'error': 'Name and role required'}), 400

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO employees (name, role) VALUES (%s, %s)", (name, role))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({'id': new_id, 'name': name, 'role': role}), 201

# Update employee
@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    data = request.get_json()
    name = data.get('name')
    role = data.get('role')
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE employees SET name = %s, role = %s WHERE id = %s", (name, role, id))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    if affected == 0:
        return jsonify({'error': 'Employee not found'}), 404
    return jsonify({'id': id, 'name': name, 'role': role})

# Delete employee
@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE id = %s", (id,))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()
    if affected == 0:
        return jsonify({'error': 'Employee not found'}), 404
    return jsonify({'result': 'Employee deleted'})

if __name__ == '__main__':
    app.run(debug=True)