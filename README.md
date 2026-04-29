# Spotify Data Warehouse

End-to-end Spotify data pipeline built with Python, Snowflake, Terraform, and dbt.

The project ingests Spotify API data into a Snowflake Bronze layer, then prepares it for downstream modeling in dbt. It is designed to be a portfolio-ready analytics project with clear infrastructure, repeatable ingestion, and a simple path to business-ready models.

## Tech Stack

- Spotify Web API
- Python
- Snowflake
- Terraform
- dbt
- GitHub Actions

## What It Does

- Pulls top tracks and playlist data from Spotify
- Loads raw records into Snowflake Bronze tables
- Manages Snowflake resources with Terraform
- Prepares the project for dbt transformations in Silver and Gold layers

## Repository Layout

```text
spotify-pipeline/
├── ingestion/
│   └── spotify_extract.py
├── terraform/
│   ├── main.tf
│   ├── outputs.tf
│   ├── snowflake.tf
│   └── variables.tf
├── dbt/
│   ├── dbt_project.yml
│   └── models/
│       ├── bronze/
│       ├── silver/
│       └── gold/
└── docs/
```

## Bronze Layer

The ingestion script writes into Snowflake Bronze tables:

- `TRACKS`
- `ARTISTS`
- `PLAYLISTS`
- `PLAYLIST_TRACKS`
- `TOP_TRACKS`

These tables store the source data before any dbt cleanup, deduplication, or aggregation.

## Setup

### 1. Create a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Add environment variables

Create a `.env` file with your Spotify and Snowflake credentials.

```env
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback

SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=SPOTIFY_DB
SNOWFLAKE_SCHEMA=BRONZE
```

## Deploy Snowflake Resources

Apply the Terraform configuration from the `spotify-pipeline/terraform` folder.

```powershell
terraform init
terraform plan
terraform apply
```

## Run the Ingestion Script

```powershell
python spotify-pipeline/ingestion/spotify_extract.py
```

## dbt Layer

The dbt project is organized to support the standard warehouse flow:

- Bronze: source tables from Snowflake
- Silver: cleaned and typed models
- Gold: business-ready reporting models

## Example Questions

- Which artists appear most often across my playlists?
- What are my top tracks over different time ranges?
- How does my listening history change over time?

## Next Improvements

- Add dbt models for deduplication and aggregation
- Add GitHub Actions for scheduled ingestion and dbt runs
- Add lineage and architecture screenshots to `docs/`
- Expand tests and data quality checks

