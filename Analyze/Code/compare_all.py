import matplotlib.pyplot as plt

algos = ["MIP", "BaB", "BFS", "CP", "Greedy"]

n_packs = []
cost = []
run_time = []

# get data
for algo in algos:
    result_path = f"Output/Output-{algo}/result_{algo}.csv"

    with open(result_path, "r") as f:
        _n_packs=[]
        _cost=[]
        _run_time=[]

        data = f.readlines()
        col_name = data.pop(0)
        remove_fail = []
        for line in data:
            if 'N/A' not in line:
                remove_fail.append(line)

        for line in remove_fail:
            values = line.strip().split(",")
            _n_packs.append(int(values[0]))
            _cost.append(float(values[3]))
            _run_time.append(float(values[4]))

        zipped = list(zip(_n_packs, _cost, _run_time))
        zipped_sorted = sorted(zipped, key = lambda x: x[0])
        _n_packs, _cost, _run_time = zip(*zipped_sorted)
        _n_packs = list(_n_packs)
        _cost = list(_cost)
        _run_time = list(_run_time)

        n_packs.append(_n_packs)
        cost.append(_cost)
        run_time.append(_run_time)

# compare all and add subplot
colors = ["#9467bdff", "#d62728ff", "#ff7f0eff", "#2ca02cff", "#1f77b4ff"]

fig, ax = plt.subplots(figsize=(15, 9))
axins = ax.inset_axes([0.05, 0.4, 0.35, 0.35])
for i in range(5):
    if algos[i] == "BaB":
        ax.plot(n_packs[i], cost[i], "-", label = "BaB-based", color = colors[i])
        axins.plot(n_packs[i][:64], cost[i][:64], "-", color = colors[i])
    else:
        ax.plot(n_packs[i], cost[i], "-", label = algos[i], color = colors[i])
        axins.plot(n_packs[i][:64], cost[i][:64], "-", color = colors[i])


x1, x2, y1, y2 = 10, 50, 350, 4350
axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)
axins.set_xticklabels([])
axins.set_yticklabels([])
ax.indicate_inset_zoom(axins)

ax.set_ylabel('Total cost')
ax.set_xlabel('Number of items')
plt.title('Total cost (lower is better)')

# # Zoom in on the bottom left region
# ax.set_xlim(0, 50)  # Adjust x-axis limits as needed
# ax.set_ylim(0, 2000)  # Adjust y-axis limits as needed

plt.legend()
# Add grid
plt.grid(True)

plt.savefig('analyze/compare_all.png')
# plt.show()

# compare run time of fisrt 25 input
fig, ax = plt.subplots(figsize=(10,5))
for i in range(5):
    if algos[i] == "BaB":
        ax.plot(n_packs[i], run_time[i], "-", label = "BaB-based", color = colors[i])
    else:
        ax.plot(n_packs[i], run_time[i], "-", label = algos[i], color = colors[i])

ax.set_ylabel('Run time (s)')
ax.set_xlabel('Number of items')
plt.title('Run time (lower is better)')
plt.legend()
plt.savefig('analyze/compare_all_run_time.png')
# plt.show()
