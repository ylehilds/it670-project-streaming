# Streaming Data Pipeline with MongoDB

A portfolio-ready **streaming data ingestion and analysis pipeline** built with **Python** and **MongoDB**. The project demonstrates how to pull records from a source stream (e.g., a CSV feeder or external API), transform them, and persist them to MongoDB for downstream querying and notebook-based analysis. It includes ready-to-run scripts, a sample dataset, extraction utilities, and Jupyter notebooks.

## What This Project Does
- **Streams data** from a source (e.g., `thanksgiving.csv` or another producer) and **writes documents to MongoDB**.
- Provides **clean separation of concerns** between streaming logic and database operations (`stream*.py` vs. `mongo_db*.py`).
- Bundles a **Jupyter workflow** for quick exploration/visualization of ingested data (`jupyter/`).
- Includes a **shell utility** to export data from MongoDB for backups or offline analytics (`extractMongoData.sh`).
- Keeps credentials/config **centralized** in `auth.py` for easy switching between local and cloud MongoDB.

## Tech Stack
- **Language:** Python 3.x
- **Database:** MongoDB (local instance or cloud, e.g., Atlas)
- **Python Libraries:** see `requirements.txt` (e.g., `pymongo` for database access)
- **Notebooks:** Jupyter (optional but recommended for EDA/visualization)
- **Shell:** Bash (for data extraction)

## Repository Structure
.
├── auth.py                ← Centralized credentials/config (URI, DB, collection, etc.)  
├── mongo_db.py            ← DB utilities (connect, insert, query) — primary  
├── mongo_db_hughes.py     ← Alternate DB helper implementation/variant  
├── stream.py              ← Main streaming script (ingest → transform → MongoDB)  
├── streamHughes.py        ← Alternate/extended streaming script  
├── extractMongoData.sh    ← Shell script to export data from MongoDB  
├── jupyter/               ← Notebooks for EDA/visualization (optional)  
├── thanksgiving.csv       ← Sample dataset for ingestion/demo  
├── requirements.txt       ← Python dependencies  
└── README.md

## Quick Start

1) **Clone & Install**

   git clone https://github.com/ylehilds/it670-project-streaming.git
   cd it670-project-streaming

   # (Recommended) create and activate a virtual environment
   python -m venv .venv
   # macOS/Linux:
   source .venv/bin/activate
   # Windows (PowerShell):
   .venv\Scripts\Activate.ps1

   # Install dependencies
   pip install -r requirements.txt

2) **Configure MongoDB**

   Open `auth.py` and set your connection details (example field names; match your file):

   MONGO_URI = "mongodb://localhost:27017"
   DB_NAME = "streaming_db"
   COLLECTION_NAME = "events"

   Ensure your MongoDB server is running locally (default 27017) or set a valid cloud connection string.

3) **Stream Data Into MongoDB**

   Run the streamer:

   # Primary streamer
   python stream.py

   Typical flow:
    - The script reads records from a source (e.g., `thanksgiving.csv`) or a generator.
    - Each record is parsed/transformed into a Python dict.
    - The record is inserted (or upserted) into MongoDB via `mongo_db.py`.

4) **Explore with Jupyter (Optional)**

   # From the project root
   jupyter notebook jupyter/

   Use notebooks to:
    - Query MongoDB (or exported CSV/JSON).
    - Perform EDA with pandas (grouping, filtering, summary stats).
    - Visualize results with matplotlib/plotly/etc.

5) **Extract Data (Optional)**

   bash extractMongoData.sh

   Note: if the script relies on `mongoexport`, ensure MongoDB Database Tools are installed and on your PATH.

## Example Usage Patterns

- **Local development demo**
    1. Start MongoDB locally (`mongod`).
    2. Set `MONGO_URI = "mongodb://localhost:27017"` in `auth.py`.
    3. Run `python stream.py` to ingest `thanksgiving.csv` line-by-line (or another sample feed).
    4. Open Jupyter to analyze inserted documents.

- **Cloud deployment demo**
    1. Create a MongoDB Atlas cluster and obtain a connection string.
    2. Paste the URI in `auth.py` and whitelist your IP.
    3. Run the streamer from your machine or a server/VM.
    4. Collaborate on notebooks pointing to the same dataset.

## Typical Queries (Illustrative)

    from mongo_db import get_client

    client = get_client()  # uses auth.py under the hood
    db = client["streaming_db"]              # match DB_NAME in auth.py
    col = db["events"]                       # match COLLECTION_NAME

    # Count docs
    print("Total docs:", col.count_documents({}))

    # Find a few samples
    for doc in col.find().limit(5):
        print(doc)

    # Aggregation example (adjust fields to your schema)
    pipeline = [
        {"$match": {"category": {"$exists": True}}},
        {"$group": {"_id": "$category", "total": {"$sum": 1}}},
        {"$sort": {"total": -1}}
    ]
    for row in col.aggregate(pipeline):
        print(row)

## Troubleshooting

- **Cannot connect to MongoDB**
    - Verify `MONGO_URI` in `auth.py` (host, port, credentials).
    - For Atlas, ensure IP is whitelisted and TLS options match.

- **Ingestion is slow or stops**
    - Check the source generator/CSV path.
    - Consider batching (`insert_many`) or basic retry logic for transient errors.

- **Data doesn’t appear in notebooks**
    - Confirm you’re pointing to the same DB/collection as the streamer.
    - Restart the kernel or re-run the connection cells.

- **`extractMongoData.sh` fails**
    - Ensure `mongoexport` is installed (MongoDB Database Tools).
    - Make it executable: `chmod +x extractMongoData.sh` (macOS/Linux).

## Extending the Project

- **Producers:** Replace the CSV reader with a real-time producer (IoT sensor, REST API, message queue).
- **Schema:** Add lightweight validation or a schema registry pattern.
- **Resilience:** Introduce batching, exponential backoff, and dead-letter queues.
- **Analytics:** Add dashboards (e.g., Streamlit) or scheduled reports.
- **CI/CD:** Linting (ruff/flake8), type checks (mypy), and unit tests (pytest) with GitHub Actions.

## At a Glance

- **Ingest:** `stream.py`
- **Persist:** `mongo_db.py`
- **Analyze:** `jupyter/` notebooks
- **Extract:** `extractMongoData.sh`
- **Configure:** `auth.py`
- **Sample data:** `thanksgiving.csv`

## License & Author

- **License:** MIT — see `LICENSE`
- **Author:** Lehi Alcantara — https://www.lehi.dev — lehi@lehi.dev