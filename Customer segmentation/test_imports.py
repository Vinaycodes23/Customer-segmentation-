import pandas as pd
import numpy as np
from sqlalchemy import create_engine

print("Pandas version:", pd.__version__)
print("NumPy version:", np.__version__)
print("SQLAlchemy version:", create_engine("sqlite:///test.db").dialect.name)