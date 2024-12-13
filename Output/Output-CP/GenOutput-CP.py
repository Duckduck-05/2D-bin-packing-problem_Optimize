# Model
import sys
import os
import time
from typing import List, Tuple, Dict
from ortools.sat.python import cp_model


class BinPackingSolver:
    """
    A solver for the bin packing optimization problem using CP (Constraint Programming) model.
    
    This class handles reading input data, creating a constraint satisfaction model,
    and solving the bin packing problem with optional rotation of packages.
    """

    def __init__(self, file_path: str, time_limit: int = 600):
        """
        Initialize the solver with input file and time limit.
        
        Args:
            file_path (str): Path to the input data file
            time_limit (int, optional): Maximum solving time in seconds. Defaults to 600.
        """
        self.file_path = file_path
        self.time_limit = time_limit
        self.n_packs = 0
        self.n_bins = 0
        self.packs = []
        self.bins = []
        self.max_width = 0
        self.max_height = 0
        self.minCost = 0

    def read_input(self) -> None:
        """
        Read input data from the specified file.
        
        Raises:
            FileNotFoundError: If the input file cannot be found
            ValueError: If the input file format is invalid
        """
        try:
            with open(self.file_path, 'r') as f:
                data = f.readlines()
                
                # Parse first line for number of packs and bins
                self.n_packs, self.n_bins = map(int, data[0].split())
                
                # Parse pack dimensions
                self.packs = [
                    tuple(map(int, data[i].split())) 
                    for i in range(1, self.n_packs + 1)
                ]
                
                # Parse bin dimensions and costs
                self.bins = [
                    tuple(map(int, data[i].split())) 
                    for i in range(self.n_packs + 1, len(data))
                ]
                
                # Calculate maximum bin dimensions for constraint setting
                self.max_width = max(x[0] for x in self.bins)
                self.max_height = max(x[1] for x in self.bins)

        except FileNotFoundError:
            raise FileNotFoundError(f"Input file not found: {self.file_path}")
        except (ValueError, IndexError) as e:
            raise ValueError(f"Invalid input file format: {e}")

    def create_model(self) -> Tuple[cp_model.CpModel, Dict, List, List]:
        """
        Create the constraint programming model for bin packing.
        
        Returns:
            Tuple containing the model, placement variables, rotation variables, 
            and bin usage variables
        """
        model = cp_model.CpModel()

        # Placement and rotation variables
        X = {}  # Pack placement in bins
        R = []  # Pack rotation flags
        for i in range(self.n_packs):
            R.append(model.NewBoolVar(f'package_{i}_rotated'))
            for j in range(self.n_bins):
                X[i, j] = model.NewBoolVar(f'pack_{i}_in_bin_{j}')

        # Bin usage tracking
        Z = [model.NewBoolVar(f'bin_{j}_is_used') for j in range(self.n_bins)]

        # Coordinate variables
        r = [model.NewIntVar(0, self.max_width, f'r_{i}') for i in range(self.n_packs)]
        l = [model.NewIntVar(0, self.max_width, f'l_{i}') for i in range(self.n_packs)]
        t = [model.NewIntVar(0, self.max_height, f't_{i}') for i in range(self.n_packs)]
        b = [model.NewIntVar(0, self.max_height, f'b_{i}') for i in range(self.n_packs)]

        return model, X, R, Z, r, l, t, b

    def add_constraints(self, model, X, R, Z, r, l, t, b):
        """
        Add constraints to the bin packing model.
        
        Args:
            model (cp_model.CpModel): The constraint model
            X, R, Z: Decision variables for placement, rotation, bin usage
            r, l, t, b: Coordinate variables
        """
        # Coordinate constraints with rotation handling
        for i in range(self.n_packs):
            model.Add(r[i] == l[i] + self.packs[i][0]).OnlyEnforceIf(R[i].Not())
            model.Add(r[i] == l[i] + self.packs[i][1]).OnlyEnforceIf(R[i])
            model.Add(t[i] == b[i] + self.packs[i][1]).OnlyEnforceIf(R[i].Not())
            model.Add(t[i] == b[i] + self.packs[i][0]).OnlyEnforceIf(R[i])

        # Pack placement constraints
        for i in range(self.n_packs):
            # Each pack must be in exactly one bin
            model.Add(sum(X[i, j] for j in range(self.n_bins)) == 1)

            # Pack must fit in the bin it's placed in
            for j in range(self.n_bins):
                model.Add(r[i] <= self.bins[j][0]).OnlyEnforceIf(X[i, j])
                model.Add(t[i] <= self.bins[j][1]).OnlyEnforceIf(X[i, j])

        # Non-overlap constraints
        for i in range(self.n_packs):
            for k in range(i+1, self.n_packs):
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

                # Ensure packs in the same bin do not overlap
                for j in range(self.n_bins):
                    model.AddBoolOr(a1, a2, a3, a4).OnlyEnforceIf(X[i, j], X[k, j])

        # Bin usage tracking
        for j in range(self.n_bins):
            b1 = model.NewBoolVar('b')
            model.Add(sum(X[i, j] for i in range(self.n_packs)) == 0).OnlyEnforceIf(b1)
            model.Add(Z[j] == 0).OnlyEnforceIf(b1)
            model.Add(sum(X[i, j] for i in range(self.n_packs)) != 0).OnlyEnforceIf(b1.Not())
            model.Add(Z[j] == 1).OnlyEnforceIf(b1.Not())

        return model, Z

    def solve(self) -> None:
        """
        Solve the bin packing problem and print results.
        """
        try:
            # Read input data
            self.read_input()

            # Create model and variables
            model, X, R, Z, r, l, t, b = self.create_model()

            # Add constraints
            model, Z = self.add_constraints(model, X, R, Z, r, l, t, b)

            # Set objective: minimize bin usage cost
            cost = sum(Z[j] * self.bins[j][2] for j in range(self.n_bins))
            model.Minimize(cost)

            # Solve the model
            solver = cp_model.CpSolver()
            solver.parameters.max_time_in_seconds = self.time_limit
            status = solver.Solve(model)
            
            # minCost
            self.minCost = solver.Value(cost)

            # Print results
            return self._print_results(solver, status, X, R, l, b, Z)

        except (FileNotFoundError, ValueError) as e:
            print(f"Error: {e}")
            sys.exit(1)


    def _print_results(self, solver, status, X, R, r, t, Z):
        """
        Print detailed solving results.
        
        Args:
            solver (cp_model.CpSolver): The solver object
            status (int): Solution status
            X, R, r, t, Z: Decision and coordinate variables
        """

        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            res = ""
            for i in range(self.n_packs):
                for j in range(self.n_bins):
                    if solver.Value(X[i, j]) == 1:
                        bin_placement = j + 1
                res += f"{i + 1} {bin_placement} {solver.Value(r[i])} {solver.Value(t[i])} {solver.Value(R[i])}"
                if i != self.n_packs -1:
                    res += '\n'
            return res
        else:
            return("F")
        
