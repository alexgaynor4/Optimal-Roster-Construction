import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np
from scipy.optimize import minimize


# Load the dataset containing cluster counts and wins
data_regular = pd.read_csv('Team Clusters Regular.csv')
data_playoffs = pd.read_csv('Team Clusters Playoffs.csv')

# Define the features and target variable
X = data_regular[['0', '1', '2', '3', '4', '5']]
y = data_regular['win_percentage']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X.values, y.values, test_size=0.2, random_state=42)

# Train the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate the model
print(f'Training R^2: {model.score(X_train, y_train)}')
print(f'Test R^2: {model.score(X_test, y_test)}')

mean_percentages = np.array([
    6.057572343449317,
    4.504333295300914,
    26.99703837888743,
    15.149414409008953,
    5.984043839623686,
    2.9477352857472328
])

# Define the objective function to maximize (negative of the predicted wins)
def objective(cluster_counts):
    cluster_counts_reshaped = np.array(cluster_counts).reshape(1, -1)
    return -model.predict(cluster_counts_reshaped)[0]

# Define the constraints
def total_count_constraint(cluster_counts):
    return 12 - sum(cluster_counts)

def total_percentage_constraint(cluster_counts):
    return 121 - np.dot(cluster_counts, mean_percentages)

constraints = [{'type': 'eq', 'fun': total_count_constraint},
               {'type': 'ineq', 'fun': total_percentage_constraint}]
bounds = [(0, 5), (0,5), (0,3), (0,5), (0,5), (0,5)]
initial_guess = [2, 2, 2, 2, 2, 2]  # Initial guess to start the optimization

# Perform the optimization
result = minimize(objective, initial_guess, bounds=bounds, constraints=constraints)
# Round the result to get integer values
optimal_cluster_counts = np.round(result.x).astype(int)

print(f'Optimal cluster counts: {optimal_cluster_counts}')
print(f'Predicted win percentage: {-objective(optimal_cluster_counts)}')

# Define the features and target variable
X = data_playoffs[['0', '1', '2', '3', '4', '5']]
y = data_playoffs['Wins']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X.values, y.values, test_size=0.2, random_state=42)

# Train the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate the model
print(f'Training R^2: {model.score(X_train, y_train)}')
print(f'Test R^2: {model.score(X_test, y_test)}')

mean_percentages = np.array([
    6.057572343449317,
    4.504333295300914,
    26.99703837888743,
    15.149414409008953,
    5.984043839623686,
    2.9477352857472328
])

constraints = [{'type': 'eq', 'fun': total_count_constraint},
               {'type': 'ineq', 'fun': total_percentage_constraint}]
bounds = [(0, 5), (0,5), (0,5), (0,5), (0,5), (0,5)]
initial_guess = [2, 2, 2, 2, 2, 2]  # Initial guess to start the optimization

# Perform the optimization
result = minimize(objective, initial_guess, bounds=bounds, constraints=constraints)

# Round the result to get integer values
optimal_cluster_counts = np.round(result.x).astype(int)

print(f'Optimal cluster counts: {optimal_cluster_counts}')
print(f'Predicted playoff wins: {-objective(optimal_cluster_counts)}')

