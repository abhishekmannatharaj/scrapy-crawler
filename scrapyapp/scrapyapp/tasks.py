import os
import subprocess
import sys

from celery import Celery

from scrapyapp.settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND


celery_app = Celery(
    "scrapyapp",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)


@celery_app.task
def crawl_spider(spider_name="spiderapp"):
    """Run one crawl in a Celery worker process."""
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    result = subprocess.run(
        [sys.executable, "-m", "scrapy", "crawl", spider_name],
        cwd=project_dir,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout[-4000:]