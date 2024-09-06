import math

class Truck:
    def __init__(self, xlocn, ylocn, payload, name, fuel_eff):
        self.x = xlocn
        self.y = ylocn
        self.miles = 0
        self.payload = payload
        self.name = name
        self.fuel_efficiency = fuel_eff
        self.fuel_consumed = 0
        self.tsm = 0
        self.fuel_cost_per_gallon = 10  # $10 per gallon
        self.maintenance_markup = 0.40  # 40% for maintenance and profit

    def add_miles(self, val, x_1, y_1):
        self.miles += val
        self.tsm += val
        self.x = x_1
        self.y = y_1

    def maintenance_check(self):
        if self.tsm >= 10000:
            print(f"Maintenance done for Truck {self.name}")
            self.tsm = 0

    def calculate_fuel_efficiency(self, distance):
        self.fuel_consumed = distance / self.fuel_efficiency
        fuel_cost = self.fuel_consumed * self.fuel_cost_per_gallon
        total_cost = fuel_cost * (1 + self.maintenance_markup)
        return self.fuel_consumed, total_cost

    def can_handle_delivery(self, x_2, y_2, load):
        distance = self.haversine_distance(self.x, self.y, x_2, y_2)

        if load <= self.payload:
            print(f"Truck named ({self.name}) can handle the delivery with a distance of {distance:.2f} km.")
            self.add_miles(distance, x_2, y_2)
            self.maintenance_check()
            fuel_consumed, total_cost = self.calculate_fuel_efficiency(distance)
            return True, distance, total_cost
        else:
            print(f"Truck at ({self.x}, {self.y}, {self.name}) cannot handle the delivery due to payload constraints.")
            return False, distance, None

    @staticmethod
    def haversine_distance(lat1, lon1, lat2, lon2):
        R = 6371.0  # Radius of the Earth in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c