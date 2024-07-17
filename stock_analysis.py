import yfinance as yf
import schedule
import time
from datetime import datetime
import json
from constants import *
import os
import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)

this_file = os.path.dirname(os.path.realpath(__file__))

def read_tickers(file_path):
    with open(file_path, 'r') as file:
      return json.load(file)[TICKER_ARRAY]


def is_market_open():
    now = datetime.now()
    return now.weekday() < 5 and MARKET_OPEN_HOUR <= now.hour < MARKET_CLOSE_HOUR

def fetch_data(ticker, period, interval):
    for _ in range(API_RETRY_LIMIT):
        try:
            return yf.download(ticker, period=period, interval=interval, progress=False)
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
    return None

def calculate_macd(df):
    short_ema = df['Close'].ewm(span=12, adjust=False).mean()
    long_ema = df['Close'].ewm(span=26, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd, signal

def analyze_trend(ticker, df):
    macd, signal = calculate_macd(df)
    ema_200 = df['Close'].ewm(span=200, adjust=False).mean()
    latest_price = df['Close'].iloc[-1]

    if macd.iloc[-1] < 0 and signal.iloc[-1] < 0:
        if macd.iloc[-2] < signal.iloc[-2] and macd.iloc[-1] > signal.iloc[-1] and latest_price > ema_200.iloc[-1]:
            return Trend.BULLISH
        elif macd.iloc[-2] > signal.iloc[-2] and macd.iloc[-1] < signal.iloc[-1] and latest_price < ema_200.iloc[-1]:
            return Trend.BEARISH
    return Trend.NONE

def analyze_data(tickers, period, interval):
    print(f'\nAnalyzing data on {period} period and interval {interval}')
    for ticker in tickers:
        df = fetch_data(ticker, period, interval)
        if df is not None and not df.empty:
            trend = analyze_trend(ticker, df)
            if trend != Trend.NONE:
                print(f"[{time.strftime('%I:%M:%S%p')}] {ticker}: {trend.value.capitalize()} trend detected on {period} period and {interval} interval.")

def schedule_tasks(tickers):
    schedule.every(5).minutes.do(analyze_data, tickers, '1mo', '30m')
    schedule.every(10).minutes.do(analyze_data, tickers, '1mo', '1h')
    schedule.every(20).minutes.do(analyze_data, tickers, '3mo', '2h')
    schedule.every(4).hours.do(analyze_data, tickers, '6mo', '1d')

def main():
    tickers = read_tickers(f"{this_file}/{TICKERS_JSON_PATH}")
    schedule_tasks(tickers)
    while True:
        if is_market_open():
            schedule.run_pending()
        else:
          now = datetime.now()
          if now.hour >= MARKET_CLOSE_HOUR and now.minute >= 30:
            print("Market closed for the day")
            exit()
          sleep_minutes = 30 - now.minute
          sleep_hours = (MARKET_OPEN_HOUR - now.hour) * 60
          sleep_seconds = (sleep_minutes + sleep_hours) * 60
          print(f"Market is closed, sleeping {sleep_seconds // 60} minutes seconds till open")
          time.sleep(sleep_seconds)
          continue
        time.sleep(1)

if __name__ == "__main__":
    main()
