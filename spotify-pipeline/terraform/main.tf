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

# =====================================================
# RECENTLY PLAYED
# =====================================================
resource "snowflake_table" "recently_played" {
  database = snowflake_database.spotify.name
  schema   = snowflake_schema.bronze.name
  name     = "RECENTLY_PLAYED"

  column {
    name = "TRACK_ID"
    type = "STRING"
  }
  column {
    name = "TRACK_NAME"
    type = "STRING"
  }
  column {
    name = "ARTIST_ID"
    type = "STRING"
  }
  column {
    name = "ARTIST_NAME"
    type = "STRING"
  }
  column {
    name = "ALBUM_ID"
    type = "STRING"
  }
  column {
    name = "ALBUM_NAME"
    type = "STRING"
  }
  column {
    name = "PLAYED_AT"
    type = "TIMESTAMP_NTZ"
  }
  column {
    name = "DURATION_MS"
    type = "NUMBER"
  }
  column {
    name = "EXPLICIT"
    type = "BOOLEAN"
  }
}

# =====================================================
# TOP TRACKS
# =====================================================
resource "snowflake_table" "top_tracks" {
  database = snowflake_database.spotify.name
  schema   = snowflake_schema.bronze.name
  name     = "TOP_TRACKS"

  column {
    name = "TRACK_ID"
    type = "STRING"
  }
  column {
    name = "TRACK_NAME"
    type = "STRING"
  }
  column {
    name = "ARTIST_ID"
    type = "STRING"
  }
  column {
    name = "ARTIST_NAME"
    type = "STRING"
  }
  column {
    name = "ALBUM_ID"
    type = "STRING"
  }
  column {
    name = "ALBUM_NAME"
    type = "STRING"
  }
  column {
    name = "DURATION_MS"
    type = "NUMBER"
  }
  column {
    name = "EXPLICIT"
    type = "BOOLEAN"
  }
  column {
    name = "RANK"
    type = "NUMBER"
  }
  column {
    name = "TIME_RANGE"
    type = "STRING"
  }
  column {
    name = "INGESTED_AT"
    type = "TIMESTAMP_NTZ"
  }
}

# =====================================================
# TOP ARTISTS
# =====================================================
resource "snowflake_table" "top_artists" {
  database = snowflake_database.spotify.name
  schema   = snowflake_schema.bronze.name
  name     = "TOP_ARTISTS"

  column {
    name = "ARTIST_ID"
    type = "STRING"
  }
  column {
    name = "ARTIST_NAME"
    type = "STRING"
  }
  column {
    name = "RANK"
    type = "NUMBER"
  }
  column {
    name = "TIME_RANGE"
    type = "STRING"
  }
  column {
    name = "INGESTED_AT"
    type = "TIMESTAMP_NTZ"
  }
}