from sqlalchemy import create_engine, text
from dotenv import dotenv_values
from datetime import datetime
from threading import Lock
import pandas as pd
import sqlalchemy

_engines = {} # Dictionary to store database engines for different environment files
_engine_lock = Lock() # Lock to ensure thread-safe engine creation

def connect_db(env_file_name = None):
    engine = get_engine(env_file_name)
    try:
        return engine.connect()
    except sqlalchemy.exc.OperationalError as e:
        raise Exception(f"Operational Error: {e}")
    except sqlalchemy.exc.ProgrammingError as e:
        raise Exception(f"Programming Error: {e}")
    except Exception as e:
        raise Exception(f"Unexpected Error: {e}")

def format_to_df(query_output):
    rows = query_output.fetchall()
    columns_name = pd.Index(query_output.keys())
    return pd.DataFrame(rows, columns=columns_name)

# Executes a query and optionally backs up a table
def get_query_from_db(query , table_to_backup , env_file_name = None , params = None):
    with connect_db(env_file_name) as conn:
        backup_table(table_to_backup, conn)
        query_output = conn.execute(text(query) , params)
        return format_to_df(query_output)

# Executes a procedure and optionally backs up a table
def exec_procedure_from_db(procedure_name , table_to_backup , env_file_name = None , params = None):
    with connect_db(env_file_name) as conn:
        backup_table(table_to_backup, conn)
        params_string = build_procedure_param_string(params)
        procedure_output = conn.execute(text(f"EXEC {procedure_name} {params_string}"), params)
        return format_to_df(procedure_output)

def build_procedure_param_string(params):
    if not params: # No parameters to process
        return ""
    return ", ".join([f"@{key} = :{key}" for key in params.keys()]) # Build the parameter string

# Backs up a table to a Markdown file
def backup_table(table_to_backup , conn):
    if table_to_backup == "":
        raise ValueError("Parameter 'table_to_backup' cannot be an empty string.")
    if table_to_backup is None:
        print("No backup will be performed as 'table_to_backup' is set to None.")
    else:
        backup_query = f"SELECT * FROM {table_to_backup}"
        backup_df = pd.read_sql_query(backup_query, conn)
        backup_filename = f"{table_to_backup}_backup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.md"

        try:
            with open(backup_filename, 'w') as f:
                f.write(backup_df.to_markdown(index=False))
            print(f"Table '{table_to_backup}' backed up successfully as {backup_filename}")
        except Exception as e:
            print(f"Failed to create backup: {e}")

# Creates or retrieves a database engine
def get_engine(env_file_name):
    global _engines
    env_file = env_file_name or ".env"
    if env_file not in _engines:
        with _engine_lock:
            if env_file not in _engines:
                env = dotenv_values(env_file)
                required_keys = {"USER", "PASSWORD", "HOST", "NAME", "DRIVER"}
                missing_keys = required_keys - env.keys()
                if missing_keys:
                    raise KeyError(f"Missing required environment variables: {', '.join(missing_keys)} in {env_file}")
                _engines[env_file] = create_engine(f"mssql+pyodbc://{env['USER']}:{env['PASSWORD']}@{env['HOST']}/{env['NAME']}?driver={env['DRIVER']}")
    return _engines[env_file]
