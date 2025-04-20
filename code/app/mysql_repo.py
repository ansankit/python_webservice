# app/mysql_repo.py
from app.repository import EmployeeRepository


class MySQLRepo(EmployeeRepository):
    def __init__(self, config):
        self.config = config

    def _get_conn(self):
        try:
            import pymysql
            return pymysql.connect(
                host=self.config['host'],
                user=self.config['user'],
                password=self.config['password'],
                database=self.config['database']
            )
        except e:
            return None
            
    def get_all(self):
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees")
        result = [{'id': r[0], 'name': r[1], 'role': r[2]} for r in cursor.fetchall()]
        conn.close()
        return result

    def get(self, id):
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees WHERE id=%s", (id,))
        row = cursor.fetchone()
        conn.close()
        return {'id': row[0], 'name': row[1], 'role': row[2]} if row else None

    def add(self, name, role):
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO employees (name, role) VALUES (%s, %s)", (name, role))
        conn.commit()
        id = cursor.lastrowid
        conn.close()
        return {'id': id, 'name': name, 'role': role}

    def update(self, id, name, role):
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("UPDATE employees SET name=%s, role=%s WHERE id=%s", (name, role, id))
        conn.commit()
        conn.close()
        return {'id': id, 'name': name, 'role': role}

    def delete(self, id):
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employees WHERE id=%s", (id,))
        conn.commit()
        conn.close()
        return True
