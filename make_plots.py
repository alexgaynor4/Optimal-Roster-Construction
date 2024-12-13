import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D

# Load the final dataset
final_dataset = pd.read_csv('final_player_dataset_2017_2023.csv')

# Set up the seaborn style
sns.set(style="whitegrid")

# Plot age vs. percent salary
plt.figure(figsize=(10, 6))
sns.scatterplot(x=final_dataset['Age'], y=final_dataset['PercentSalaryCap'])
plt.title('Age vs. Percent Salary Cap')
plt.xlabel('Age')
plt.ylabel('Percent Salary Cap')
plt.grid(True)
plt.show()

# Plot percent salary vs. usage rate
plt.figure(figsize=(10, 6))
sns.scatterplot(x=final_dataset['PercentSalaryCap'], y=final_dataset['UsageRate'])
plt.title('Percent Salary Cap vs. Usage Rate')
plt.xlabel('Percent Salary Cap')
plt.ylabel('Usage Rate')
plt.grid(True)
plt.show()

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Scatter plot
sc = ax.scatter(
    final_dataset['UsageRate'],
    final_dataset['Age'],
    final_dataset['PercentSalaryCap'],
    c=final_dataset['PercentSalaryCap'],  # Color by PercentSalaryCap
    cmap='viridis',
    marker='o'
)

# Add color bar which maps values to colors
cbar = plt.colorbar(sc)
cbar.set_label('Percent Salary Cap')

# Set labels
ax.set_xlabel('Usage Rate')
ax.set_ylabel('Age')
ax.set_zlabel('Percent Salary Cap')

# Set title
ax.set_title('3D Scatter Plot: Usage Rate vs Age vs Percent Salary Cap')

plt.show()