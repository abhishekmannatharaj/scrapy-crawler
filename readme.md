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
scrapy crawl spiderapp -O mydata.csv
```

Prices are exported as numbers and product URLs are absolute URLs. The spider
uses XPath for product extraction and `response.urljoin` for link resolution.

## External Systems

Persistence and messaging are opt-in. Set a comma-separated list in
`SCRAPY_PERSISTENCE_BACKENDS` before starting a crawl:

```powershell
$env:SCRAPY_PERSISTENCE_BACKENDS = "postgres,mongodb,redis,rabbitmq"
$env:POSTGRES_DSN = "postgresql://user:password@localhost:5432/scrapyapp"
$env:MONGODB_URI = "mongodb://localhost:27017"
$env:REDIS_URL = "redis://localhost:6379/0"
$env:RABBITMQ_URL = "amqp://guest:guest@localhost:5672/%2F"
scrapy crawl spiderapp
```

The PostgreSQL and MongoDB pipelines persist products, Redis stores JSON items
in `scrapyapp:products`, and RabbitMQ publishes durable messages to the
`scrapyapp.items` queue. The services must be running before the crawl starts.

Celery uses RabbitMQ as its broker and Redis as its result backend by default.
Start a Windows worker from the project directory:

```powershell
celery -A scrapyapp.tasks worker --loglevel=INFO --pool=solo
```

Queue a crawl from Python or a Celery client:

```python
from scrapyapp.tasks import crawl_spider

crawl_spider.delay("spiderapp")
```

For larger deployments, run multiple Celery workers and use shared
RabbitMQ/Redis instances. Set `CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND`
when those services are not local.

## 📈 Crawl Metrics & Verification

Below are the benchmark metrics from the latest execution run:

| Metric | Value |
| :--- | :--- |
| **Item Count Extracted** | 68 products |
| **Request Count** | 4 requests (1 robots.txt + 3 paginated catalogs) |
| **Response Code** | HTTP 200 OK (all endpoints) |
| **Downloader Throughput** | ~1020 items/min |
| **Execution Wall Time** | ~4.6 seconds |


### 📋 Extracted Data Preview (Sample)

| Name | Price | Product URL |
| :--- | :--- | :--- |
| 2.5kg Bulk 41% Milk Hot Chocolate Drops | £50.00 | `/products/2-5kg-bulk-of-our-41-milk-hot-chocolate-drops` |
| 41% Milk Hot Chocolate Drops | £8.75 | `/products/41-colombian-milk-hot-chocolate-drops` |
| Blonde Caramel | £5.00 | `/products/blonde-caramel-chocolate-bar` |