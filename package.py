class Package:
    def __init__(self, x, y, weight, priority):
        self.to_x = x  # الوجهة
        self.to_y = y
        self.weight = weight
        self.priority = priority

    def delivery_location(self):
        return (self.to_x, self.to_y)

    def pickup_location(self):
        return (0, 0)  # المتجر دائمًا هو نقطة الانطلاق
    
    
    def __eq__(self, other):
        return (self.weight == other.weight and
                self.to_x == other.to_x and
                self.to_y == other.to_y and
                self.priority == other.priority)

    def __hash__(self):
        return hash((self.weight, self.to_x, self.to_y, self.priority))