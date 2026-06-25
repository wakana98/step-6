
import sys
import math
import random
import time

from common import print_tour, read_input

def distance(city1, city2):
    return math.sqrt((city1[0]-city2[0]) ** 2 + (city1[1]-city2[1]) ** 2)

def solve(cities):
    N = len(cities)

    # 1. 距離行列の計算
    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    # 2. 初期解の生成（Greedy）
    current_point = 0
    unvisited_points = set(range(1, N))
    tour = [current_point]

    while len(unvisited_points) > 0:
        next_point = min(unvisited_points, key=lambda city: dist[current_point][city])
        unvisited_points.remove(next_point)
        tour.append(next_point)
        current_point = next_point

    tour = two_opt(tour, dist)
    tour = simulated_annealing(tour, dist)
    
    return tour

# 2-opt 
def two_opt(tour, dist):
    N = len(tour)
    while True:
        count = 0
        for i in range(N-2):
            for j in range(i+2, N):
                l1 = dist[tour[i]][tour[i + 1]]
                l2 = dist[tour[j]][tour[(j + 1) % N]]
                l3 = dist[tour[i]][tour[j]]
                l4 = dist[tour[i + 1]][tour[(j + 1) % N]]
                if l1 + l2 > l3 + l4:
                    tour[i+1 : j+1] = tour[i+1 : j+1][::-1]
                    count += 1
        if count == 0:
            break
    return tour

def simulated_annealing(tour, dist):
    N = len(tour)
    
    #パラメータ設定 ─
    DURATION = 2.5           # 実行時間（秒）
    START_TEMP = 5.0         
    END_TEMP = 0.01          # 最後はきっちり冷やす
    
    start_time = time.time()
    current_tour = list(tour)
    
    def get_total_dist(t):
        return sum(dist[t[k]][t[(k + 1) % N]] for k in range(N))
    
    best_tour = list(current_tour)
    best_dist = get_total_dist(best_tour)
    current_dist = best_dist

    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time > DURATION:
            break
            
        progress = elapsed_time / DURATION
        temp = START_TEMP * ((END_TEMP / START_TEMP) ** progress)
        
        # ランダムな2点選択の偏りを修正（平等に選ぶ）
        idx1, idx2 = random.sample(range(N), 2)
        i, j = min(idx1, idx2), max(idx1, idx2)
        if j - i < 2 or (i == 0 and j == N - 1):
            continue
        
        l1 = dist[current_tour[i]][current_tour[i + 1]]
        l2 = dist[current_tour[j]][current_tour[(j + 1) % N]]
        l3 = dist[current_tour[i]][current_tour[j]]
        l4 = dist[current_tour[i + 1]][current_tour[(j + 1) % N]]
        
        diff = (l3 + l4) - (l1 + l2)
        
        if diff < 0 or random.random() < math.exp(-diff / temp):
            current_tour[i+1 : j+1] = current_tour[i+1 : j+1][::-1]
            current_dist += diff
            
            if current_dist < best_dist:
                best_dist = current_dist
                best_tour = list(current_tour)
                
    return best_tour

if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)