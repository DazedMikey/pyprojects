""" Factory method examples
"""

from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass
import attr
import dacite

EMPLOYEES = [
    {
        "name": "Jessica",
        "age": 26,
        "has_license": False
    },
    {
        "name": "Mathew",
        "age": 18,
        "has_license": True
    },
    {
        "name": "Sam",
        "age": 30,
        "has_license": True
    },
    {
        "name": "Bill",
        "age": 16,
        "has_license": False
    },
    {
        "name": "Bob",
        "age": 26,
        "has_license": True
    },
    {
        "name": "Anne",
        "age": 17,
        "has_license": False
    },    
]
VEHICLES = [
    {
        "color": "red",
        "style": "street"
    },
    {
        "color": "black",
        "style": "cruiser"
    },
    {
        "color": "green",
        "style": "mountain"
    },
    {
        "color": "blue",
        "style": "street"
    },
    {
        "color": "black",
        "model": "mazda",
        "year": 1998
    },
    {
        "color": "red",
        "model": "toyota",
        "year": 2006
    },
    {
        "color": "green",
        "model": "chevy",
        "year": 1978
    },
    {
        "color": "black",
        "model": "ford",
        "year": 2019
    }
]

class Transport(ABC):
    """ Transportation of goods
    """
    @abstractmethod
    def transport(self) -> str:
        ...

@dataclass
class Person:
    name: str

@dataclass
class Employee(Person):
    age: int
    has_license: bool

@dataclass
class Customer(Person):
    distance: int

@dataclass
class Bike(Transport):
    style: str
    color: str

    def transport(self) -> str:
        return f"on a {self.color} {self.style} bike!"

@dataclass
class Car(Transport):
    color: str
    model: str
    year: int

    def transport(self) -> str:
        return f"in a {self.color} {self.model}!"

class DeliveryService:
    """ Delivery service for pizza orders
    """
    def __init__(self) -> None:
        self.employees = self.load_employees(EMPLOYEES)
        self.vehicles = self.load_vehicles(VEHICLES)

    def deliver_pizza(self, customer: Customer) -> None:
        person, vehicle = self.get_transport(customer)
        print(f"{person.name} {'has a' if person.has_license else 'has no'} license, will deliver pizza {vehicle.transport()}")

    def pick_employee(self, req_license: bool) -> Employee:
        for i, employee in enumerate(self.employees):
            if not employee.has_license and req_license:
                continue
            else:
                self.employees.append(self.employees.pop(i))
                return employee

    def get_transport(self, customer: Customer) -> (Employee, Transport):
        for i, vehicle in enumerate(self.vehicles):
            if customer.distance >= 2 and vehicle.__class__ == Car:
                self.vehicles.append(self.vehicles.pop(i))
                person = self.pick_employee(True)
                break
            if customer.distance < 2 and vehicle.__class__ == Bike:
                self.vehicles.append(self.vehicles.pop(i))
                person = self.pick_employee(False)
                break
        return person, vehicle
    
    def load_employees(self, list: List[dict]) -> List[Employee]:
        roster = []
        for emp in list:
            roster.append(dacite.from_dict(Employee, emp))
        return roster

    def load_vehicles(self, list: List[dict]) -> List[Transport]:
        fleat = []
        for v in list:
            if "model" in v.keys():
                fleat.append(dacite.from_dict(Car, v))
            else:
                fleat.append(dacite.from_dict(Bike, v))

        return fleat

def main():
    ds = DeliveryService()
    while True:
        name = input("Customer Name: ")
        distance = input("Customer distance: ")

        if not name or not distance:
            break

        customer = dacite.from_dict(Customer, data = {"name": name, "distance": int(distance)})
        ds.deliver_pizza(customer)

if __name__ == "__main__":
    main()
