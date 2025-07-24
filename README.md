# Food Analyzer 🍎

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Pandas Version](https://img.shields.io/badge/pandas-1.3.0%2B-150458.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A Python package for analyzing nutritional compound concentrations in foods and identifying the best food sources for specific nutrients.


## 🚀 Features

- **Database Creation**: Merges and processes food data, compounds, and nutritional contents
- **Interactive Analysis**: Search for foods richest in specific compounds
- **Automatic Ranking**: Ranks foods by decreasing concentration
- **Flexible Export**: Generates custom CSV reports
- **Configurable Setup**: Supports environment variables for custom paths


## 📦 Installation

### Prerequisites

- Python 3.8 or newer
- pandas 1.3.0 or newer

### Standard Installation

```bash
# Clone repository
git clone https://github.com/SimFour64/Nutricheck_FoodDB.git
cd Nutricheck_FoodDB

# Install package
pip install -e .
```

## 🎯 Quick Start

### 1. Prepare Your Data

Place your CSV files in the `Nutricheck_FoodDB/data/data_raw/` folder:
- `foods.csv`: List of foods with columns `id`, `name`
- `compounds.csv`: List of compounds with columns `id`, `name` ,`other_identifiers`
- `contents.csv`: Nutritional contents with columns `food_id`, `source_id`, `source_type`, `orig_content`

### 2. Create Database

```bash
python -c "from Nutricheck_FoodDB.core.database import create_db; create_db()"
```

**Expected interaction:**
```
⏳ Creating database...
📂 Database saved!
```

### 3. Analyze Compounds

```bash
python -c "from food_analyzer.core.analysis import get_ranked_foods; get_ranked_foods()"
```

**Example interaction:**
```
Enter a comma-separated list of compounds: Protein,Vitamin C,Iron
🔍 Searching for: Protein, Vitamin C, Iron
🚀 Food list saved!
```

## 📂 Data Structure

### Input File Format

**foods.csv**
```csv
id,name_foods,category
1,Spinach,Vegetables
2,Beef,Meat
3,Orange,Fruits
```

**compounds.csv**
```csv
id,name_compounds,unit
1,Protein,g
2,Vitamin C,mg
3,Iron,mg
```

**contents.csv**
```csv
food_id,source_id,source_type,orig_content
1,1,Compound,2.9
1,2,Compound,28.1
2,1,Compound,26.0
```

### Output Format

The generated report contains:
- `compound_name`: Name of the nutritional compound
- `food_rank`: Food rank (1 = highest concentration)
- `food_name`: Name of the food
- `concentration`: Compound concentration


## ⚙️ Advanced Configuration

### Environment Variables

Customize paths via environment variables:

```bash
# Custom paths
export FOOD_DATA_RAW_PATH="/my/path/data/"
export FOOD_DATABASE_PATH="/my/path/db/"
export FOOD_RESULTS_PATH="/my/path/results/"

# Custom parameters
export FOOD_TOP_N="10"      # Top 10 instead of 5
```

## 💻 Programmatic Usage

```python
from food_analyzer.core.database import create_db
from food_analyzer.core.analysis import get_ranked_foods, filter_compounds, get_top_compounds
import pandas as pd

# Create database
create_db()

# Programmatic analysis (without user interaction)
compounds_df = pd.read_csv("path/to/ranked_compounds.csv")
filtered = filter_compounds(compounds_df, ["Protein", "Iron"])
top_foods = get_top_compounds(filtered, top_n=3)
print(top_foods)
```

## 🗂️ Project Structure

```
Nutricheck_FoodDB/
└── Nutricheck_FoodDB/
    ├── core/
    │   ├── database.py      # Database creation
    │   └── analysis.py      # Compound analysis
    ├── config.py            # Configuration
    └── data/                # Default data
```