if __name__ == "__main__":
    numtest = [[1, 40], [0, 59], [0, 59]]
    for phase in range(1, 4):
        for test in range(numtest[phase-1][0], numtest[phase-1][1]+1):
            input_path = f"Test_case/Phase_{phase}/input{test:02d}.txt"
            output_path = f"Output/Output-CP/Phase_{phase}/output{test:02d}.txt"

            with open(input_path, "r") as input_file:
                start_time = time.time()

                solver = BinPackingSolver(input_path, 300)
                result = solver.solve()
                end_time = time.time()
                execution_time = end_time - start_time

                summary = f"{solver.n_bins} {solver.n_packs} {solver.minCost} {execution_time}"
            input_file.close()
            
            with open(output_path, "w") as output_file:
                output_file.write(result)
                if result != "F":
                    output_file.write('\n')
                    output_file.write(summary)
            output_file.close()

    # input_path = "Output/Ouput-CP/test_input.txt"
    # output_path = "Output/Ouput-CP/test_output.txt"

    # with open(input_path, "r") as input_file:
    #     start_time = time.time()

    #     solver = BinPackingSolver(input_path, 300)
    #     result = solver.solve()
    #     end_time = time.time()
    #     execution_time = end_time - start_time

    #     summary = f"{solver.n_bins} {solver.n_packs} {solver.minCost} {execution_time}"
    # input_file.close()
    
    # # print(result)
    # with open(output_path, "w") as output_file:
    #     output_file.write(result)
    #     if result != "F":
    #         output_file.write('\n')
    #         output_file.write(summary)
    # output_file.close()
