# coding: utf8

__author__ = 'Trebuchet clement'

S = '123456789'
ABCDEFGHI = 'ABCDEFGHI'
assignments = []


def cross(a, b):
    """Cross product of elements in a and elements in b.

    :param a: a list of string
    :param b: a list of string
    :return: list

    """

    return [s + t for s in a for t in b]


def r_string(expression):
    """human readable reversed string function

    :type expression: str
    :param expression: a string to reverse

    :return: (str)

    """
    return expression[::-1]


def _get_boxes():
    """return a list of boxes

    :return: list
    """
    return cross(rows, cols)


def _get_row_units():
    """Rows Constraint

    :return:list

    """
    return [cross(r, cols) for r in rows]


def _get_columns_unit():
    """Columns Constraint

    :return: list

    """
    return [cross(rows, c) for c in cols]


def _get_square_units(sq=3):
    """Square Constraints

    :type sq: int
    :return: list

    """

    crows = (rows[i:i + sq] for i in range(0, len(rows), sq))
    ccols = (cols[i:i + sq] for i in range(0, len(cols), sq))
    prows = tuple([x for x in crows])
    pcols = tuple([x for x in ccols])
    return [cross(rs, cs) for rs in prows for cs in pcols]


def _get_diag():
    """Diagonal Constraints

    :return: list
    """
    return [[a + b for a, b in zip(rows, cols)], [a + b for a, b in zip(rows, r_string(cols))]]


rows = '{}'.format(ABCDEFGHI)
cols = '{}'.format(S)
boxes = _get_boxes()
row_units = _get_row_units()
column_units = _get_columns_unit()
square_units = _get_square_units()
diagonals_u = _get_diag()
unitlist = row_units + column_units + square_units + diagonals_u
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - {s}) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '%s', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    for unit in unitlist:
        unit_v = [values[box] for box in unit]
        twins_num = []
        for data in unit_v:
            if unit_v.count(data) == 2 and len(data) == 2:
                twins_num.append(data)
        # Eliminate the naked twins as possibilities for their peers
        for numbers in twins_num:
            for number in numbers:
                for box in unit:
                    if values[box] != numbers:
                        values = assign_value(values, box, values[box].replace(number, ''))
    return values


def grid_values(grid):
    """Convert grid into a dict of {square: char} with '%s' for empties.

    :param grid: A grid in string form.
    :return: dict

    """
    chars = []
    for c in grid:
        if c in cols:
            chars.append(c)
        if c == '.':
            chars.append(cols)
    assert len(chars) == 81
    return dict(zip(boxes, chars))


def display(values):
    """Display the values as a 2-D grid.

    :type values: dict
    :param values: a dictionary {box: box_val}

    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values):
    """List all the solved values given in puzzle
    For each box, eliminate the solved value as a possibility in all the boxes in the peers

    :type values: dict
    :param values: a dictionary {box: box_val}
    :return:
    """
    s_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in s_values:
        digit = values[box]
        for peer in peers[box]:
            values = assign_value(values, peer, values[peer].replace(digit, ''))
    return values


def only_choice(values):
    """In every unit, check for every possible digit if it is the only choice in that unit

    :type values: dict
    :param values: a dictionary {box: box_val}
    :return: dict
    """
    for unit in unitlist:
        for digit in cols:
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values = assign_value(values, dplaces[0], digit)
    return values


def reduce_puzzle(values):
    """eliminate, only_choice and naked_twins

    :type values: dict
    :param values: a dictionary {box: box_val}
    :return: dict
    """
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = naked_twins(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """Using depth-first search and propagation, try all possible values.


    :type values: dict
    :param values: a dictionary {box: box_val}

    :return:dict
    """
    # First, use reduce puzzle strategies to narrow the solution space
    values = reduce_puzzle(values)
    if not values:
        return values
    if all(len(values[s]) == 1 for s in boxes):
        return values
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku = assign_value(new_sudoku, s, value)
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))


if __name__ == '__main__':
    diag_sudoku_grid = '4.....8.5.3..........7......2.....6.....8.4......1.......6.....5..2.....1.4......'
    solve(diag_sudoku_grid)

    try:
        from visualize import visualize_assignments

        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
