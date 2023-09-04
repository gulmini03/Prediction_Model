import pyodbc
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Database connection parameters
server = 'enter server name'
database = 'enter database name'
trusted_connection = 'yes' 

# Establish a connection to the SQL Server database using Windows Authentication
conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection={trusted_connection}')

# SQL query to select data
query = 'SELECT * FROM table_name'

# Fetch data from SQL Server into pandas DataFrame
data = pd.read_sql(query, conn)
#print(data)



# Pivot the table to have one row per employee with columns for each month's leave count
pivot_table = data.pivot_table(index=['employee_id', 'leave_type'], columns='month', values='leave_count', aggfunc='sum', fill_value=0)
# Reset the index to have a flat DataFrame
pivot_table.reset_index(inplace=True)
# Identify the numeric month columns (e.g., '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', etc.)
numeric_month_columns = [col for col in pivot_table.columns if col.isdigit()]

# Rename only the numeric month columns to '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', etc.
pivot_table[numeric_month_columns] = pivot_table[numeric_month_columns].rename(columns=lambda col: str(int(col)))

print(pivot_table)

# Taking user input for the employee ID
employee_id = int(input("Enter the Employee ID: "))

# Taking user input for the target month
target_month = int(input("Enter the target month (1-12): "))

# Checking if the target column exists in the pivot_table
if target_month in pivot_table.columns:
    # Training the data-Preparwation
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
conn.close()
