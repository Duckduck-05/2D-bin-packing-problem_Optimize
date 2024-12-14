import csv

algos = ["BaB", "BFS", "CP", "Greedy"]
col_names = ["n_items", "n_trucks", "n_trucks_used", "cost", "running_time"]
numtest = [[1, 40], [0, 59], [0, 59]]

# Generate each csv result file for each algorithm
for algo in algos:
    result_path = f"Output/Output-{algo}/result_{algo}.csv"
    data = []
    data.append(col_names)

    for phase in range(1, 4):
        for test in range(numtest[phase-1][0], numtest[phase-1][1]+1):
            input_path = f"Test_case/Phase_{phase}/input{test:02d}.txt"
            output_path = f"Output/Output-{algo}/Phase_{phase}/output{test:02d}.txt"
            
            with open(output_path, "r") as output_file:
                lines = output_file.readlines()
            
            if lines != ["F"]:
                trucks_used = [line.split()[1] for line in lines[:-1]]
                n_trucks_used = len(trucks_used)

                n_items, n_trucks, cost, running_time = lines[-1].split()
            else:
                with open(input_path, "r") as input_file:
                    n_items, n_trucks =  input_file.readline().split()
                n_trucks_used, cost, running_time = 'N/A', 'N/A', 'N/A'
            data.append([n_items, n_trucks, n_trucks_used, cost, running_time])

    with open(result_path, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)


