### Database Query and Backup Script - Summary

This script provides the `get_query_from_db` and `exec_procedure_from_db` functions, designed to interact with a SQL Server database. It supports executing queries or stored procedures, and optionally creating backups of tables.

#### Function Usage

- **`get_query_from_db(query, table_to_backup, env_file_name=None, params=None)`**:
  - Executes a SQL query on the database.
  - Parameters:
    - `query`: A SQL query string to execute on the database.
    - `table_to_backup`: The name of a table to back up. Set this to `None` if no backup is needed.
    - `env_file_name` (optional): The path to the `.env` file containing database credentials. Defaults to `.env`.
    - `params` (optional): A dictionary of parameters to bind to the query.
  - Returns:
    - A pandas DataFrame with the query results.

- **`exec_procedure_from_db(procedure_name, table_to_backup, env_file_name=None, params=None)`**:
  - Executes a stored procedure on the database.
  - Parameters:
    - `procedure_name`: The name of the stored procedure to execute.
    - `table_to_backup`: The name of a table to back up. Set this to `None` if no backup is needed.
    - `env_file_name` (optional): The path to the `.env` file containing database credentials. Defaults to `.env`.
    - `params` (optional): A dictionary of parameters to bind to the procedure.
  - Returns:
    - A pandas DataFrame with the procedure's output.

#### Setup Instructions

1. **Environment Variables**:
   - The script requires a `.env` file to load database credentials and connection details.
   - Required variables:
     ```plaintext
     USER=
     PASSWORD=
     HOST=
     NAME=
     DRIVER=ODBC+Driver+17+for+SQL+Server
     ```
     Fill in the variables with your database details. Leave `DRIVER` unchanged unless you are using a different driver.

#### Installation

Install the package directly from PyPI:

```bash
pip install Credito_SQLViaCode

#### Examples:

- **Execute a Query**:
   ```python
   from SQLViaCode import get_query_from_db

   query = "SELECT * FROM your_table"
   result_df = get_query_from_db(query, "your_table_to_backup")
   print(result_df)
