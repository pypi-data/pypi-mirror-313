# my_finance_lib/data_fetcher.py
import asyncio
import aiohttp
import pandas as pd
import time
from .utils import setup_logging

logger = setup_logging()

class RSIDataFetcher:
    def __init__(self, api_key):
        self.api_key = api_key

    async def fetch_rsi(self, session, ticker, timespan):
        url = f'https://api.polygon.io/v2/indicators/rsi/{ticker}?timespan={timespan}&apiKey={self.api_key}'
        start_time = time.perf_counter()
        try:
            async with session.get(url) as response:
                data = await response.json()
                rsi_value = data.get('rsi_value')  # Adjust based on actual API response
                logger.info(f'Fetched RSI for {ticker} over {timespan}: {rsi_value}')
                return {
                    'ticker': ticker,
                    'timespan': timespan,
                    'rsi': rsi_value
                }
        except Exception as e:
            logger.error(f'Error fetching RSI for {ticker} over {timespan}: {e}')
            return {
                'ticker': ticker,
                'timespan': timespan,
                'rsi': None
            }
        finally:
            end_time = time.perf_counter()
            logger.info(f'fetch_rsi took {end_time - start_time:.4f} seconds')

    async def rsi_snapshot(self, tickers, timespans):
        async with aiohttp.ClientSession() as session:
            tasks = [
                self.fetch_rsi(session, ticker, span)
                for ticker in tickers
                for span in timespans
            ]
            start_time = time.perf_counter()
            results = await asyncio.gather(*tasks)
            end_time = time.perf_counter()
            logger.info(f'rsi_snapshot fetched all data in {end_time - start_time:.4f} seconds')
            rsi_df = pd.DataFrame(results)
            return rsi_df

class MACDDataFetcher:
    def __init__(self, api_key):
        self.api_key = api_key

    async def fetch_macd(self, session, ticker, timespan):
        url = f'https://api.polygon.io/v2/indicators/macd/{ticker}?timespan={timespan}&apiKey={self.api_key}'
        start_time = time.perf_counter()
        try:
            async with session.get(url) as response:
                data = await response.json()
                macd_value = data.get('macd_value')  # Adjust based on actual API response
                logger.info(f'Fetched MACD for {ticker} over {timespan}: {macd_value}')
                return {
                    'ticker': ticker,
                    'timespan': timespan,
                    'macd': macd_value
                }
        except Exception as e:
            logger.error(f'Error fetching MACD for {ticker} over {timespan}: {e}')
            return {
                'ticker': ticker,
                'timespan': timespan,
                'macd': None
            }
        finally:
            end_time = time.perf_counter()
            logger.info(f'fetch_macd took {end_time - start_time:.4f} seconds')

    async def histogram_snapshot(self, tickers, timespans):
        async with aiohttp.ClientSession() as session:
            tasks = [
                self.fetch_macd(session, ticker, span)
                for ticker in tickers
                for span in timespans
            ]
            start_time = time.perf_counter()
            results = await asyncio.gather(*tasks)
            end_time = time.perf_counter()
            logger.info(f'histogram_snapshot fetched all data in {end_time - start_time:.4f} seconds')
            macd_df = pd.DataFrame(results)
            return macd_df
