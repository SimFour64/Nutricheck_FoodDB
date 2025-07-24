import os
from pathlib import Path

# Default relative paths to datafiles from root
DEFAULT_DATA_RAW_PATH = Path("Nutricheck_FoodDB/data/data_raw")
DEFAULT_DATABASE_PATH = Path("Nutricheck_FoodDB/data/database")
DEFAULT_RESULTS_PATH = Path("Nutricheck_FoodDB/data/results")

# Override parameters through environment variables
DATA_RAW_PATH = Path(os.getenv("FOOD_DATA_RAW_PATH",DEFAULT_DATA_RAW_PATH))
DATABASE_PATH = Path(os.getenv("FOOD_DATABASE_PATH",DEFAULT_DATABASE_PATH))
RESULTS_PATH = Path(os.getenv("FOOD_RESULTS_PATH",DEFAULT_RESULTS_PATH))

# Other parameters
TOP_N_FOODS = int(os.getenv("FOOD_TOP_N_FOODS",5))
