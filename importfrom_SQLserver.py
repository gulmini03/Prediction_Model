import pyodbc
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler

# Function to sum the individual digits in a number
def sum_digits(number):
    return sum(int(digit) for digit in str(number))

# Database connection parameters
server = 'enter servername'
database = 'enter databse name'
trusted_connection = 'yes'

# Establish a connection to the SQL Server database using Windows Authentication
conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection={trusted_connection}')

# SQL query to select data
query = 'SELECT * FROM sampledata'

# Fetch data from SQL Server into pandas DataFrame
data = pd.read_sql(query, conn)

# Pivot the table to have one row per employee with columns for each month's leave count
pivot_table = data.pivot_table(index=['employee_id', 'leave_type'], columns='month', values='leave_count', aggfunc='sum', fill_value=0)
# Reset the index to have a flat DataFrame
pivot_table.reset_index(inplace=True)

# Convert all columns (except 'employee_id' and 'leave_type') to strings
pivot_table = pivot_table.astype({'employee_id': str, 'leave_type': str})
# Iterate through numeric month columns and apply the sum_digits function
for col in pivot_table.columns:
    if col not in ['employee_id', 'leave_type']:
        pivot_table[col] = pivot_table[col].apply(sum_digits)
print(pivot_table)
# Taking user input for the employee ID
employee_id = int(input("Enter the Employee ID: "))

# Taking user input for the target month
target_month = int(input("Enter the target month (1-12): "))

# Checking if the target column exists in the pivot_table
if str(target_month) in pivot_table.columns:  # Convert target_month to string here
    # Training the data-Preparation
    X = pivot_table[pivot_table['employee_id'] == str(employee_id)].drop(columns=[str(target_month), 'employee_id', 'leave_type'])
    y = pivot_table[pivot_table['employee_id'] == str(employee_id)][str(target_month)]

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
conn.close()
