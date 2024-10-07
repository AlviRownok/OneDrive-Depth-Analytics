
import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
file_path = 'Onedrive_Fabritech.csv'
df = pd.read_csv(file_path, encoding='ISO-8859-1')

# Calculate the depth level, starting from 'FABRITECH'
def calculate_depth_from_fabritech(path):
    if 'FABRITECH' in path:
        # Only count folders after 'FABRITECH'
        return path.split('FABRITECH', 1)[1].count('/')
    else:
        return 0

df['depth_level'] = df['Percorso'].apply(calculate_depth_from_fabritech)

# Generate the first plot: Depth Level vs Tipo di elemento
plt.figure(figsize=(10, 6))
df.groupby('depth_level')['Tipo di elemento'].value_counts().unstack().plot(kind='bar', stacked=True)
plt.title('Depth Level vs Tipo di elemento (Starting from FABRITECH)')
plt.xlabel('Depth Level')
plt.ylabel('Count')
plt.tight_layout()
plt.show()

# Generate the second plot: Depth Level vs Modificato da
plt.figure(figsize=(10, 6))
df.groupby('depth_level')['Modificato da'].value_counts().unstack().plot(kind='bar', stacked=True)
plt.title('Depth Level vs Modificato da (Starting from FABRITECH)')
plt.xlabel('Depth Level')
plt.ylabel('Count')
plt.tight_layout()
plt.show()
