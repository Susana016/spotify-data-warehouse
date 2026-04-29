from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import snowflake.connector
from datetime import datetime, timezone

# -----------------------
# LOAD ENV
# -----------------------
load_dotenv()

# -----------------------
# SPOTIFY AUTH
# -----------------------
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    scope="user-top-read user-read-recently-played"
))

# -----------------------
# SNOWFLAKE CONNECTION
# -----------------------
conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA"),
)

cur = conn.cursor()

cur.execute("SELECT CURRENT_DATABASE(), CURRENT_SCHEMA(), CURRENT_WAREHOUSE()")
db, schema, wh = cur.fetchone()
print(f"Connected to: database={db}, schema={schema}, warehouse={wh}")

me = sp.current_user()
print(f"Authenticated as: {me['display_name']} ({me['id']})")


def safe_get(obj, *keys, default=None):
    """Safely traverse nested dicts and lists."""
    for key in keys:
        if obj is None:
            return default
        if isinstance(obj, list):
            if not isinstance(key, int) or key >= len(obj):
                return default
            obj = obj[key]
        elif isinstance(obj, dict):
            obj = obj.get(key)
        else:
            return default
    return obj if obj is not None else default


try:
    # =====================================================
    # 1. RECENTLY PLAYED
    # =====================================================
    print("\n--- recently played ---")
    recent = sp.current_user_recently_played(limit=50)
    count = 0

    for item in recent["items"]:
        track = item.get("track")
        if not track:
            continue
        try:
            cur.execute("""
                INSERT INTO BRONZE.RECENTLY_PLAYED
                    (TRACK_ID, TRACK_NAME, ARTIST_ID, ARTIST_NAME, ALBUM_ID, ALBUM_NAME, PLAYED_AT, DURATION_MS, EXPLICIT)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                track.get("id"),
                track.get("name"),
                safe_get(track, "artists", 0, "id") if track.get("artists") else None,
                safe_get(track, "artists", 0, "name") if track.get("artists") else None,
                safe_get(track, "album", "id"),
                safe_get(track, "album", "name"),
                item.get("played_at"),
                track.get("duration_ms"),
                track.get("explicit"),
            ))
            count += 1
        except Exception as e:
            print(f"  ERROR inserting recently played track '{track.get('name')}': {e}")

    print(f"Inserted {count} recently played tracks")


    # =====================================================
    # 2. TOP TRACKS (short / medium / long term)
    # =====================================================
    print("\n--- top tracks ---")

    for time_range in ["short_term", "medium_term", "long_term"]:
        results = sp.current_user_top_tracks(limit=50, time_range=time_range)
        count = 0

        for rank, track in enumerate(results["items"], start=1):
            try:
                cur.execute("""
                    INSERT INTO BRONZE.TOP_TRACKS
                        (TRACK_ID, TRACK_NAME, ARTIST_ID, ARTIST_NAME, ALBUM_ID, ALBUM_NAME, DURATION_MS, EXPLICIT, RANK, TIME_RANGE, INGESTED_AT)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    track.get("id"),
                    track.get("name"),
                    safe_get(track, "artists", 0, "id") if track.get("artists") else None,
                    safe_get(track, "artists", 0, "name") if track.get("artists") else None,
                    safe_get(track, "album", "id"),
                    safe_get(track, "album", "name"),
                    track.get("duration_ms"),
                    track.get("explicit"),
                    rank,
                    time_range,
                    datetime.now(timezone.utc)
                ))
                count += 1
            except Exception as e:
                print(f"  ERROR inserting top track '{track.get('name')}': {e}")

        print(f"  {time_range}: inserted {count} tracks")


    # =====================================================
    # 3. TOP ARTISTS (short / medium / long term)
    # =====================================================
    print("\n--- top artists ---")

    for time_range in ["short_term", "medium_term", "long_term"]:
        results = sp.current_user_top_artists(limit=50, time_range=time_range)
        count = 0

        for rank, artist in enumerate(results["items"], start=1):
            try:
                cur.execute("""
                    INSERT INTO BRONZE.TOP_ARTISTS
                        (ARTIST_ID, ARTIST_NAME, RANK, TIME_RANGE, INGESTED_AT)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    artist.get("id"),
                    artist.get("name"),
                    rank,
                    time_range,
                    datetime.now(timezone.utc)
                ))
                count += 1
            except Exception as e:
                print(f"  ERROR inserting top artist '{artist.get('name')}': {e}")

        print(f"  {time_range}: inserted {count} artists")


    # =====================================================
    # COMMIT
    # =====================================================
    conn.commit()
    print("\nCommit successful.")

except Exception as e:
    print(f"\nFATAL ERROR: {e}")
    conn.rollback()
    raise

finally:
    cur.close()
    conn.close()

print("Spotify ingestion complete.")