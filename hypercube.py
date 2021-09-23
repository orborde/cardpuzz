import itertools

N=3
SPACE = list(range(N))
CUBE = [
    [
        [0, 1, 2],
        [0, 2, 2],
        [1, 0, 1],
    ],
    [
        [1, 2, 0],
        [0, 1, 1],
        [2, 0, 2],
    ],
    [
        [2, 0, 1],
        [2, 1, 0],
        [1, 2, 0],
    ],
]

def hypercube_solver(player, view_left, view_right):
    if player == 0:
        assert view_left == []
        row, layer = view_right
        for column in range(3):
            if CUBE[layer][row][column] == player:
                return column
        raise Exception("Not found!")
    
    if player == 1:
        column, = view_left
        layer, = view_right
        for row in range(3):
            if CUBE[layer][row][column] == player:
                return row
        raise Exception("Not found!")
    
    if player == 2:
        column, row = view_left
        assert view_right == []
        for layer in range(3):
            if CUBE[layer][row][column] == player:
                return layer
        raise Exception("Not found!")
    
    raise Exception("Invalid player!")

def pl(*args, **kwargs):
    print(*args, end=' ', **kwargs)

def check(solver, verbose=True):
    all_solved = True
    for gamestate in itertools.product(SPACE, repeat=N):
        gamestate = list(gamestate) # thanks python
        if verbose: pl(gamestate)

        solved=False
        for player in range(N):
            hidden = gamestate[player]
            view_left =  gamestate[:player]
            view_right = gamestate[player+1:]
            guess = solver(player, view_left, view_right)
            if verbose: pl(f'{player}:{guess}')
            if guess == hidden:
                if verbose: pl('✅')
                solved=True
            else:
                if verbose: pl('❌')

        all_solved = all_solved and solved
        if not solved:
            if verbose: pl('NOT SOLVED')

        if verbose: print()
    if not all_solved:
        if verbose: print('❌❌❌❌❌❌❌ FAILED TO SOLVE ALL ❌❌❌❌❌❌❌')
    return all_solved

def solve_via_map(card_mapping, player_mapping, player, view_left, view_right):
    view_left = [card_mapping[x] for x in view_left]
    view_right = [card_mapping[x] for x in view_right]
    player = player_mapping[player]

    # lazy lazy
    for x in SPACE:
        if x + sum(view_left) + sum(view_right) == player:
            return x

def solvers_equivalent(solver_a, solver_b):
    for gamestate in itertools.product(SPACE, repeat=N):
        gamestate = list(gamestate) # thanks python
        pl(gamestate)

        all_equal = True
        for player in range(N):
            view_left =  gamestate[:player]
            view_right = gamestate[player+1:]
            guess_a = solver_a(player, view_left, view_right)
            guess_b = solver_b(player, view_left, view_right)

            pl(f'{player}:{guess_a}/{guess_b}')
            if guess_a == guess_b:
                pl('✅')
            else:
                pl('❌')
                all_equal = False
        print()
        if not all_equal:
            return False
    return True

def check_solve_via_map():
    for card_perm in itertools.product(SPACE, repeat=N):
        card_mapping = {i:x for i,x in enumerate(card_perm)}

        for player_perm in itertools.product(SPACE, repeat=N):
            player_mapping = {i:x for i,x in enumerate(player_perm)}

            def map_solver(player, view_left, view_right):
                return solve_via_map(card_mapping, player_mapping, player, view_left, view_right)

            eq = solvers_equivalent(hypercube_solver, map_solver)
            pl(f'{card_perm} {player_perm}')
            if eq:
                print('✅')
                return True
            else:
                print('❌')

            print()
    print('❌❌❌❌❌❌❌ NO SOLUTIONS ❌❌❌❌❌❌❌')

assert check(hypercube_solver)
print()
check_solve_via_map()