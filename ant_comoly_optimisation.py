import math, random

# ---------- Distance Matrix ----------
def compute_distance_matrix(cities):
    n = len(cities)
    dist = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dist[i][j] = math.dist(cities[i], cities[j])
    return dist

# ---------- Ant Colony Optimization ----------
def ACO_TSP(cities, n_ants=10, n_iterations=50, alpha=1, beta=2, rho=0.5, Q=100):
    n = len(cities)
    dist = compute_distance_matrix(cities)

    # initialize pheromone trails
    pheromone = [[1 for _ in range(n)] for _ in range(n)]
    best_route, best_length = None, float("inf")

    for _ in range(n_iterations):
        all_routes = []
        for _ in range(n_ants):
            route = [random.randint(0, n-1)]
            while len(route) < n:
                i = route[-1]
                probs = []
                for j in range(n):
                    if j not in route:
                        tau = pheromone[i][j] ** alpha
                        eta = (1 / dist[i][j]) ** beta
                        probs.append((j, tau * eta))
                total = sum(p for _, p in probs)
                r = random.random() * total
                s = 0
                for j, p in probs:
                    s += p
                    if s >= r:
                        route.append(j)
                        break
            route_length = sum(dist[route[i]][route[(i+1)%n]] for i in range(n))
            all_routes.append((route, route_length))
            if route_length < best_length:
                best_route, best_length = route, route_length

        # evaporate pheromone
        pheromone = [[(1-rho) * pheromone[i][j] for j in range(n)] for i in range(n)]

        # deposit pheromone
        for route, length in all_routes:
            for i in range(n):
                a, b = route[i], route[(i+1)%n]
                pheromone[a][b] += Q / length
                pheromone[b][a] += Q / length

    return best_route, best_length

# ---------- Example ----------
cities = [(0,0), (1,5), (5,2), (6,6), (8,3)]
best_route, best_length = ACO_TSP(cities)

print("Best Route (city indices):", best_route)
print("Best Route Length:", best_length)




'''
Best Route (city indices): [1, 3, 4, 2, 0]
Best Route Length: 22.35103276995244
'''
