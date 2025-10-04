import random
from z3 import Solver, Bool, PbEq, sat
from cell import Cell


def create_game_board(size, num_mines):
    board = [[Cell() for _ in range(size)] for _ in range(size)]

    num_mines = min(num_mines, size * size)
    if num_mines <= 0 and size * size > 0:
        num_mines = min(num_mines, size * size - 1) if size * size > 1 else 0

    if num_mines > 0:
        mine_positions = random.sample([(r, c) for r in range(size) for c in range(size)], num_mines)
        for r, c in mine_positions:
            board[r][c].has_mine = True

    for r in range(size):
        for c in range(size):
            if not board[r][c].has_mine:
                count = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < size and 0 <= nc < size and board[nr][nc].has_mine:
                            count += 1
                board[r][c].adjacent_mines = count
    return board


def reveal_cell_recursive(board, r, c):
    size = len(board)
    if not (0 <= r < size and 0 <= c < size):
        return

    cell = board[r][c]
    if cell.revealed or cell.flagged:
        return

    cell.revealed = True

    if cell.adjacent_mines == 0 and not cell.has_mine:
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                reveal_cell_recursive(board, r + dr, c + dc)


def check_win_condition(board):
    size = len(board)
    for r in range(size):
        for c in range(size):
            cell = board[r][c]
            if not cell.has_mine and not cell.revealed:
                return False
    return True


def analyze_board_probabilities(board):
    size = len(board)
    base_solver = Solver()
    vars_map = {}

    for r_idx in range(size):
        for c_idx in range(size):
            if not board[r_idx][c_idx].revealed:
                vars_map[(r_idx, c_idx)] = Bool(f"m_{r_idx}_{c_idx}")

    for r_idx in range(size):
        for c_idx in range(size):
            cell = board[r_idx][c_idx]
            if cell.revealed and cell.adjacent_mines >= 0:
                neighbors_coords = []
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r_idx + dr, c_idx + dc
                        if 0 <= nr < size and 0 <= nc < size and not board[nr][nc].revealed:
                            neighbors_coords.append((nr, nc))

                num_flagged_among_unrevealed_neighbors = sum(
                    1 for nr, nc in neighbors_coords if board[nr][nc].flagged
                )

                vars_list_for_constraint = [
                    vars_map[coord] for coord in neighbors_coords if coord in vars_map
                ]

                if vars_list_for_constraint:
                    base_solver.add(
                        PbEq([(v, 1) for v in vars_list_for_constraint],
                             cell.adjacent_mines - num_flagged_among_unrevealed_neighbors)
                    )

    for r in range(size):
        for c_cell_obj in board[r]:
            c_cell_obj.probability = None

    for (r_coord, c_coord), var_z3 in vars_map.items():
        if board[r_coord][c_coord].flagged:
            board[r_coord][c_coord].probability = 1.0
            continue

        s_true = Solver()
        s_true.add(base_solver.assertions())
        s_true.add(var_z3 == True)
        s_false = Solver()
        s_false.add(base_solver.assertions())
        s_false.add(var_z3 == False)

        t_sat = s_true.check() == sat
        f_sat = s_false.check() == sat

        if t_sat and not f_sat:
            board[r_coord][c_coord].probability = 1.0
        elif not t_sat and f_sat:
            board[r_coord][c_coord].probability = 0.0
        elif t_sat and f_sat:
            board[r_coord][c_coord].probability = 0.5
        else:
            board[r_coord][c_coord].probability = -1.0