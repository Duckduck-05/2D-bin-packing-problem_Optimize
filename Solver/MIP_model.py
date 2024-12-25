### MIP model - Group 9

from ortools.linear_solver import pywraplp

# function to get input data from user (type through console)
def input_data():
    n, k = (int(x) for x in input().split())
    data = {}
    data['size_item'] = []  # 'size_item': [[w0, h0], [w1, h1], ...]
    data['size_truck'] = [] # 'size_truck': [[W0, H0], [W1, H1], ...]
    data['cost'] = []       # 'cost': [c0, c1, ...]
    
    for i in range(n):
        w, h = (int(x) for x in input().split())
        data['size_item'].append([w, h])
        # w = data['size_item'][i][0]
        # h = data['size_item'][i][1]

    for j in range(k):
        w, h, c = (int(x) for x in input().split())
        data['size_truck'].append([w, h])
        data['cost'].append(c)

    W_truck = [data['size_truck'][i][0] for i in range(k)]
    H_truck = [data['size_truck'][i][1] for i in range(k)]
    return n, k, data, W_truck, H_truck

    
# MAIN SOLVER 
def process_test_case(n, k, data, W_truck, H_truck):

    max_W = max(W_truck)    
    max_H = max(H_truck)    

    # Create Solver
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Create variables
    M = 1000000 

    X = {}  # X[(i,j)] = 1 if item i is packed in truck j else 0
    o = {}  # if o = 1 then rotation = 90 degree, else 0
    Z = {}  # equals 1 if truck j is used; otherwise, 0
    l = {}  # left coordinate of item
    b = {}  # bottom coodinate of item
    r = {}  # right coordinate of item
    t = {}  # top coordinate of item
    e = {}  # e[(i, j, k)] equals 1 if both item i and item j are placed in truck k, otherwise 0
    p1 = {} # p1[(i, j, k)] equals 1 if item i is on the left of item j when in truck k, otherwise 0.
    p2 = {} # p2[(i, j, k)] equals 1 if item i is on the right of item j when in truck k, otherwise 0.
    p3 = {} # p3[(i, j, k)] equals 1 if item i is under item j when in truck k, otherwise 0.
    p4 = {} # p4[(i, j, k)] equals 1 if item i is on the top of item j when in truck k, otherwise 0.


    for i in range(n):
        # coordinate and orientation of item i 
        o[i] = solver.IntVar(0, 1, 'o[%i]' % i)
        l[i] = solver.IntVar(0, max_W, 'l[%i]' % i)
        r[i] = solver.IntVar(0, max_W, 'r[%i]' % i)
        t[i] = solver.IntVar(0, max_H, 't[%i]' % i)
        b[i] = solver.IntVar(0, max_H, 'b[%i]' % i)

        # ri = li + wi · (1 − Oi) + hi · Oi
        # ti = bi + hi · (1 − Oi) + wi · Oi
        solver.Add(r[i] == l[i] + (1 - o[i]) * data['size_item'][i][0] + o[i] * data['size_item'][i][1])
        solver.Add(t[i] == b[i] + (1 - o[i]) * data['size_item'][i][1] + o[i] * data['size_item'][i][0])

        for m in range(k):
            X[(i, m)] = solver.IntVar(0, 1, 'X_[%i]_[%i]' % (i, m)) # Xij

            # item i must not exceed area of truck
            # ri ≤ Wj + M · (1 − Xij)
            # ti ≤ Hj + M · (1 − Xij)
            solver.Add(r[i] <= (1 - X[(i, m)]) * M + W_truck[m])
            solver.Add(t[i] <= (1 - X[(i, m)]) * M + H_truck[m])

    # each item must be packed in 1 truck
    for i in range(n):
        solver.Add(sum(X[(i, m)] for m in range(k)) == 1) # iterate through k trucks, we get the sum of Xij = 1

    # if 2 items are packed in the same truck, they must not overlap
    for i in range(n - 1):
        for j in range(i + 1, n):
            for m in range(k):
                e[(i, j, m)] = solver.IntVar(0, 1, f'e[{i}][{j}][{m}]')
                solver.Add(e[(i, j, m)] >= X[(i, m)] + X[(j, m)] - 1)
                solver.Add(e[(i, j, m)] <= X[(i, m)])
                solver.Add(e[(i, j, m)] <= X[(j, m)])

                # Binary variables for each constraint
                p1[(i, j, m)] = solver.IntVar(0, 1, f'p1[{i}][{j}][{m}]')
                p2[(i, j, m)] = solver.IntVar(0, 1, f'p2[{i}][{j}][{m}]')
                p3[(i, j, m)] = solver.IntVar(0, 1, f'p3[{i}][{j}][{m}]')
                p4[(i, j, m)] = solver.IntVar(0, 1, f'p4[{i}][{j}][{m}]')

                # Constraints that the binary variables must satisfy
                solver.Add(r[i] <= l[j] + M * (1 - p1[(i, j, m)]))
                solver.Add(r[j] <= l[i] + M * (1 - p2[(i, j, m)]))
                solver.Add(t[i] <= b[j] + M * (1 - p3[(i, j, m)]))
                solver.Add(t[j] <= b[i] + M * (1 - p4[(i, j, m)]))

                solver.Add(p1[(i, j, m)] + p2[(i, j, m)] + p3[(i, j, m)] + p4[(i, j, m)] + (1 - e[(i, j, m)]) * M >= 1)
                solver.Add(p1[(i, j, m)] + p2[(i, j, m)] + p3[(i, j, m)] + p4[(i, j, m)] <= e[(i, j, m)] * M)

    # find trucks being used
    for m in range(k):
        Z[m] = solver.IntVar(0, 1, f'Z[{m}]')
        # if sum(X[i][m]) >= 1 then truck m is used => Z[m] = 1
        # else, Z[m] = 0

        q = solver.IntVar(0, n, f'q[{m}]')
        solver.Add(q == sum(X[(i, m)] for i in range(n)))
        # truck m is used if there are at least 1 item packed in it, so sum(X[(i, m)] for i in range(n)) != 0

        # q = 0 => Z[m] = 0
        # q != 0 => Z[m] = 1
        solver.Add(Z[m] <= q * M)
        solver.Add(q <= Z[m] * M)

    # objective
    cost = sum(Z[m] * data['cost'][m] for m in range(k)) # sum of used trucks * trucks' cost
    solver.Minimize(cost) # minimize that sum
    # time_limit = 300*1000 # time is in milisecond
    # solver.set_time_limit(int(time_limit))

    #start_time = time.time()
    status = solver.Solve()
    #end_time = time.time()

    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        result = []
        for i in range(n):
            item_result = [i + 1] # i: item digit 
            for j in range(k):
                if X[i, j].solution_value() == 1:
                    item_result.append(j + 1)   # t[i]: truck j the item is put in 
            item_result.append(int(l[i].solution_value()))  # x[i]: left coordinate == x
            item_result.append(int(b[i].solution_value()))  # y[i]: bottom coordinate == y
            item_result.append(int(o[i].solution_value()))  # o[i]: orientation of item
            result.append(item_result)

        # for analysis
        #num_trucks_used = int(sum(used[m].solution_value() for m in range(k)))
        #total_cost = solver.Objective().Value()
        #running_time = end_time - start_time

        # result is the output list (𝑖, 𝑡[𝑖], 𝑥[𝑖], 𝑦[𝑖], 𝑜[𝑖]) of the problem
        return result    
        #return result, n, k, num_trucks_used, total_cost, running_time  # n, k is for analysis
    else:
        return None


n, k, data, W_truck, H_truck = input_data()
#result, n, k, num_trucks_used, total_cost, running_time = process_test_case(n, k, data, W_truck, H_truck)
result = process_test_case(n, k, data, W_truck, H_truck)

# print(running_time)

for res in result:
    for i in res:
        print(i, end=" ")
    print()

    # Process each test case in the folder
    #for testcase_filename in os.listdir(testcase_folder):
    #    testcase_path = os.path.join(testcase_folder, testcase_filename)
    #    result, num_trucks_used, total_cost, running_time = process_test_case(testcase_path)
#
    #    if result is not None:
    #        print(f"Test case {testcase_filename}:")
    #         for item_result in result:
    #            print(' '.join(map(str, item_result)))
    #        print(f'Number of trucks used: {num_trucks_used}')
    #        print(f'Total cost: {total_cost}')
    #        print(f'Running time: {running_time:.4f} seconds')
    #    else:
    #        print(f"Test case {testcase_filename}: No feasible solution found")
