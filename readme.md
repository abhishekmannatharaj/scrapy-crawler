uv venv
Windows: .venv\Scripts\activate 
uv pip install scrapy


## Architecture 

```text
scrapy-crawler/
├── crawler_app/              # Core Scrapy Module
│   ├── spiders/              # Custom spider definitions & link crawlers
│   ├── items.py              # Data schema containers (Field definitions)
│   ├── middlewares.py        # Request/Response hooks (User-Agents, Proxies)
│   ├── pipelines.py          # Data cleaning, validation, and storage sinks
│   └── settings.py           # Concurrency, throttling, delays, and pipelines
├── data/
│   ├── raw/                  # Local scraped feeds (JSONL/CSV) - git-ignored
│   └── processed/            # Cleaned data ready for DB ingestion
├── scrapy.cfg                # Scrapy deployment and project settings
├── requirements.txt          # Frozen dependency manifest
└── README.md