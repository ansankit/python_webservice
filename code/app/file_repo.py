# app/file_repo.py
import json, os
from app.repository import EmployeeRepository

class FileRepo(EmployeeRepository):
    def __init__(self, filepath):
        self.filepath = filepath
        if not os.path.exists(filepath):
            with open(filepath, 'w') as f:
                json.dump([], f)

    def _read(self):
        with open(self.filepath, 'r') as f:
            return json.load(f)

    def _write(self, data):
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=2)

    def get_all(self):
        return self._read()

    def get(self, id):
        return next((emp for emp in self._read() if emp['id'] == id), None)

    def add(self, name, role):
        data = self._read()
        new_id = (max((emp['id'] for emp in data), default=0) + 1)
        new_emp = {'id': new_id, 'name': name, 'role': role}
        data.append(new_emp)
        self._write(data)
        return new_emp

    def update(self, id, name, role):
        data = self._read()
        for emp in data:
            if emp['id'] == id:
                emp.update({'name': name, 'role': role})
                self._write(data)
                return emp
        return None

    def delete(self, id):
        data = self._read()
        data = [emp for emp in data if emp['id'] != id]
        self._write(data)
        return True
