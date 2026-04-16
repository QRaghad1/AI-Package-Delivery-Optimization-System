import random
import math
from copy import deepcopy
from utils import euclidean_distance
from vehicle import Vehicle

# حساب تكلفة الحل
def total_cost(vehicles, priority_weight=4):
    shop = (0, 0)
    total_distance = 0
    total_priority_penalty = 0

    for v in vehicles:
        if not v.packages:
            continue

        current = shop
        traveled_distance = 0

        for p in v.packages:
            dist = euclidean_distance(current, p.delivery_location())
            traveled_distance += dist
            total_distance += dist

            effective_priority = 1 / p.priority
            delay_penalty = effective_priority * traveled_distance * priority_weight
            total_priority_penalty += delay_penalty

            current = p.delivery_location()

        total_distance += euclidean_distance(current, shop)

    return total_distance + total_priority_penalty

# حساب fitness بناءً على تكلفة أقل
def fitness(solution):
    cost = total_cost(solution)
    return 1 / (1 + cost)

# حساب وزن كل البضائع
def total_weight(packages):
    return sum(p.weight for p in packages)

# توليد حل عشوائي
def generate_random_solution(packages, vehicles):
    vehs = [Vehicle(v.capacity) for v in vehicles]

    def score(p):
        priority_score = 1 / p.priority
        weight_score = p.weight / 100
        noise = random.uniform(0, 0.1)
        return -(priority_score + weight_score + noise)

    sorted_packages = sorted(packages, key=score)

    for pkg in sorted_packages:
        random.shuffle(vehs)
        for v in vehs:
            if v.remaining_capacity >= pkg.weight:
                v.add_package(pkg)
                break

    return vehs

# تهيئة السكان
def initialize_population(packages, vehicles, population_size):
    return [generate_random_solution(packages, vehicles) for _ in range(population_size)]

# الاختيار بالترتيب
def rank_selection(population):
    ranked_population = sorted(population, key=fitness, reverse=True)
    n = len(ranked_population)
    ranks = list(range(n, 0, -1))
    total = sum(ranks)
    pick = random.uniform(0, total)
    current = 0
    for individual, rank in zip(ranked_population, ranks):
        current += rank
        if current >= pick:
            return deepcopy(individual)

# التزاوج
def crossover(parent1, parent2):
    num_vehicles = len(parent1)
    split_point = num_vehicles // 2

    child = [Vehicle(v.capacity) for v in parent1]
    used_packages = set()

    for i in range(split_point):
        for pkg in parent1[i].packages:
            if pkg not in used_packages and child[i].add_package(pkg):
                used_packages.add(pkg)

    for v in parent2:
        for pkg in v.packages:
            if pkg not in used_packages:
                for c in child:
                    if c.add_package(pkg):
                        used_packages.add(pkg)
                        break

    return child

# الطفرة
def mutate(solution, mutation_rate):
    if random.random() < mutation_rate:
        return mutate_solution(solution)
    return deepcopy(solution)

# تطبيق الطفرة
def mutate_solution(current_solution):
    new_solution = deepcopy(current_solution)
    action = random.choice(['swap_between', 'swap_within', 'move_package'])

    vehicles = [v for v in new_solution if v.packages]
    if len(vehicles) < 2:
        return new_solution

    if action == 'swap_between':
        v1, v2 = random.sample(vehicles, 2)
        if v1.packages and v2.packages:
            i = random.randint(0, len(v1.packages) - 1)
            j = random.randint(0, len(v2.packages) - 1)
            p1, p2 = v1.packages[i], v2.packages[j]

            if v1.remove_package(p1) and v2.remove_package(p2):
                if v1.add_package(p2) and v2.add_package(p1):
                    pass
                else:
                    v1.remove_package(p2)
                    v2.remove_package(p1)
                    v1.add_package(p1)
                    v2.add_package(p2)

    elif action == 'swap_within':
        v = random.choice(vehicles)
        if len(v.packages) >= 2:
            i, j = random.sample(range(len(v.packages)), 2)
            v.packages[i], v.packages[j] = v.packages[j], v.packages[i]

    elif action == 'move_package':
        v_from, v_to = random.sample(vehicles, 2)
        if v_from.packages:
            pkg = random.choice(v_from.packages)
            if v_to.remaining_capacity >= pkg.weight:
                if v_from.remove_package(pkg):
                    v_to.add_package(pkg)

    return new_solution

# الخوارزمية الجينية الرئيسية (مع إرجاع الطرود غير الموزعة)
def genetic_algorithm(packages, vehicles, population_size=50, mutation_rate=0.05, generations=500):
    population = initialize_population(packages, vehicles, population_size)
    best_solution = max(population, key=fitness)
    best_score = fitness(best_solution)

    for generation in range(generations):
        new_population = []
        for _ in range(population_size):
            parent1 = rank_selection(population)
            parent2 = rank_selection(population)
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate)
            new_population.append(child)
        population = new_population
        current_best = max(population, key=fitness)
        current_score = fitness(current_best)
        if current_score > best_score:
            best_solution = current_best
            best_score = current_score

    # تحديد الطرود غير الموزعة
    assigned_packages = set()
    for v in best_solution:
        assigned_packages.update(v.packages)

    unassigned_packages = [pkg for pkg in packages if pkg not in assigned_packages]

    return best_solution, total_cost(best_solution), unassigned_packages