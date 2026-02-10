# Every time you work on your project:

# 1. Activate environment
conda activate spotify_dw

# 2. Work on your project
cd spotify-data-warehouse
python scripts/load_data.py
dbt run

# 3. When done (optional)
conda deactivate
```

---

## **Complete Project Structure with Environment Files**
```
spotify-data-warehouse/
├── environment.yml              # Conda environment definition
├── requirements.txt             # Python packages
├── .gitignore                   # Don't commit environment files
├── README.md
├── terraform/
├── ansible/
├── dbt_project/
└── scripts/