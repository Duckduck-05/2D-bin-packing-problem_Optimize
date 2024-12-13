import pandas as pd

data = {'Column1': [1, 2, 3], 'Column2': [4.5, 6.7, 8.9]}
df = pd.DataFrame(data)

# Convert to LaTeX
latex_table = df.to_latex(index=False) 
print(latex_table) 

# Convert to Markdown
markdown_table = df.to_markdown(index=False)
print(markdown_table)