import numpy as np

world = []
with open('map/map1.txt', 'r') as f:
    lines = f.read().splitlines()
    for line in lines:
        world.append(line.split('.'))

for i in range(len(world)):
    for j in range(len(world[i])):
        if world[i][j] == 'A':
            start = (i, j)

def adj(a, x):
    arr = []
    i = x[0]
    j = x[1]
    if i - 1 >= 0:
        arr.append((i - 1, j))
    if j - 1 >= 0:
        arr.append((i, j - 1))
    if i + 1 <= len(a) - 1:
        arr.append((i + 1, j))
    if j + 1 <= len(a) - 1:
        arr.append((i, j + 1))
    return arr

B = np.full_like(world, 0, dtype=int)
P = np.full_like(world, 0, dtype=int)
S = np.full_like(world, 0, dtype=int)
W = np.full_like(world, 0, dtype=int)
visited = []
safe = [start]
safe.extend(adj(world, start))
stack = [start]
prev = {}

def update_map(x):
    for cell in adj(world, x):
        if B[x] == 1:
            P[cell] = 1
            if cell in safe and cell not in visited:
                safe.remove(cell)
        if S[x] == 1:
            W[cell] = 1
            if cell in safe and cell not in visited:
                safe.remove(cell)
    for i in range(len(world) - 1):
        for j in range(len(world) - 1):
            if B[i, j] == 1 and S[i, j] == 0 and B[i + 1, j + 1] == 0 and S[i + 1, j + 1] == 1:
                P[i, j + 1] = 0
                W[i, j + 1] = 0
                P[i + 1, j] = 0
                W[i + 1, j] = 0
                if (i, j + 1) not in safe:
                    safe.append((i, j + 1))
                if (i + 1, j) not in safe:
                    safe.append((i + 1, j))
        for j in range(1, len(world)):
            if B[i, j] == 1 and S[i, j] == 0 and B[i + 1, j - 1] == 0 and S[i + 1, j - 1] == 1:
                P[i, j - 1] = 0
                W[i, j - 1] = 0
                P[i + 1, j] = 0
                W[i + 1, j] = 0
                if (i, j - 1) not in safe:
                    safe.append((i, j - 1))
                if (i + 1, j) not in safe:
                    safe.append((i + 1, j))

ramify = []
            
def update_ramify():
    for i in ramify:
        num_visit = 0
        for j in adj(world, i):
            if (j in visited) or (W[j] == 1) or (P[j] == 1):
                num_visit += 1
        if num_visit >= len(adj(world, i)):
            ramify.remove(i)
            
def update_stack():
    for i in stack:
        if (W[i] == 1) or (P[i] == 1):
            stack.remove(i)

def goback_bfs(start, end):
    parent = {}
    queue = [start]
    bfs_visited = []
    path = []
    while len(queue) > 0:
        browse_cur = queue[0]
        bfs_visited.append(browse_cur)
        queue = queue[1:]
        if browse_cur == end:
            path = [end]
            while path[-1] != start:
                path.append(parent[path[-1]])
            path.reverse()
            return path[1:]
        for adjacent in adj(world, browse_cur):
            if (adjacent not in queue) and (adjacent in safe) and (adjacent not in bfs_visited):
                parent[adjacent] = browse_cur
                queue.append(adjacent)
            
            
def get_agent_path(stack):
    path = []
    num_gold = 0
    ramify = []
    
    while len(stack) != 0:
        update_stack()
        cur = stack[-1]
        stack = stack[:-1]
        if world[cur] == '-':
            for i in adj(world, cur):
                if i not in safe:
                    safe.append(i)
        if cur not in visited:
            path.append(cur)
            visited.append(cur)
            if 'G' in world[cur]:
                num_gold = 1
            if 'B' in world[cur]:
                B[cur] = 1
                if cur not in safe:
                    safe.append(cur)
            if 'S' in world[cur]:
                S[cur] = 1
                if cur not in safe:
                    safe.append(cur)
            update_map(cur)
            update_ramify()
            num_direc = 0
            for i in adj(world, cur):
                if (i not in visited) & (P[i] != 1) & (W[i] != 1):
                    stack.append(i)
                    prev[i] = cur
                    num_direc += 1
            
            if num_direc > 1:
                ramify.append(cur)
            elif num_direc == 0:
                update_ramify()
                if len(ramify) > 0:
                    path.extend(goback_bfs(cur, ramify[-1]))
                else:
                    path.extend(goback_bfs(cur, start))
                    break
    print(f'path: {path}')
    return path



get_agent_path(stack)
# print(f'path: {path}')
# print(len(path))
# num_gold

