import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

# Load the CSV file into a pandas DataFrame
data = pd.read_csv('sampledata.csv')

# Pivot the table to have one row per employee with columns for each month's leave count
pivot_table = data.pivot_table(index=['employee_id', 'leave_type'], columns='month', values='leave_count', aggfunc='sum', fill_value=0)

# Reset the index to have a flat DataFrame
pivot_table.reset_index(inplace=True)
print(pivot_table)
# Taking user input for the employee ID
employee_id = int(input("Enter the Employee ID: "))

# Taking user input for the target month
target_month = int(input("Enter the target month (1-12): "))

# Checking if the target column exists in the pivot_table
if target_month in pivot_table.columns:
    # Preparing the data for training
    X = pivot_table[pivot_table['employee_id'] == employee_id].drop(columns=[target_month, 'employee_id', 'leave_type'])
    y = pivot_table[pivot_table['employee_id'] == employee_id][target_month]

    if X.empty:
        print(f"Employee ID '{employee_id}' not found in the data.")
    else:
        # Standardizing the features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Create the Gradient Boosting regressor model
        model = GradientBoostingRegressor(n_estimators=500, learning_rate=0.05, max_depth=4, subsample=0.8, random_state=42)

        # Training the model on the sample dataset
        model.fit(X_scaled, y)

        # Trained model to predict
        new_employee_data = X_scaled[0]
        predicted_leaves = model.predict([new_employee_data])
        rounded_predicted_leaves = round(predicted_leaves[0])
        print(f'No of times Leaves will be taken: {rounded_predicted_leaves}')
else:
    print(f"Target column '{target_month}' not found in the data.")
    