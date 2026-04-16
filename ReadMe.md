# AI Package Delivery Optimization System

An intelligent **AI-based package delivery system** that optimizes vehicle routing and package assignment using metaheuristic algorithms such as **Simulated Annealing (SA)** and **Genetic Algorithm (GA)**.

The system solves a real-world **Vehicle Routing Problem (VRP)** with constraints such as vehicle capacity, delivery priorities, and distance minimization.

---

## Overview

This project simulates a smart delivery system where multiple vehicles deliver packages from a central warehouse to different locations.

The goal is to:
- Minimize total travel distance
- Respect vehicle capacity constraints
- Prioritize urgent deliveries
- Optimize overall delivery cost using AI algorithms

---

## Key Features

### Package Management
- Add packages with:
  - Destination (X, Y coordinates)
  - Weight
  - Priority (1 = highest, 5 = lowest)

---

### Vehicle Management
- Define number of vehicles
- Assign capacity for each vehicle
- Automatically distribute packages based on constraints

---

### AI Optimization Engine
- Smart assignment of packages to vehicles
- Route optimization using AI algorithms
- Handles unassigned packages if capacity is exceeded

---

### Visualization
- Graphical route display using Matplotlib
- Shows:
  - Warehouse (starting point)
  - Delivery paths
  - Vehicle routes
  - Package order

---

## Algorithms Used

### 1. Simulated Annealing (SA)
- Starts from initial solution
- Iteratively improves routes
- Accepts worse solutions with probability to escape local minima

### 2. Genetic Algorithm (GA)
- Population-based optimization
- Uses selection, mutation, and evolution
- Finds near-optimal routing solutions

---

## Tech Stack

- Python
- Tkinter (GUI)
- Matplotlib (Visualization)
- Object-Oriented Programming (OOP)

---

## Project Structure

 - project/
 - │
 - ├── main_gui.py # Tkinter interface
 - ├── main.py # Algorithm runner
 - ├── package.py # Package model
 - ├── vehicle.py # Vehicle model
 - ├── simulated_annealing.py
 - ├── genetic_algorithm.py
 - ├── utils.py
 - │
 - └── visualization (matplotlib)


---

## How It Works

1. User adds packages (location, weight, priority)
2. User defines vehicles and capacities
3. System runs AI optimization (SA or GA)
4. Packages are assigned to vehicles
5. Routes are optimized automatically
6. Results are visualized graphically

---

## Installation

### Clone repository
   - git clone https://github.com/your-username/ai-delivery-system.git
   - cd ai-delivery-system

### Install dependencies
    pip install matplotlib

###  Run application
    python main_gui.py
---

## Example Output
 - Optimized delivery routes per vehicle

 - Total travel distance

 - Vehicle load distribution

 - Unassigned packages (if any)
---

## Objective Function

 - The system minimizes:

 - Total Euclidean distance

 - Priority-based delivery delay penalty

 - Vehicle overload violations

## Future Improvements

 - Add 2-opt local search optimization

 - Improve GA crossover strategy

 - Add real map integration (Google Maps API)

 - Convert GUI to web-based dashboard (Flask/React)

 - Add real-time tracking system

## Notes

 - This project is for educational purposes

 - It demonstrates AI optimization techniques in logistics

 - Focuses on solving VRP (Vehicle Routing Problem)

## Author

- Raghad 
-  Computer Engineering Student



