# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from schedule_manager import load_schedules, save_schedules
import requests

from utils.scraper import scrape_sentiment_data
from utils.excel_scraper import get_all_sentiment_excel_data
from utils.pdf_scraper import get_all_sentiment_pdf_data, get_pdf_sentiment_history
from utils.pmi_scraper import scrape_pmi_marquee
from utils.ism_scraper_new import get_all_ism_data
from utils.ism_scraper import get_ism_history
from utils.pse_scraper import scrape_pse_index, get_pse_index_history
from utils.bls_cpi_scraper import scrape_bls_cpi_table_a, get_bls_cpi_history
from utils.bls_ppi_scraper import scrape_bls_ppi_latest_numbers, get_bls_ppi_history
from utils.jlt_scraper import scrape_jlt_latest_number, get_jlt_history, get_jlt_history_summary
from utils.conference_board_scraper import scrape_conference_board_indicators, get_conference_board_history, get_conference_board_history_summary
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for now; restrict for production
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- APScheduler setup for daily scraping at 9am ---
scheduler = BackgroundScheduler()
scheduler.start()

SCRAPER_FUNCTIONS = {
    "pdf_sentiment": get_all_sentiment_pdf_data,
    "ism_data": get_all_ism_data,
    "pse_index": scrape_pse_index,
    "bls_cpi": scrape_bls_cpi_table_a,
    "bls_ppi": scrape_bls_ppi_latest_numbers,
    "conference_board": scrape_conference_board_indicators,
    "jlt_scraper": scrape_jlt_latest_number,
    "pmi_spglobal": scrape_pmi_marquee,
    # Add more as needed
}

def reschedule_jobs():
    scheduler.remove_all_jobs()
    schedules = load_schedules()
    for module, time_str in schedules.items():
        hour, minute = map(int, time_str.split(":"))
        func = SCRAPER_FUNCTIONS.get(module)
        if func:
            scheduler.add_job(func, 'cron', hour=hour, minute=minute, id=module)

@app.get("/api/scraper-schedules")
def get_scraper_schedules():
    return load_schedules()

@app.post("/api/scraper-schedules")
async def set_scraper_schedules(request: Request):
    data = await request.json()
    save_schedules(data)
    reschedule_jobs()
    return JSONResponse({"status": "schedules updated"})
# --- End APScheduler setup ---

@app.get("/api/ism-data")
def fetch_ism_data():
    return get_all_ism_data()

@app.get("/api/pdf-sentiment")
def get_pdf_sentiment_data():
    return get_all_sentiment_pdf_data()

@app.get("/api/pdf-sentiment-history")
def get_pdf_sentiment_history_data():
    return get_pdf_sentiment_history()

@app.get("/api/ism-history")
def fetch_ism_history():
    return get_ism_history()

@app.get("/api/sentiment")
def get_html_sentiment_data():
    return scrape_sentiment_data()

@app.get("/api/excel-sentiment")
def get_excel_sentiment_data():
    return get_all_sentiment_excel_data()

@app.get("/api/pmi-marquee")
def get_pmi_marquee_data():
    return scrape_pmi_marquee()

@app.get("/api/pmi-spglobal")
def get_pmi_spglobal():
    return scrape_pmi_marquee()

@app.get("/api/pse-index")
def get_pse_index():
    return scrape_pse_index()

@app.get("/api/pse-index-history")
def get_pse_index_history_api():
    return get_pse_index_history()

@app.get("/api/bls-cpi")
def get_bls_cpi():
    return scrape_bls_cpi_table_a()

@app.get("/api/bls-cpi-history")
def get_bls_cpi_history_api():
    return get_bls_cpi_history()

@app.get("/api/bls-ppi")
def get_bls_ppi():
    return scrape_bls_ppi_latest_numbers()

@app.get("/api/bls-ppi-history")
def get_bls_ppi_history_api():
    return get_bls_ppi_history()

@app.get("/api/jlt-latest")
def get_jlt_latest():
    return scrape_jlt_latest_number()

@app.get("/api/jlt-history")
def get_jlt_history_api():
    return get_jlt_history()

@app.get("/api/jlt-history-summary")
def get_jlt_history_summary_api():
    return get_jlt_history_summary()

@app.get("/api/conference-board")
def get_conference_board_indicators():
    return scrape_conference_board_indicators()

@app.get("/api/conference-board-history")
def get_conference_board_history_api():
    return get_conference_board_history()

@app.get("/api/conference-board-history-summary")
def get_conference_board_history_summary_api():
    return get_conference_board_history_summary()
