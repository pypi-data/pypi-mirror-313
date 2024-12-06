import pandas as pd
import httpx
from .models.finra_models import TickerATS
from fudstop.apis.polygonio.polygon_database import PolygonDatabase
from fudstop.apis.helpers import format_large_numbers_in_dataframe
db = PolygonDatabase()
import asyncio

class FinraSDK:
    def __init__(self):
        self.headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        }

        self.download_info_payload = {"quoteValues":False,"delimiter":"|","limit":500,"fields":["weekStartDate"],"sortFields":["-weekStartDate"],"compareFilters":[{"fieldName":"summaryTypeCode","fieldValue":"ATS_W_FIRM","compareType":"EQUAL"},{"fieldName":"tierIdentifier","fieldValue":"T1","compareType":"EQUAL"}]}


    async def download_details(self):
        endpoint = f"https://api.finra.org/data/group/otcMarket/name/weeklyDownloadDetails"

        payload = self.download_info_payload
        async with httpx.AsyncClient(headers=self.headers) as client:
            data = await client.post(endpoint,json=payload, headers=self.headers)


            data = data.json()

            week_starts = [i.get('weekStartDate') for i in data]
            

            return week_starts


    async def summary(self, type:str='WEEKLY'):
        endpoint=f"https://api.finra.org/data/group/OTCMARKET/name/{type}"
        payload={"quoteValues":False,"delimiter":"|","limit":1000,"fields":[],"compareFilters":[{"fieldName":"weeklyStartDate","fieldValue":"2024-05-13","compareType":"EQUAL"}]}


        async with httpx.AsyncClient(headers=self.headers) as client:
            data = await client.post(endpoint,json=payload, headers=self.headers)


            data = data.json()

            print(data)


    async def ticker_ats(self, ticker:str, week_start:str='2024-05-13'):
        try:
            payload = {"quoteValues":False,"delimiter":"|","limit":5000,"sortFields":["-totalWeeklyShareQuantity"],"compareFilters":[{"fieldName":"summaryTypeCode","fieldValue":"ATS_W_SMBL_FIRM","compareType":"EQUAL"},{"fieldName":"issueSymbolIdentifier","fieldValue":ticker,"compareType":"EQUAL"},{"fieldName":"weekStartDate","fieldValue":week_start,"compareType":"EQUAL"},{"fieldName":"tierIdentifier","fieldValue":"T1","compareType":"EQUAL"}]}

            endpoint=f"https://api.finra.org/data/group/otcMarket/name/weeklySummary"

            async with httpx.AsyncClient(headers=self.headers) as client:
                data = await client.post(endpoint,json=payload, headers=self.headers)


                data = data.json()


                data = TickerATS(data)
                return data
        except Exception as e:
            print(e)
            
        async with httpx.AsyncClient(headers=self.headers) as client:
            response = await client.post(endpoint, json=payload)

            try:
                response.raise_for_status()  # Raise an HTTPError if the response was an HTTP error
                data = response.json()
            except httpx.HTTPStatusError as exc:
                print(f"HTTP error occurred: {exc.response.status_code} - {exc.response.text}")
                return None
            except ValueError as exc:
                print(f"JSON decoding error: {exc}")
                return None

            return TickerATS(data)
        
    async def ticker_nonats(self, ticker:str, week_start:str='2024-05-20'):
        try:
            payload={"quoteValues":True,"delimiter":"|","limit":5000,"sortFields":["-totalWeeklyShareQuantity"],"compareFilters":[{"fieldName":"summaryTypeCode","fieldValue":"OTC_W_SMBL_FIRM","compareType":"EQUAL"},{"fieldName":"issueSymbolIdentifier","fieldValue":f"{ticker}","compareType":"EQUAL"},{"fieldName":"issueName","fieldValue":"GameStop Corp. Class A","compareType":"EQUAL"},{"fieldName":"tierIdentifier","fieldValue":"T1","compareType":"EQUAL"},{"fieldName":"weekStartDate","fieldValue":week_start,"compareType":"EQUAL"}]}

            endpoint = f"https://api.finra.org/data/group/otcMarket/name/weeklySummary"
            async with httpx.AsyncClient(headers=self.headers) as client:
                data = await client.post(endpoint, json=payload)

                data = data.json()


                data = TickerATS(data)
                return data
        except Exception as e:
            print(e)
    async def all_ticker_ats(self, ticker: str):

        await db.connect()
        try:
            dates = await self.download_details()

            tasks = [self.ticker_ats(ticker, date) for date in dates]
            results = await asyncio.gather(*tasks)

            # Filter out None results in case of errors
            results = [result for result in results if result is not None]

            # Convert each result to a DataFrame and concatenate them
            dataframes = [result.as_dataframe for result in results]
            final_df = pd.concat(dataframes, ignore_index=True)
            final_df = final_df.rename(columns={'issue_symbol_identifier': 'ticker', 'market_participant_name': 'participant'})
            await db.batch_insert_dataframe(final_df, table_name='finra_ats', unique_columns='ticker, last_reported_date')
            final_df = final_df.drop(columns=['firm_crd_number', 'product_type_code', 'summary_type_code'])
            print(final_df.columns)
            return final_df
        except Exception as e:
            print(f"An error occurred: {e}")


    async def all_ticker_nonats(self, ticker:str):
        await db.connect()
        try:
            dates = await self.download_details()
            tasks = [self.ticker_nonats(ticker,date) for date in dates]
            results = await asyncio.gather(*tasks)
            results = [result for result in results if result is not None]
            dataframes = [result.as_dataframe for result in results]
            final_df = pd.concat(dataframes, ignore_index=True)
            final_df = final_df.rename(columns={'issue_symbol_identifier': 'ticker', 'market_participant_name': 'participant'})
            await db.batch_insert_dataframe(final_df, table_name='finra_nonats', unique_columns='ticker, last_reported_date')
            final_df = final_df.drop(columns=['firm_crd_number', 'product_type_code', 'summary_type_code'])
            print(final_df.columns)
            return final_df
        except Exception as e:
            print(f"An error occurred: {e}")

