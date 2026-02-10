Useful Conda commands:

created spotify_dw environment and installed ansible terraform and dbtproject 

# Install packages
pip install ansible
pip install psycopg2-binary
pip install dbt-postgres

# Verify installations
pip list | grep -E "ansible|psycopg2|dbt"

# List all your environments
conda env list

# Activate environment
conda activate spotify_dw

# Deactivate environment
conda deactivate

# Delete environment (if you mess up and want to start over)
conda env remove -n spotify_dw

# Export environment (for GitHub)
conda env export > environment.yml

# Install new package
conda activate spotify_dw
pip install package_name

# Update requirements.txt after installing new packages
pip freeze > requirements.txt