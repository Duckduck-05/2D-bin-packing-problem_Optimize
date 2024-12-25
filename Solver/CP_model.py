### CP model - Group 9

from typing import List, Tuple, Dict
from ortools.sat.python import cp_model

def Input():
    """
    Reads input data from stdin and returns it in a structured format.
    
    Returns:
        Tuple[int, int, List[Tuple[int, int]], List[Tuple[int, int, int]]]:
        A tuple containing: number of items, number of trucks, 
        list of item dimensions, list of truck dimensions and costs
    """
    try:

        # Parse first line for number of items and trucks
        n_items, n_trucks = map(int, input().split())

        # Parse item dimensions
        items = [
            tuple(map(int, input().split())) 
            for i in range(n_items)
        ]

        # Parse truck dimensions and costs
        trucks = [
            tuple(map(int, input().split())) 
            for i in range(n_trucks)
        ]

        return n_items, n_trucks, items, trucks

    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid input format: {e}")


def CP(n_items: int, n_trucks: int, items: List[Tuple[int, int]], trucks: List[Tuple[int, int, int]], time_limit: int = 300) -> List[str]:
    """
    Solves the bin packing problem using Constraint Programming.
    
    Args:
        n_items (int): Number of items to pack.
        n_trucks (int): Number of trucks (bins).
        items (List[Tuple[int, int]]): List of item dimensions (width, length).
        trucks (List[Tuple[int, int, int]]): List of truck dimensions (width, length, cost).
        time_limit (int, optional): Maximum solving time in seconds. Defaults to 300.
    
    Returns:
        List[str]: A list of strings representing the solution for each item. 
                   Returns ["F"] if no feasible solution.
    """
    max_width = max(truck[0] for truck in trucks)
    max_height = max(truck[1] for truck in trucks)

    model = cp_model.CpModel()

    # Placement and rotation variables
    X = {}  # Item placement in trucks
    R = []  # Item rotation flags
    for i in range(n_items):
        R.append(model.NewBoolVar(f'item_{i}_rotated'))
        for j in range(n_trucks):
            X[i, j] = model.NewBoolVar(f'item_{i}_in_truck_{j}')

    # Truck usage tracking
    Z = [model.NewBoolVar(f'truck_{j}_is_used') for j in range(n_trucks)]

    # Coordinate variables
    r = [model.NewIntVar(0, max_width, f'r_{i}') for i in range(n_items)]
    l = [model.NewIntVar(0, max_width, f'l_{i}') for i in range(n_items)]
    t = [model.NewIntVar(0, max_height, f't_{i}') for i in range(n_items)]
    b = [model.NewIntVar(0, max_height, f'b_{i}') for i in range(n_items)]

    # Coordinate constraints with rotation handling
    for i in range(n_items):
        model.Add(r[i] == l[i] + items[i][0]).OnlyEnforceIf(R[i].Not())
        model.Add(r[i] == l[i] + items[i][1]).OnlyEnforceIf(R[i])
        model.Add(t[i] == b[i] + items[i][1]).OnlyEnforceIf(R[i].Not())
        model.Add(t[i] == b[i] + items[i][0]).OnlyEnforceIf(R[i])

    # Pack placement constraints
    for i in range(n_items):
        # Each item must be in exactly one truck
        model.Add(sum(X[i, j] for j in range(n_trucks)) == 1)

        # Item must fit in the truck it's placed in
        for j in range(n_trucks):
            model.Add(r[i] <= trucks[j][0]).OnlyEnforceIf(X[i, j])
            model.Add(t[i] <= trucks[j][1]).OnlyEnforceIf(X[i, j])

    # Non-overlap constraints
    for i in range(n_items):
        for k in range(i + 1, n_items):
            a1 = model.NewBoolVar('a1')
            model.Add(r[i] <= l[k]).OnlyEnforceIf(a1)
            model.Add(r[i] > l[k]).OnlyEnforceIf(a1.Not())

            a2 = model.NewBoolVar('a2')
            model.Add(t[i] <= b[k]).OnlyEnforceIf(a2)
            model.Add(t[i] > b[k]).OnlyEnforceIf(a2.Not())

            a3 = model.NewBoolVar('a3')
            model.Add(r[k] <= l[i]).OnlyEnforceIf(a3)
            model.Add(r[k] > l[i]).OnlyEnforceIf(a3.Not())

            a4 = model.NewBoolVar('a4')
            model.Add(t[k] <= b[i]).OnlyEnforceIf(a4)
            model.Add(t[k] > b[i]).OnlyEnforceIf(a4.Not())

            # Ensure items in the same truck do not overlap
            for j in range(n_trucks):
                model.AddBoolOr(a1, a2, a3, a4).OnlyEnforceIf(X[i, j], X[k, j])

    # Truck usage tracking
    for j in range(n_trucks):
        b1 = model.NewBoolVar('b')
        model.Add(sum(X[i, j] for i in range(n_items)) == 0).OnlyEnforceIf(b1)
        model.Add(Z[j] == 0).OnlyEnforceIf(b1)
        model.Add(sum(X[i, j] for i in range(n_items)) != 0).OnlyEnforceIf(b1.Not())
        model.Add(Z[j] == 1).OnlyEnforceIf(b1.Not())
        
    # Set objective: minimize truck usage cost
    cost = sum(Z[j] * trucks[j][2] for j in range(n_trucks))
    model.Minimize(cost)

    # Solve the model
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    status = solver.Solve(model)

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        results = []
        for i in range(n_items):
            for j in range(n_trucks):
                if solver.Value(X[i, j]) == 1:
                    truck_placement = j + 1
                    break
            results.append(f"{i + 1} {truck_placement} {solver.Value(l[i])} {solver.Value(b[i])} {solver.Value(R[i])}")
        return results
    else:
        return ["F"]


def main():
    """
    Main entry point of the script.
    Reads input, solves the bin packing problem, and prints results.
    """
    try:
        n_items, n_trucks, items, trucks = Input()
        # Let time_limit = 600s
        solution = CP(n_items, n_trucks, items, trucks, 600)

        if solution == ["F"]:
            print("F")
        else:
            for item_solution in solution:
                print(item_solution)
                
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
