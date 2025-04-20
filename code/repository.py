# app/repository.py
from abc import ABC, abstractmethod

class EmployeeRepository(ABC):
    @abstractmethod
    def get_all(self): pass

    @abstractmethod
    def get(self, id): pass

    @abstractmethod
    def add(self, name, role): pass

    @abstractmethod
    def update(self, id, name, role): pass

    @abstractmethod
    def delete(self, id): pass