import pandas as pd

algos = ["BaB", "BFS", "CP", "Greedy"]
col_names = ["n_items", "n_trucks", "n_trucks_used", "cost", "running_time"]
numtest = [[1, 40], [0, 59], [0, 59]]

# Generate each excel file for each algorithm
for algo in algos:
    result_path = f"Output/Output-{algo}/result_{algo}.csv"
    excel_path = f"Analyze/result_{algo}.xlsx"

    df = pd.read_csv(result_path)
    data = df.iloc[:, 2:5]

    data.to_excel(excel_path, index=False, index_label= False)