from collections import deque

# Moves: (M, C) possible on boat
BOAT_MOVES = [(2,0), (0,2), (1,1), (1,0), (0,1)]

def valid_state(state):
    """Check if a state is safe (no missionaries eaten)."""
    ML, CL, boat, MR, CR = state

    # Check boundaries
    if ML < 0 or CL < 0 or MR < 0 or CR < 0:
        return False

    # Cannibals don't outnumber missionaries (if missionaries >0)
    if ML > 0 and CL > ML:
        return False
    if MR > 0 and CR > MR:
        return False

    return True

def successors(state):
    result = []
    ML, CL, boat, MR, CR = state

    # Determine direction
    if boat == 'L':
        sign = -1
        new_boat = 'R'
    else:
        sign = 1
        new_boat = 'L'

    for m_move, c_move in BOAT_MOVES:
        new_ML = ML + sign * m_move
        new_CL = CL + sign * c_move
        new_MR = MR - sign * m_move
        new_CR = CR - sign * c_move

        new_state = (new_ML, new_CL, new_boat, new_MR, new_CR)
        if valid_state(new_state):
            result.append(new_state)

    return result

def agenda_search(start, goal, strategy='BFS'):
    """
    strategy: 'BFS' = queue, 'DFS' = stack
    """
    if strategy not in ('BFS','DFS'):
        raise ValueError("strategy must be 'BFS' or 'DFS'")

    # Initialize agenda with start state and path
    if strategy == 'BFS':
        agenda = deque()
        agenda.append((start, [start]))
    else:
        # DFS: push/pop from right
        agenda = [(start, [start])]

    visited = set()

    while agenda:
        if strategy == 'BFS':
            state, path = agenda.popleft()
        else:
            state, path = agenda.pop()

        if state in visited:
            continue
        visited.add(state)

        # Goal test
        if state == goal:
            return path

        for next_state in successors(state):
            if next_state not in visited:
                new_path = path + [next_state]
                if strategy == 'BFS':
                    agenda.append((next_state, new_path))
                else:
                    agenda.append((next_state, new_path))

    return None

def print_solution(path):
    for step in path:
        print(step)
    print(f"\nTotal steps: {len(path)-1}")

if __name__ == "__main__":
    start = (3,3,'L',0,0)
    goal  = (0,0,'R',3,3)

    print("=== BFS Solution ===")
    solution_bfs = agenda_search(start, goal, strategy='BFS')
    print_solution(solution_bfs)

    print("\n=== DFS Solution ===")
    solution_dfs = agenda_search(start, goal, strategy='DFS')
    print_solution(solution_dfs)
