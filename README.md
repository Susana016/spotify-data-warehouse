Spotify Data Pipeline — Project Plan
Stack: Spotify API · Python · Snowflake · dbt Cloud · GitHub Actions · Terraform
Goal: End-to-end cloud data pipeline, fully documented on GitHub with architecture diagram and screenshots — ready to put on a resume.


python -m venv venv  
install requirements.txt
Activate virtual environment: <venv>\Scripts\Activate.ps1

spotify-pipeline/
├── terraform/
│   ├── main.tf              # Snowflake provider config
│   ├── variables.tf         # Account, region, credentials
│   ├── snowflake.tf         # Database, schemas, warehouse, roles
│   └── outputs.tf           # Export connection values
├── ingestion/
│   └── spotify_extract.py       # Pulls from Spotify API → Snowflake raw
├── dbt/
│   ├── models/
│   │   ├── bronze/              # Raw layer (source tables)
│   │   ├── silver/              # Cleaned, typed, deduplicated
│   │   └── gold/                # Business-ready aggregations
│   └── dbt_project.yml
├── .github/
│   └── workflows/
│       └── pipeline.yml         # Scheduled GitHub Actions run
├── docs/
│   └── architecture.png         # Draw this in Excalidraw or draw.io
└── README.md                    # Most important file for recruiters


What are my most repeated artists across playlists?

1. tracks
2. artists
3. playlists
4. playlist_tracks
5. top_tracks

into bronze schema
