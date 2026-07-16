"""
Central configartion for the price tracker project.

Keep all tunable values here so no other module hardcodes
URLs, credentials, or intervals. 
"""


import os


# --- Target site ---
BASE_URL = "https://www.newegg.com/Gaming-Laptop/Category/ID-363"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)

# --- Scrapper behaviour ---
REQUEST_TIMEOUT_SECONDS = 10
REQUEST_DELAY_SECONDS = 3        # polite delay between requests
MAX_RETRIES = 3
RETRY_BACKOFF_SECONDS = 5


# --- Threading ---
MAX_WORKER_THREADS = 5


# --- Scheduler (Phase 5) ---
SCRAPE_INTERVAL_SECONDS = 3600   # default: every hour


# --- Database (Phase 4) ---
# Never hardcode real credentials — pull from environment variables.
DATABASE_PROVIDER = "mongodb"    # "mongodb" or "supabase"
DATABASE_URI = os.environ.get("PRICE_TRACKER_DB_URI", "")
DATABASE_NAME = "price_tracker"



# --- Logging ----
LOG_DIR = "logs"
LOG_FILE = "price_tracker.log"
LOG_LEVEL = "info"