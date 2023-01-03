#!/usr/bin/env python3

import argparse, os, sys
from copy import deepcopy
from collections import defaultdict
from itertools import islice


def load_data(input_filename:str):

    assert(os.path.exists(input_filename))
    assert(os.path.isfile(input_filename))

    data = list()

    with open(input_filename, 'r') as ifile:
        for row in ifile.readlines():
            data.append(row.strip('\n'))

    return data


def build_grid_from_data(data:list):

    grid = list()

    for row in data:
        grid.append(list())
        for c in row:
            if c == '.':
                grid[-1].append(None)
            else:
                grid[-1].append(int(c))
    
    return grid


def print_puzzle(grid:list):

    for i,row in enumerate(grid):
        if i == 0:
            print('- - - - - - - - - - - - -')
        for j,c in enumerate(row):
            if (j) % 3 == 0:
                print('|',end=' ')
            if c is not None:
                print(c, end=' ')
            else:
                print(' ', end=' ')
            if j == len(row) - 1:
                print('|', end=' ')
        print()
        if (i + 1) % 3 == 0 or i == len(grid) - 1:
            print('- - - - - - - - - - - - -')
            

def get_block_id(row:int, col:int, N=3):
    row_idx = row // N
    col_idx = col // N
    bid = row_idx * N + col_idx
    return bid

