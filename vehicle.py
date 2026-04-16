from utils import euclidean_distance  

class Vehicle:
    def __init__(self, capacity):
        self.capacity = capacity
        self.remaining_capacity = capacity
        self.packages = []
        self.route_distance = 0.0

    def add_package(self, package):
        if package.weight <= self.remaining_capacity:
            self.packages.append(package)
            self.remaining_capacity -= package.weight
            return True
        return False

    def current_load(self):
        return self.capacity - self.remaining_capacity

    def remove_package(self, package):
        if package in self.packages:
            self.packages.remove(package)
            self.remaining_capacity += package.weight
            return True
        return False

    def calculate_route_distance(self):
        shop = (0, 0)
        current = shop
        total_distance = 0.0
        
        for p in self.packages:
            total_distance += euclidean_distance(current, (p.to_x, p.to_y))
            current = (p.to_x, p.to_y)
        
        total_distance += euclidean_distance(current, shop)
        self.route_distance = total_distance
        return total_distance
