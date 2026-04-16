import random
import math
from copy import deepcopy
from collections import defaultdict
from utils import euclidean_distance
from vehicle import Vehicle


# ========== Cost Function ==========

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

            # كلما كانت الأولوية أعلى (رقمها أصغر)، زادت العقوبة
            effective_priority = 1 / p.priority
            delay_penalty = effective_priority * traveled_distance * priority_weight
            total_priority_penalty += delay_penalty 

            current = p.delivery_location()

        total_distance += euclidean_distance(current, shop)

    return total_distance + total_priority_penalty


# ========== Initial Solution ==========

def initial_solution(packages, vehicles):
    vehs = [Vehicle(v.capacity) for v in vehicles]
    unassigned_packages = []

    def score(p):
        priority_score = 1 / p.priority
        weight_score = p.weight / 100
        noise = random.uniform(0, 0.1)
        return -(priority_score + weight_score + noise)

    sorted_packages = sorted(packages, key=score)

    for pkg in sorted_packages:
        random.shuffle(vehs)
        placed = False
        for v in vehs:
            if v.remaining_capacity >= pkg.weight:
                v.add_package(pkg)
                placed = True
                break
        if not placed:
            unassigned_packages.append(pkg)

    # طباعة الحل النهائي بعد إضافة الطرود للمركبات
    print("\nFinal Distribution of Packages to Vehicles:")
    for i, v in enumerate(vehs):
        print(f"Vehicle {i+1} (Capacity: {v.capacity}):")
        if v.packages:
            for pkg in v.packages:
                print(f"  - Package (Priority: {pkg.priority}, Weight: {pkg.weight})")
        else:
            print("  No packages assigned.")

    return vehs, unassigned_packages




# ========== Improve Solution ==========

def improve_solution(current_solution):
    new_solution = deepcopy(current_solution)
    action = random.choice(['swap_between', 'swap_within', 'move_package'])

    vehicles = [v for v in new_solution if v.packages]
    if len(vehicles) < 2 and action != 'swap_within':
        return new_solution

    if action == 'swap_between':
        v1, v2 = random.sample(vehicles, 2)
        if v1.packages and v2.packages:
            i, j = random.randint(0, len(v1.packages) - 1), random.randint(0, len(v2.packages) - 1)
            p1, p2 = v1.packages[i], v2.packages[j]

            # تحقق من السعة قبل التبديل
            if (v1.remaining_capacity + p1.weight >= p2.weight and 
                v2.remaining_capacity + p2.weight >= p1.weight):
                
                # قم بإزالة الطرود أولاً
                v1.remove_package(p1)
                v2.remove_package(p2)
                
                # حاول إضافة الطرود الجديدة
                success1 = v1.add_package(p2)
                success2 = v2.add_package(p1)
                
                if not success1 or not success2:
                    # في حالة الفشل، أعد الطرود إلى أماكنها الأصلية
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
                    if not v_to.add_package(pkg):
                        # إذا فشلت الإضافة، أعد الطرد إلى المركبة الأصلية
                        v_from.add_package(pkg)

    return new_solution


# ========== Simulated Annealing ==========

def simulated_annealing(packages, vehicles, initial_temp=1000, cooling_rate=0.95, stop_temp=1):
    # الحصول على الحل الابتدائي وقائمة الطرود غير الموزعة
    current_solution, unassigned_packages = initial_solution(packages, vehicles)
    current_cost = total_cost(current_solution)

    temp = initial_temp
    iterations_per_temp = 100

    while temp > stop_temp:
        for _ in range(iterations_per_temp):
            candidate_solution = improve_solution(current_solution)
            candidate_cost = total_cost(candidate_solution)

            delta = candidate_cost - current_cost
            if delta < 0 or random.uniform(0, 1) < math.exp(-delta / temp):
                current_solution = candidate_solution
                current_cost = candidate_cost

        temp *= cooling_rate

    # إرجاع المركبات المحسنة، الكلفة، والطرود غير الموزعة
    return current_solution, current_cost, unassigned_packages