def get_row_col_from_block_id(bid: int, N=3):
    row = N * (bid // N)
    col = N * (bid % N)
    return row, col


def check_elements(element_sets:list):
    for row in element_sets:
        for col in row:
            if len(col) > 1:
                return False
    return True

def remove_element(i, j, r, solution, element_sets, row_sets, col_sets, block_sets):
    if solution[i][j] is not None:
        return False
    if solution[i][j] == r:
        return False
    
    block_id = get_block_id(i,j)

    solution[i][j] = r
    if r in element_sets[i][j]:
        element_sets[i][j].remove(r)
    if r in row_sets[i]:
        row_sets[i].remove(r)
    if r in col_sets[j]:
        col_sets[j].remove(r)
    if r in block_sets[block_id]:
        block_sets[block_id].remove(r)

    return True


def relax_sets(solution, element_sets, row_sets, col_sets, block_sets):
    change_flag = False

    for i,row in enumerate(element_sets):
        for j,c in enumerate(row):

            if len(c) == 0:
                continue

            if len(c) == 1:
                r = list(c)[0]
                change_flag |= remove_element(i, j, r, solution, element_sets, row_sets, col_sets, block_sets)
                continue

            a = set.intersection(c, row_sets[i])
            a = set.intersection(a, col_sets[j])
            a = set.intersection(a, block_sets[get_block_id(i,j)])

            if a != c:
                change_flag = True

                element_sets[i][j] = a
                
                if len(a) == 1:
                    r = list(a)[0]
                    remove_element(i, j, r, solution, element_sets, row_sets, col_sets, block_sets)

    return change_flag


def scan_for_singles(element_sets):

    change_flag = False

    for i,row in enumerate(element_sets):
        for j,c in enumerate(row):
            if len(c) <= 1:
                continue

            for v in c:
                count = 0
                for a in range(len(row)):
                    if a == i:
                        continue
                    if v in element_sets[a][j]:
                        count += 1
                if count == 0:
                    element_sets[i][j] = { v }
                    change_flag = True
                    break
            
            if len(element_sets[i][j]) == 1:
                continue

            for v in c:
                count = 0
                for a in range(len(row)):
                    if a == j:
                        continue
                    if v in element_sets[i][a]:
                        count += 1
                if count == 0:
                    element_sets[i][j] = { v }
                    change_flag = True
                    break


    return change_flag


def union_pair_scan_vector(solution_slice, element_set_slice):

    valid_idxes = [i for i,s in enumerate(solution_slice) if s is None]

    #union_map_set = defaultdict(dict)
    match_sets = defaultdict(list)
    for i,idx in enumerate(valid_idxes):
        for c_idx in islice(valid_idxes, i+1, None):
            set_union = element_set_slice[idx].union(element_set_slice[c_idx])
            #union_map_set[idx][c_idx] = set_union
            match_sets[tuple(set_union)].append((idx, c_idx))

    change_flag = False
    for set_list, idx_pair_list in match_sets.items():
        idx_set = set()
        for idx_pair in idx_pair_list:
            idx_set = idx_set.union(set(idx_pair))
        if len(set_list) == len(idx_set) and len(idx_set) != len(valid_idxes):
            for idx in set(valid_idxes).difference(idx_set):
                dif = element_set_slice[idx].difference(set(set_list))
                if dif != element_set_slice[idx]:
                    change_flag |= True
                element_set_slice[idx] = dif
    
    return change_flag


def union_pair_scan_rows(solution, element_sets):
    
    for r_solution, r_es in zip(solution, element_sets):
        if union_pair_scan_vector(r_solution, r_es):
            return True

    return False


def union_pair_scan_cols(solution, element_sets):

    for c_idx in range(9):
        c_sol = [row[c_idx] for row in solution]
        c_es = [row[c_idx] for row in element_sets]
        if union_pair_scan_vector(c_sol, c_es):
            for idx in range(len(c_es)):
                element_sets[idx][c_idx] = c_es[idx]
            return True

    return False

def union_pair_scan_blocks(solution, element_sets, N=3):
    # Not Tested

    for bid in range(9):
        start_row, start_col = get_row_col_from_block_id(bid, N)
        idxes = list()
        b_sol = list()
        b_es = list()
        for row in range(start_row, N):
            for col in range(start_col, N):
                idxes.append((row, col))
                b_sol.append(solution[row][col])
                b_es.append(element_sets[row][col])
        b_b_es = deepcopy(b_es)
        if union_pair_scan_vector(b_sol, b_es):
            print(b_b_es)
            print(b_es)
            print(element_sets[row][col])
            for (row,col), es in zip(idxes, b_es):
                element_sets[row][col] = es
            print(element_sets[row][col])
            return True
    return False


def union_pair_scan(solution, element_sets, row_sets, col_sets, block_sets):
    if union_pair_scan_rows(solution, element_sets):
        return True
    if union_pair_scan_cols(solution, element_sets):
        return True
    #if union_pair_scan_blocks(solution, element_sets):
    #    return True
    return False
    

def solve(grid:list):
    solution = deepcopy(grid)

    element_sets = [[set([j for j in range(1,10)]) for i in row] for row in grid]
    row_sets = [set([j for j in range(1,10)]) for _ in grid]
    col_sets = [set([j for j in range(1,10)]) for _ in grid[0]]
    block_sets = [set([j for j in range(1,10)]) for _ in range(9)]

    for i,row in enumerate(solution):
        for j,c in enumerate(row):
            if c is not None:
                element_sets[i][j] = { c }
                row_sets[i].remove(c)
                col_sets[j].remove(c)
                block_sets[get_block_id(i,j)].remove(c)

    change_flag = True
    idx = 0
    while not check_elements(element_sets) and change_flag:
        change_flag = relax_sets(solution, element_sets, row_sets, col_sets, block_sets)
        if not change_flag:
            change_flag = scan_for_singles(element_sets)
        if not change_flag:
            change_flag = union_pair_scan(solution, element_sets, row_sets, col_sets, block_sets)

        print(f'Iteration {idx}')
        idx += 1
        print_puzzle(solution)

    return solution


def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('input_filename', type=str)
    args = parser.parse_args()

    data = load_data(args.input_filename)
    grid = build_grid_from_data(data)

    print('Begin :: ')
    print_puzzle(grid)

    solution = solve(grid)

    print('Solution ::')
    print_puzzle(solution)



if __name__ == '__main__':
    main()
