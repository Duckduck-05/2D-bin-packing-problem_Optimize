import pandas as pd

data = {
    'A': {
        'A1': {1, 2, 3},
        'A2': {4, 5, 6}
    },
    'B': {
        'B1': {1, 2, 3},
        'B2': {4, 5, 6}
    }
}

for key, value in data.items():
    print(f"{key}:")
    for subkey, subvalue in value.items():
        print(f"  {subkey}: {subvalue}")


# import pandas as pd

# Flatten the nested dictionary
flat_data = []
for key, value in data.items():
    for subkey, subvalue in value.items():
        flat_data.append([key, subkey, list(subvalue)])

# Create a DataFrame
df = pd.DataFrame(flat_data, columns=['Main Category', 'Subcategory', 'Values'])

print(df.to_latex())