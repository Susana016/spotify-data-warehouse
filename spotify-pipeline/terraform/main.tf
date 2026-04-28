# Business resources

resource "snowflake_database" "spotify" {
  name = "SPOTIFY_DB"
}

resource "snowflake_schema" "bronze" {
  database = snowflake_database.spotify.name
  name     = "BRONZE"
}

resource "snowflake_schema" "silver" {
  database = snowflake_database.spotify.name
  name     = "SILVER"
}

resource "snowflake_schema" "gold" {
  database = snowflake_database.spotify.name
  name     = "GOLD"
}

resource "snowflake_warehouse" "spotify_wh" {
  name           = "SPOTIFY_WH"
  warehouse_size = "XSMALL"
  auto_suspend   = 60
  auto_resume    = true
}

resource "snowflake_table" "spotify_tracks_raw" {
  database = snowflake_database.spotify.name
  schema   = snowflake_schema.bronze.name
  name     = "SPOTIFY_TRACKS_RAW"

  column {
    name = "RAW"
    type = "VARIANT"
  }

  column {
    name = "SOURCE"
    type = "STRING"
  }

  column {
    name = "INGESTED_AT"
    type = "TIMESTAMP_NTZ"
  }
}