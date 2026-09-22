# Scrapy Catalog Crawler Application

A high-performance web scraper built with Scrapy to extract, clean, and export paginated product catalogs.

## 🚀 Getting Started

### 1. Prerequisites & Environment Setup
Make sure you have `uv` installed. Create a virtual environment and install the required dependencies:

```bash
# Create a virtual environment
uv venv

# Activate the virtual environment (Windows)
.venv\Scripts\activate

# Activate the virtual environment (macOS/Linux)
source .venv/bin/activate

# Install Scrapy
uv pip install scrapy
```

## 📁 Repository Layout

```text
scrapy/
├── scrapyapp/                  # Core Scrapy Module
│   ├── spiders/
│   │   └── spiderapp.py        # Catalog crawler & pagination extractor
│   ├── items.py                # Schema containers
│   ├── middlewares.py          # Downloader & Spider interceptors
│   ├── pipelines.py            # Data cleaning & persistence layer
│   ├── settings.py             # Crawler configuration (throttles, delays, bot name)
│   └── scrapy.cfg              # Scrapy deployment manifest
├── requirements.txt            # Dependency specifications
└── README.md
```

## 📊 Run & Crawl Execution

### 1. List Available Spiders
Verify the active spiders discovered by the Scrapy engine:
```powershell
scrapy list
```

### 2. Execute Crawl (Console Output)
Run the crawler and stream standard log data to the console:
```powershell
scrapy crawl spiderapp
```

### 3. Export Clean Data Feeds
Run the crawler and stream structured records directly to output files:

```powershell
# Export to JSON (Appends to existing data)
scrapy crawl spiderapp -o mydata.json

# Export to JSON (Overwrites existing data)
scrapy crawl spiderapp -O mydata.json

# Export to CSV
scrapy crawl spiderapp -o mydata.csv
```

## 📈 Crawl Metrics & Verification

Below are the benchmark metrics from the latest execution run:

| Metric | Value |
| :--- | :--- |
| **Item Count Extracted** | 68 products |
| **Request Count** | 4 requests (1 robots.txt + 3 paginated catalogs) |
| **Response Code** | HTTP 200 OK (all endpoints) |
| **Downloader Throughput** | ~1020 items/min |
| **Execution Wall Time** | ~4.6 seconds |
