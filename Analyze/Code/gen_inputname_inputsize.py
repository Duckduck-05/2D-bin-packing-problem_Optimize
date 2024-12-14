import pandas as pd

numtest = [[1, 40], [0, 59], [0, 59]]

input_size = []
input_size.append(["n_items", "n_trucks"])

test_name = [["Test"]]

for phase in range(1, 4):
    for i in range(numtest[phase-1][0], numtest[phase-1][1]+1):
        input_path = f"Test_case/Phase_{phase}/input{i:02d}.txt"
        test_name.append([f"Phase_{phase}/input_{i:2d}.txt"])

        with open(input_path, "r") as input_file:
            n_items, n_trucks = input_file.readline().split()
            input_size.append([n_items, n_trucks])
        input_file.close()

df_input_size = pd.DataFrame(input_size)
df_test_name = pd.DataFrame(test_name)

df_input_size.to_excel("Analyze/input_size.xlsx", index=False)
df_test_name.to_excel("Analyze/test_name.xlsx", index=False)

