# Import the functions you want to expose
from .SQLViaCode import get_query_from_db, exec_procedure_from_db

# Define the public API of the package
__all__ = ["get_query_from_db", "exec_procedure_from_db"]
