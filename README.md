#Employee Leave Prediction Project

**Overview:**
This project builds a predictive model to forecast the number of leaves employees will take in a specific month using historical leave data stored in a SQL Server database.
It offers insights into employee leave patterns to help organizations with resource planning.

**Key Features:**
1. **Data Retrieval:** Connects to a SQL Server database and retrieves historical employee leave data.
2. **Data Transformation:** Transforms the data into a pivot table structure for modeling.
3. **Data Conversion:** Converts binary leave counts to decimal values for each month.
4. **Model Building:** Utilizes a Gradient Boosting Regressor to predict leave counts for a target month.
5. **User Input:** Prompts the user to input an employee ID and a target month.
6. **Results:** Displays the predicted number of leaves for the selected employee and month.

**Usage:**
1. Clone the repository.
2. Set up your SQL Server connection details.
3. Run the script to predict employee leaves.

**Requirements:**
- Python
- SQL Server
- Libraries: Pandas, Scikit-Learn, PyODBC
- HTML
- CSS

**Note:**
- Ensure the SQL Server table structure matches the script's expectations.
- Customize the script to fit your database and leave type.

**Contributions:** Contributions are welcome! Feel free to improve the project and create pull requests.

**Author:** Gulmini Pradhan

For more details, refer to the full documentation.
