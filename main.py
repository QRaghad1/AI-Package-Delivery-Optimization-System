from package import Package
from vehicle import Vehicle
from simulated_annealing import simulated_annealing
from genetic_algorithm import genetic_algorithm

def run_algorithm_and_get_results(algorithm, vehicle_capacities, packages):
    # Create vehicles from the given list of capacities
    vehicles = [Vehicle(cap) for cap in vehicle_capacities]

    if algorithm == 'sa':
        return simulated_annealing(packages, vehicles)
    elif algorithm == 'ga':
        return genetic_algorithm(packages, vehicles, population_size=100, mutation_rate=0.08)
    else:
        raise ValueError("Invalid algorithm")



